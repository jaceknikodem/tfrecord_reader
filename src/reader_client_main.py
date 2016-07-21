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
gflags.DEFINE_string("output_file", None,
                     "Path to the output file to generate.")

FLAGS = gflags.FLAGS


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    file_path = argv[1]

    client = reader_client.ReaderClient(FLAGS.host, FLAGS.port, FLAGS.timeout)

    if FLAGS.output_file:
        client.query_and_save(file_path, FLAGS.output_file, FLAGS.root,
                              FLAGS.limit)
        return

    for chunk in client.query(file_path, FLAGS.proto, FLAGS.root, FLAGS.select,
                              FLAGS.limit):
        print chunk


if __name__ == "__main__":
    gflags.MarkFlagsAsRequired(["proto"])
    app.run()
