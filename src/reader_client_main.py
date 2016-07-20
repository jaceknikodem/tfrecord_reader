import sys

import gflags

import app
import reader_client

# Server flags
gflags.DEFINE_string("host", "localhost", "Server host.")
gflags.DEFINE_integer("port", 8888, "Server port.")
gflags.DEFINE_integer("timeout", 5, "Timeout in seconds.")

# Query flags
gflags.DEFINE_string("root", None, "Path to a file with a proto definition.")
gflags.DEFINE_string("proto", None, "Proto to use.")
gflags.DEFINE_integer("limit", None, "How many records to read.")
gflags.DEFINE_string("select", None, "Which fields to select.")

FLAGS = gflags.FLAGS


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    client = reader_client.ReaderClient(FLAGS.host, FLAGS.port)

    for chunk in client.query(argv[1], FLAGS.proto, FLAGS.root, FLAGS.select,
                       FLAGS.limit, FLAGS.timeout):
        print chunk


if __name__ == "__main__":
    gflags.MarkFlagsAsRequired(["proto"])
    app.run()
