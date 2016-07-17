import prototype
import reader_service_pb2


class RecordReaderServicer(reader_service_pb2.RecordReaderServicer):
    def Query(self, request, context):
        limit = request.limit if request.HasField("limit") else None
        for chunk in prototype.query(request.file_path, request.proto,
                                     request.root, request.select, limit):
            response = reader_service_pb2.QueryResponse()
            response.chunk = chunk
            yield response
