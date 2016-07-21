import itertools

import prototype
import reader_service_pb2


class RecordReaderServicer(reader_service_pb2.RecordReaderServicer):
    def Query(self, request, context):
        for chunk in prototype.query(request.file_path, request.proto,
                                     request.root, request.select,
                                     request.limit):
            response = reader_service_pb2.QueryResponse()
            response.chunk = chunk
            yield response

    def Write(self, request, response):
        prototype.query_and_save(request.file_path, request.output_path,
                                 request.proto, request.root, request.limit)
        return reader_service_pb2.WriteResponse()

    def Complete(self, request, context):
        response = reader_service_pb2.CompletionResponse()
        names = prototype.proto_names()
        if request.prefix:
            names = itertools.ifilter(lambda k: k.startswith(request.prefix),
                                      names)

        response.options.extend(sorted(names))
        return response
