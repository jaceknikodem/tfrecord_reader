"""
Usage:
    python prototype.py example/foo.tfr --definition_path=/code/src/example/foo_pb2.py \
        --proto=example.Person \
        --limit=10 \
        --select=name,address.number
"""
import sys

# TODO(nikodem): Use gflags here.
import tensorflow as tf

import prototype

tf.flags.DEFINE_string("root", None, "Path to a file with a proto definition.")
tf.flags.DEFINE_string("proto", None, "Proto to use.")
tf.flags.DEFINE_integer("limit", None, "How many records to read.")
tf.flags.DEFINE_string("select", None, "Which fields to select.")

FLAGS = tf.flags.FLAGS


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    for value in prototype.query(argv[1], FLAGS.proto, FLAGS.root,
                                 FLAGS.select, FLAGS.limit):
        print value


if __name__ == "__main__":
    tf.app.run()
