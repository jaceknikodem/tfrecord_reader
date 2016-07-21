from grpc.beta import implementations
import retrying

import reader_service_pb2


def _create_request(cls, **kwargs):
    request = cls()
    for k, v in kwargs.iteritems():
        if v is not None:
            setattr(request, k, v)
    return request


class ReaderClient(object):
    def __init__(self, host, port, timeout=5, reconnect=5):
        self._port = port
        self._host = host
        self._timeout = timeout

        # connect = retrying.retry(self._connect,
        #                          stop_max_attempt_number=reconnect) if reconnect else self._connect
        self._stub = self._connect()

    def _connect(self):
        channel = implementations.insecure_channel(self._host, self._port)
        return reader_service_pb2.beta_create_RecordReader_stub(channel)

    def complete(self, words, current, timeout=None):
        timeout = timeout or self._timeout

        request = reader_service_pb2.CompletionRequest()
        request.words.extend(words)
        request.current = current
        response = self._stub.Complete(request, timeout)
        return list(response.options)

    def query(self,
              file_path,
              proto,
              root=None,
              select=None,
              limit=None,
              timeout=5):
        timeout = timeout or self._timeout

        request = _create_request(reader_service_pb2.QueryRequest,
                                  file_path=file_path,
                                  proto=proto,
                                  root=root,
                                  select=select,
                                  limit=limit)
        for response in self._stub.Query(request, timeout):
            yield response.chunk

    def query_and_save(self,
                       file_path,
                       output_path,
                       proto,
                       root=None,
                       limit=None,
                       timeout=5):
        timeout = timeout or self._timeout

        request = _create_request(reader_service_pb2.WriteRequest,
                                  file_path=file_path,
                                  output_path=output_path,
                                  proto=proto,
                                  root=root,
                                  limit=limit)
        self._stub.Write(request, timeout)
