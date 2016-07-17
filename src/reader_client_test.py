import os
import unittest

from grpc.framework.interfaces.face import face

import reader_client

# TODO(nikodem): Find a proper way to pass code base folder with Bazel.
CODE_BASE = os.environ.get("CODE_BASE") or "/code"

_FIRST_ITEM = """name: "Patrick"
address {
  street: "Tavistock"
  number: 47
}
things {
  name: "car"
  value: 99.7218780518
}
things {
  name: "bottle"
  value: 8.25360012054
}
"""


class QueryTest(unittest.TestCase):
    def setUp(self):
        self._root = CODE_BASE
        self._file_path = os.path.join(CODE_BASE, "src", "example", "foo.tfr")
        self._proto = "example.Person"

    def test_proto_not_provided(self):
        with self.assertRaises(face.RemoteError):
            list(reader_client.query(self._file_path, None, self._root))

    def test_proto_not_found(self):
        with self.assertRaisesRegexp(face.RemoteError, "mean example.Person"):
            list(reader_client.query(self._file_path, "example.FakeProto",
                                     self._root))

    def test_root_not_found(self):
        with self.assertRaisesRegexp(face.RemoteError, "doesn't exist"):
            list(reader_client.query(self._file_path, self._proto,
                                     "/fake_root"))

    def test_data_file_not_found(self):
        with self.assertRaises(face.RemoteError):
            list(reader_client.query("/fake_path", self._proto, self._root))

    def test_query_all(self):
        output = list(reader_client.query(self._file_path, self._proto,
                                          self._root))
        self.assertEqual(len(output), 100)

    def test_limit_one(self):
        output = list(reader_client.query(
            self._file_path, self._proto,
            self._root, limit=1))
        self.assertEqual(len(output), 1)

    def test_limit_zero(self):
        with self.assertRaises(ValueError):
            list(reader_client.query(self._file_path,
                                     self._proto,
                                     self._root,
                                     limit=0))

    def test_select_fields(self):
        output = list(reader_client.query(
            self._file_path, self._proto,
            self._root, limit=1))
        self.assertItemsEqual(output, [_FIRST_ITEM])

    def test_select_empty_fields(self):
        output = list(reader_client.query(self._file_path,
                                          self._proto,
                                          self._root,
                                          limit=1,
                                          select=""))
        self.assertItemsEqual(output, [_FIRST_ITEM])

    def test_select_top_level_single_field(self):
        output = list(reader_client.query(self._file_path,
                                          self._proto,
                                          self._root,
                                          limit=1,
                                          select="name"))
        self.assertItemsEqual(output, ["name:\tPatrick"])

    def test_select_top_level_complex_field(self):
        output = list(reader_client.query(self._file_path,
                                          self._proto,
                                          self._root,
                                          limit=1,
                                          select="address"))
        self.assertItemsEqual(output,
                              ['address:\tstreet: "Tavistock"\nnumber: 47\n'])

    def test_select_two_top_level_fields(self):
        output = list(reader_client.query(self._file_path,
                                          self._proto,
                                          self._root,
                                          limit=1,
                                          select="name, address"))
        self.assertItemsEqual(
            output,
            ['name:\tPatrick\naddress:\tstreet: "Tavistock"\nnumber: 47\n'])

    def test_select_subfield(self):
        output = list(reader_client.query(self._file_path,
                                          self._proto,
                                          self._root,
                                          limit=1,
                                          select="address.number"))
        self.assertItemsEqual(output, ['address.number:\t47'])


if __name__ == "__main__":
    unittest.main()
