# vim: fileencoding=utf8:et:sw=4:ts=8:sts=4

import logging
import sys

import feather.monitor
import greenhouse

from . import resources
from .storage import user


@greenhouse.global_exception_handler
def handle_exc(klass, exc, tb):
    logging.getLogger("legalease.error").error("greenhouse caught exception",
            exc_info=(klass, exc, tb))
    resources.statsd.incr('error.exceptions_reached_greenhouse')


def setup_logging():
    fmt = logging.Formatter(
            "%(process)d [%(asctime)s] %(name)s/%(levelname)s | %(message)s")
    access_handler = logging.FileHandler('/logs/access.log')
    error_handler = logging.FileHandler('/logs/error.log')
    access_handler.setFormatter(fmt)
    error_handler.setFormatter(fmt)
    access_log = logging.getLogger("feather.http.access")
    access_log.addHandler(access_handler)
    access_log.setLevel(1)
    error_log = logging.getLogger("feather.http.errors")
    error_log.addHandler(error_handler)
    error_log.setLevel(1)

    ll_logger = logging.getLogger("legalease")
    ll_logger.addHandler(error_handler)
    ll_logger.setLevel(1)

    sys.stdout = open("/logs/stdout.log", "a")
    sys.stderr = open("/logs/stderr.log", "a")


class Monitor(feather.monitor.Monitor):
    # long parses (coeur.pdf) take too much CPU time and the feather master
    # decides that the worker is dead, hard-killing it. in any real production
    # setup we would separate out this CPU work and make it an I/O wait in the
    # feather server, but for now just bump up the monitor's timeout.
    WORKER_TIMEOUT = 5.0

    # the fork destroys all open FDs, so open the FileHandlers *afterwards*
    def worker_postfork(self, worker_id, process_id):
        setup_logging()
        resources.setup_redispool()
        resources.setup_dbpool()
        resources.setup_statsd()

        # FIXME: temporary while we are on a single global document list
        user.ensure_static_user()
