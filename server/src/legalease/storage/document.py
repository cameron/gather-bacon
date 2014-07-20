# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

'''Document metadata storage
'''

import functools
import os
import time
import uuid
import sys

from datahog import alias, error, node, relationship
from datahog.const import util as hog_util
import greenhouse

from .. import resources
from . import const

BASEDIR = '/docs'
STOP_WORDS = set([x[:-1] for x in open("/srv/app/legalease/storage/stoplist.txt").readlines() if x[0] != "#"])


# TODONT
term_ids = terms = terms_to_ids = ids_to_terms = ids_to_idfs = None
def _fetch_terms():
    global terms_to_ids, ids_to_terms, ids_to_idfs
    term_ids = node.list_children(resources.dbpool, 1, const.TERM, limit=50000)
    terms = node.batch_get(resources.dbpool, zip(term_ids, [const.TERM]*len(term_ids)))
    terms_to_ids = dict([(t['term'], t['guid']) for t in terms])
    ids_to_terms = dict([(t['guid'], term) for t in terms])
    ids_to_idfs = None


def _redis_optional(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except resources.redis.ConnectionError:
            return None
    return decorator


def store(uid, filename, contents):
    """store a document

    :param int uid: the owner's user id
    :param str filename: the externally-visible doc name
    :param contents: file-like object of the file's contents
    """
    node = _store(uid, filename, contents)

    if node is None:
        return None

    _store_cache(uid, node['value']['name'], node['value']['path'])

    @greenhouse.schedule
    def update_idfs_and_score():
        _update_idfs(node['value']['tfs'])
        _score(node)

    return path

def _score(node):
    offset, doc_ids = node.list_children(resources.dbpool, uid, const.DOC)
    docs = node.batch_get(resources.dbpool, zip(doc_ids, [const.DOC]*len(doc_ids)))
    cur_tf_idfs = _tf_idfs(node['value']['tfs'])
    for doc in docs:
        doc_tf_idfs = _tf_idfs(doc['value']['tfs'])
        shared_terms = set(cur_tf_idfs.keys()).intersection(set(doc_tf_idfs.keys()))
        cur_vec_magnitude = _magnitude(shared_terms, cur_tf_idfs)
        vec_magnitude = _magnitude(shared_terms, doc_tf_idfs)
        dot_prod = sum(cur_tf_idfs[term] * doc_tf_idfs[term] for term in shared_terms)
        score = dot_prod / (cur_vec_magnitude * vec_magnitude)
        relationship.create(resources.dbpool, 
                            const.DOC_SCORE, 
                            node['guid'], 
                            doc['guid'], 
                            flags=hog_util.int_to_flags(score * sys.maxint))

def _magnitude(terms, weights):
    return math.sqrt(sum(math.pow(weights[term], 2) for term in terms))

def _tfs(doc_string):
    ''' Turns a document into a dictionary of word frequencies normalized
    for length
    
    :param str doc_string: the document to convert
    '''
    contents = re.sub("[^\w]+"," ", doc_string.lower()).split()
    words = [w for w in contents if len(x) and x not in STOP_WORDS]

    tfs, counts = {}, {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    content_length = float(len(contents))
    for term, count in counts.iteritems():
        tfs[terms_to_ids[term]] = count / content_length

    return tfs

def _update_idfs(tfs={}):
    if ids_to_terms is None: # TODONT
        _fetch_terms()

    for term in tfs:
        node = ids_to_terms[terms_to_ids[term]]
        node['value']['doc_count'] += 1
        node.update(db.resources, node['guid'], const.TERM, node['value'])

    for term_id, term_node in ids_to_terms.iteritems():
        ids_to_idfs[term_id] = math.log(doc_count / term_node['value']['doc_count'])

def _tf_idfs(tfs):
    tf_idfs = {}
    for term in tfs:
        tf_idfs[term] = tfs[term] * ids_to_idfs[terms_to_ids[term]]
    return tf_idfs

def _store(uid, filename, contents):
    path = uuid.uuid4().hex

    n = node.create(resources.dbpool, 
                    uid, 
                    const.DOC,
                    {'name': filename, 
                     'path': path, 
                     'tfs': _tfs(contents)}, 
                    timeout=1.0)

    try:
        alias.set(resources.dbpool, n['guid'], const.DOC_LOOKUP,
                "%d:%s" % (uid, filename), timeout=1.0)
    except error.AliasInUse:
        @greenhouse.schedule
        def cleanup():
            node.remove(resources.dbpool, n['guid'], const.DOC, uid)
        return None

    with open(os.path.join(BASEDIR, path), 'wb') as fp:
        for chunk in _chunked_read(contents):
            fp.write(chunk)

    node.add_flags(resources.dbpool,
            n['guid'], const.DOC, [const.DOC_OK], timeout=1.0)

    return n

@_redis_optional
def _store_cache(uid, filename, path):
    resources.get_redis().set("%d:doc:%s" % (uid, filename), path)


def retrieve(uid, filename):
    """read back a document's contents

    :param int uid: the owner's user id
    :param str filename: the externally visible document name

    :returns: a generator of bytestrings that produces the document, or None
    """
    path = _retrieve_cache(uid, filename)

    if path is None:
        path = _retrieve(uid, filename)

    if path is None:
        return None

    return _chunked_file_read(os.path.join(BASEDIR, path))

@_redis_optional
def _retrieve_cache(uid, filename):
    return resources.get_redis().get("%d:doc:%s" % (uid, filename))

def _retrieve(uid, filename):
    a = alias.lookup(resources.dbpool, "%d:%s" % (uid, filename),
            const.DOC_LOOKUP, timeout=1.0)
    if a is None:
        return None

    n = node.get(resources.dbpool, a['base_id'], const.DOC, timeout=1.0)
    if n is None:
        return None

    return n['value']['path']


def enumerate_docs(uid):
    "generate the metadata of documents owned by a user"
    start = 0
    while 1:
        chunk, start = node.get_children(resources.dbpool,
                uid, const.DOC, start=start, timeout=1.0)

        if not chunk:
            return

        for n in chunk:
            if const.DOC_OK in n['flags']:
                yield n['value']


def _chunked_file_read(filepath, chunksize=8192):
    with open(filepath, 'rb') as fp:
        for chunk in _chunked_read(fp, chunksize):
            yield chunk


def _chunked_read(obj, chunksize=8192):
    while 1:
        chunk = obj.read(chunksize)
        if chunk == '':
            return
        yield chunk
