import sys

from tensorflow.python.lib.io import tf_record

from example import foo_pb2


def load(filepath):
    for raw in tf_record.tf_record_iterator(filepath):
        pb = foo_pb2.Person()
        pb.ParseFromString(raw)

        yield "{}".format(pb)


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    filepath = argv[1]

    for chunk in load(filepath):
        try:
            print chunk
        except (IOError, KeyboardInterrupt):
            pass  # Ignore broken pipe.


if __name__ == "__main__":
    main(sys.argv)
