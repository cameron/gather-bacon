# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

'''User storage

for now in our pre-user state, this is going to be a hack to make sure there is
just one "global" user with entity id 1.

this way we can structure document storage as being user-specific, but still
get the global doc store we want in this proof-of-concept phase.
'''

import psycopg2

from .. import resources
from . import const


GLOBAL_UID = 1

#FIXME: this is only for the single global user model
def ensure_static_user():
    global GLOBAL_UID

    with resources.dbpool.get_by_shard(0, timeout=1.0) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
insert into entity (guid, ctx, flags)
values (%s, 1, 0)
""", (GLOBAL_UID,))
        except psycopg2.IntegrityError:
            conn.rollback()
        except Exception:
            conn.rollback()
            raise

        # unconditionally skip a value. this might be unnecessary, but at least
        # the sequence will definitely not allocate 1 after this.
        cursor.execute("select nextval('guids')")
        conn.commit()
