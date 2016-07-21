import os
import subprocess
import time
import unittest

from grpc.framework.interfaces.face import face

import reader_client

CODE_BASE = os.environ.get("CODE_BASE")

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

_SRC_ROOT = os.path.join(CODE_BASE, "src")
_ROOT = os.path.join(_SRC_ROOT, "example")
_FILE_PATH = os.path.join(_ROOT, "*.tfr")
_PROTO = "example.Person"
_PORT = 8004


class QueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = subprocess.Popen(["python", os.path.join(
            _SRC_ROOT, "reader_server_main.py"), "--port={}".format(_PORT)])
        time.sleep(1)
        cls.client = reader_client.ReaderClient("localhost", _PORT)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()

    def assertExists(self, filepath):
        self.assertTrue(
            os.path.exists(filepath),
            "Filepath {} doesn't exists.".format(filepath))

    def test_query_and_save(self):
        output_path = os.path.join(_ROOT, "foo.txt")
        self.client.query_and_save(
            _FILE_PATH, output_path,
            _PROTO, _ROOT, limit=1)
        self.assertExists(output_path)

    def test_proto_not_provided(self):
        with self.assertRaises(face.RemoteError):
            list(self.client.query(_FILE_PATH, None, _ROOT))

    def test_proto_not_found(self):
        with self.assertRaisesRegexp(face.RemoteError, "mean example.Person"):
            list(self.client.query(_FILE_PATH, "example.FakeProto", _ROOT))

    def test_root_not_found(self):
        with self.assertRaisesRegexp(face.RemoteError, "doesn't exist"):
            list(self.client.query(_FILE_PATH, _PROTO, "/fake_root"))

    def test_data_file_not_found(self):
        with self.assertRaises(face.RemoteError):
            list(self.client.query("/fake_path", _PROTO, _ROOT))

    def test_query_all(self):
        output = list(self.client.query(_FILE_PATH, _PROTO, _ROOT))
        self.assertEqual(len(output), 100)

    def test_limit_one(self):
        output = list(self.client.query(_FILE_PATH, _PROTO, _ROOT, limit=1))
        self.assertEqual(len(output), 1)

    def test_select_fields(self):
        output = list(self.client.query(_FILE_PATH, _PROTO, _ROOT, limit=1))
        self.assertItemsEqual(output, [_FIRST_ITEM])

    def test_select_empty_fields(self):
        output = list(self.client.query(
            _FILE_PATH, _PROTO, _ROOT,
            limit=1, select=""))
        self.assertItemsEqual(output, [_FIRST_ITEM])

    def test_select_top_level_single_field(self):
        output = list(self.client.query(
            _FILE_PATH, _PROTO,
            _ROOT, limit=1, select="name"))
        self.assertItemsEqual(output, ["name:\tPatrick"])

    def test_select_top_level_complex_field(self):
        output = list(self.client.query(
            _FILE_PATH, _PROTO,
            _ROOT, limit=1,
            select="address"))
        self.assertItemsEqual(output,
                              ['address:\tstreet: "Tavistock"\nnumber: 47\n'])

    def test_select_two_top_level_fields(self):
        output = list(self.client.query(
            _FILE_PATH,
            _PROTO, _ROOT,
            limit=1, select="name, address"))
        self.assertItemsEqual(
            output,
            ['name:\tPatrick\naddress:\tstreet: "Tavistock"\nnumber: 47\n'])

    def test_select_subfield(self):
        output = list(self.client.query(_FILE_PATH,
                                        _PROTO,
                                        _ROOT,
                                        limit=1,
                                        select="address.number"))
        self.assertItemsEqual(output, ['address.number:\t47'])


if __name__ == "__main__":
    unittest.main()
