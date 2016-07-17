import logging

import gflags
from grpc.beta import implementations

import app
import reader_service_pb2

gflags.DEFINE_integer("port", 8888, "Server port.")
gflags.DEFINE_integer("timeout", 5, "Timeout in seconds.")

FLAGS = gflags.FLAGS


def main(_):
    channel = implementations.insecure_channel('localhost', FLAGS.port)
    stub = reader_service_pb2.beta_create_RecordReader_stub(channel)

    logging.info("Sending request to the server.")
    request = reader_service_pb2.EmptyRequest()
    response = stub.Quit(request, FLAGS.timeout)
    print "Response: ", response


if __name__ == "__main__":
    app.run()
