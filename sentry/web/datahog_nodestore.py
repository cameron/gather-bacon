# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

from datahog import context, table, entity, prop, storage, pool
from django.conf import settings
from sentry.nodestore import base


BASE = 1
context.set_context(BASE, table.ENTITY)

BLOB = 2
context.set_context(BLOB, table.PROPERTY, {
    'base_ctx': BASE,
    'storage': storage.SERIAL,
})


class NodeStorage(base.NodeStorage):
    def __init__(self, **config):
        super(NodeStorage, self).__init__()
        self._dbpool = None
        self._config = config

    @property
    def pool(self):
        if self._dbpool is None:
            p = self._dbpool = pool.GreenhouseConnPool(self._config)
            p.start()
            if not p.wait_ready(2.0):
                raise Exception("postgres connection timeout")

        return self._dbpool

    def delete(self, id):
        entity.remove(self.pool, long(id), BASE)

    def get(self, id):
        return prop.get(self.pool, id, BLOB)['value']

    def set(self, id, data):
        return prop.set(self.pool, id, BLOB, data)

    def generate_id(self):
        return entity.create(self.pool, BASE)['guid']
