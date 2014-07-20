# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

from datahog import context, flag, storage, table
import mummy

# users
USER = 1
context.set_context(USER, table.ENTITY)

# documents -- nodes under a user
DOC = 2
context.set_context(DOC, table.NODE, {
  'base_ctx': USER,
  'storage': storage.SERIAL,
  'schema': {
    'name': str,
    'path': mummy.UNION(str, unicode),
    'tfs': [(int, float)] # int is a term guid, float is the tf value
  },
})

# lookup documents by "%d:%s" % (user_id, doc_name)
DOC_LOOKUP = 3
context.set_context(DOC_LOOKUP, table.ALIAS, {'base_ctx': DOC})

# document has been written to filesystem, and isn't a race-condition duplicate
DOC_OK = 1
flag.set_flag(DOC_OK, DOC)

# terms -- nodes under a user storing idf values
TERM = 4
context.set_context(TERM, table.NODE, {
  'base_ctx': USER,
  'storage': storage.INT,
})

TERM_LOOKUP = 5
context.set_context(TERM_LOOKUP, table.ALIAS, {'base_ctx': TERM})

DOC_SCORE = 6
context.set_context(DOC_SCORE, table.RELATIONSHIP, {'base_ctx': DOC})
