import contextlib
import datetime
import logging
import os
import sys

import gflags

gflags.DEFINE_bool("logtostderr", False, "Should we log to stderr.")

FLAGS = gflags.FLAGS

LOGGING_ROOT = "/log"


@contextlib.contextmanager
def supress_exception(cls):
    try:
        yield
    except cls:
        pass


def setup_logging(logtostderr, script_name):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s] %(levelname)s - %(message)s")

    with supress_exception(OSError):
        os.mkdir(LOGGING_ROOT)

    timestamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = os.path.join(LOGGING_ROOT, "{}.{}".format(script_name,
                                                         timestamp))
    with supress_exception(OSError):
        os.symlink(filename, os.path.join(LOGGING_ROOT, script_name))
    handler = logging.FileHandler(filename, mode='w')

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if logtostderr:
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setLevel(logging.DEBUG)

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def run(main=None):
    argv = gflags.FLAGS(sys.argv)

    main = main or sys.modules['__main__'].main

    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    setup_logging(FLAGS.logtostderr, script_name)

    sys.exit(main(argv))
