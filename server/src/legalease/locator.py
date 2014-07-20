#!/usr/bin/env python
# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import bisect
from cStringIO import StringIO
import re
import sys

from pyPdf import PdfFileReader


the_term = re.compile(ur'\((?:the )?["\u2020]([^)"]+)["\u2021]\)')
as_term = re.compile(
        ur', as ["\u2020]?((?:[A-Z][a-z]+ )*[A-Z][a-z]+)["\u2021]?,')


switches = {
    'ref required': True,
    'ref before def': True,
}

def switch(name):
    return switches.get(name, False)


class PDFDoc(object):
    def __init__(self, text):
        self.text = text
        self.pages = []
        self.offsets = []

    def parse(self):
        reader = PdfFileReader(StringIO(self.text))
        self.text = None
        offset = 0
        for i in xrange(reader.numPages):
            text = reader.getPage(i).extractText(Tj_suffix=' ')
            self.pages.append(text)
            self.offsets.append(offset)
            offset += len(text)

    def matches(self, regex, overlap=20):
        prev = None
        if isinstance(regex, (str, unicode)):
            regex = re.compile(regex)

        for n, (offset, text) in enumerate(zip(self.offsets, self.pages)):
            if prev:
                prefix = prev[-overlap:]
                text = prefix + text
                offset -= len(prefix)

            for match in re.finditer(regex, text):
                if prev and match.end() < overlap:
                    # contained entirely in the overlap section, so
                    # we already got this match in the previous page
                    continue

                item = {
                    'regex': regex.pattern,
                    'term': match.group(1),
                    'page': n,
                    'start': offset + match.start(),
                    'end': offset + match.end(),
                }

                if prev and match.start() < overlap:
                    # count this match on the previous
                    # page if it straddles the boundary
                    item['page'] -= 1

                yield item

            prev = text

    def page_index(self, global_position, page=None):
        if page is None:
            page = bisect.bisect_right(self.offsets, global_position)
        return global_position - self.offsets[page]


def definitions(doc, regexen):
    if not isinstance(doc, PDFDoc):
        doc = PDFDoc(doc)

    if not doc.pages:
        doc.parse()

    defns = {}

    for regex in regexen:
        for defn in doc.matches(regex):
            existing = defns.get(defn['term'])
            if not existing:
                refs = []
                for ref in doc.matches(ur'(%s)' % re.escape(defn['term'])):
                    # skip the ref that shows up in the definition itself
                    if defn['start'] <= ref['start'] < defn['end']:
                        continue
                    refs.append(ref)

                defns[defn['term']] = {
                    'term': defn['term'],
                    'candidates': [],
                    'references': refs,
                }

            defns[defn['term']]['candidates'].append(defn)

    if switch('ref required'):
        # pull out terms lacking a reference
        # besides the definition itself (!)
        for defn in defns.values():
            if not defn['references']:
                del defns[defn['term']]

    if switch('ref before def'):
        # pull out any terms which have a reference
        # before the earliest candidate definition
        for defn in defns.values():
            if not defn['references']:
                continue

            d = defn['candidates'][0]
            r = defn['references'][0]
            if r['start'] < d['start'] - len(defn['term']) - 5:
                del defns[defn['term']]

    return defns


def terms(text, regexen):
    doc = PDFDoc(text)
    defns = definitions(doc, regexen)
    return doc, defns

def report(text, regexen, out=None):
    if out is None:
        out = sys.stdout
    doc, defns = terms(text, regexen) 
    for defn in defns.itervalues():
        print >>out, '-' * 80
        print >>out, defn['term'] + ':'
        for cand in defn['candidates']:
            start = doc.page_index(cand['start'], cand['page'])
            end = doc.page_index(cand['end'], cand['page'])
            print >>out, '  page %s candidate: %r' % (
                    str(cand['page'] + 1).zfill(3),
                    doc.pages[cand['page']][start-20:end+20])

        for ref in defn['references']:
            start = doc.page_index(ref['start'], ref['page'])
            end = doc.page_index(ref['end'], ref['page'])
            print >>out, '  page %s reference: %r' % (
                    str(ref['page'] + 1).zfill(3),
                    doc.pages[ref['page']][start-20:end+20])


if __name__ == '__main__':
    report(open('eg-docs/coeur.pdf', 'r').read(), [the_term, as_term])
