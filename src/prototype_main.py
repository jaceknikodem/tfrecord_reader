"""
Usage:
    python prototype.py example/foo.tfr --definition_path=/code/src/example/foo_pb2.py \
        --proto=example.Person \
        --limit=10 \
        --select=name,address.number
"""
import sys

import gflags

import prototype

gflags.DEFINE_string("root", None, "Path to a file with a proto definition.")
gflags.DEFINE_string("proto", None, "Proto to use.")
gflags.DEFINE_integer("limit", None, "How many records to read.")
gflags.DEFINE_string("select", None, "Which fields to select.")

FLAGS = gflags.FLAGS


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    for value in prototype.query(argv[1], FLAGS.proto, FLAGS.root,
                                 FLAGS.select, FLAGS.limit):
        print value


if __name__ == "__main__":
    #gflags.MarkFlagsAsRequired(["proto"])
    print sys.argv
    argv = FLAGS(sys.argv)
    print argv
    sys.exit(main(argv))
