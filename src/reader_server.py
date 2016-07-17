import reader_service_pb2


class RecordReaderServicer(reader_service_pb2.RecordReaderServicer):
    def Quit(self, request, context):
        return reader_service_pb2.EmptyResponse()
