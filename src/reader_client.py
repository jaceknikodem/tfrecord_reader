import sys

import gflags
from grpc.beta import implementations

import app
import reader_service_pb2

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


def create_request(**kwargs):
    request = reader_service_pb2.QueryRequest()
    for k, v in kwargs.iteritems():
        if v is not None:
            setattr(request, k, v)
    return request


def query(file_path,
          proto,
          root=None,
          select=None,
          limit=None,
          host='localhost',
          port=8888,
          timeout=5):
    channel = implementations.insecure_channel(host, port)
    stub = reader_service_pb2.beta_create_RecordReader_stub(channel)

    request = create_request(file_path=file_path,
                             proto=proto,
                             root=root,
                             select=select,
                             limit=limit)
    for response in stub.Query(request, timeout):
        yield response.chunk


def main(argv):
    if len(argv) == 1:
        print "Missing input path"
        sys.exit(1)

    for chunk in query(argv[1], FLAGS.proto, FLAGS.root, FLAGS.select,
                       FLAGS.limit, FLAGS.host, FLAGS.port, FLAGS.timeout):
        print chunk


if __name__ == "__main__":
    gflags.MarkFlagsAsRequired(["proto"])
    app.run()
