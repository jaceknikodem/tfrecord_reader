import itertools

import prototype
import reader_service_pb2


class RecordReaderServicer(reader_service_pb2.RecordReaderServicer):
    def __init__(self, root):
        super(RecordReaderServicer, self).__init__()

        self._root = root

        prototype.load_protos(root)

    def Query(self, request, context):
        limit = request.limit if request.HasField(
            "limit") else prototype.NO_LIMIT
        for chunk in prototype.query(request.file_path, request.proto,
                                     request.select, limit):
            response = reader_service_pb2.QueryResponse()
            response.chunk = chunk
            yield response

    def Write(self, request, response):
        limit = request.limit if request.HasField(
            "limit") else prototype.NO_LIMIT
        prototype.query_and_save(request.file_path, request.output_path,
                                 request.proto, limit)
        return reader_service_pb2.WriteResponse()

    def Complete(self, request, context):
        response = reader_service_pb2.CompletionResponse()
        names = prototype.proto_names()
        if request.prefix:
            names = itertools.ifilter(lambda k: k.startswith(request.prefix),
                                      names)

        response.options.extend(sorted(names))
        return response
