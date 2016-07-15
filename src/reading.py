import binascii
import struct


class PyRecordReader(object):
    """Pure Python implementation of tensorflow/python/lib/io/py_record_reader.h"""

    def __init__(self, fp):
        self._fp = fp

    def read_record(self):
        raw = self._fp.read(8)
        length = struct.unpack('q', raw)[0]

        crc = binascii.crc32(raw) % (1 << 32)
        masked_length = ((crc >> 15) | (crc << 17)) + 0xa282ead8

        raw = self._fp.read(4)
        expected = struct.unpack('I', raw)[0]
        # TODO(nikodem): Add CRC checks.

        data = self._fp.read(length)

        self._fp.read(4)

        return data

    def read(self):
        while True:
            try:
                yield self.read_record()
            except struct.error:
                return
