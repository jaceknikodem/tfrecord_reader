import logging
import time

import gflags

import app
import reader_service_pb2
import reader_server

gflags.DEFINE_integer("port", 8888, "Port to run on.")
gflags.DEFINE_string("root", None, "Path to a file with a proto definition.")

FLAGS = gflags.FLAGS


def main(_):
    servicer = reader_server.RecordReaderServicer(FLAGS.root)
    server = reader_service_pb2.beta_create_RecordReader_server(servicer)
    logging.info("Starting a server on: %d", FLAGS.port)
    server.add_insecure_port('[::]:{}'.format(FLAGS.port))
    server.start()
    logging.info("Server started.")

    while True:
        try:
            time.sleep(60 * 60)
        except KeyboardInterrupt:
            logging.info("Shutting down the server.")
            server.stop(grace=None)
            return


if __name__ == "__main__":
    app.run()
