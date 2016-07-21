"""
Usage:
    python prototype.py example/foo.tfr --definition_path=/code/src/example/foo_pb2.py \
        --proto=example.Person \
        --limit=10 \
        --select=name,address.number \
        --where="'{name}'=='Patrick'"
"""
import difflib
import fnmatch
import glob
import gzip
import imp
import os
import re

from google.protobuf import symbol_database

import reading

NO_LIMIT = -1
_KEY = "key_"
_CURLY = re.compile(r'{([a-zA-Z.]*)}')


def find_files(folder, glob):
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, glob):
            yield os.path.join(root, filename)


def load_protos(root):
    if not os.path.exists(root):
        raise ValueError("Specified directory doesn't exist.")

    for filename in find_files(root, "*_pb2.py"):
        name, _ = os.path.splitext(os.path.basename(filename))
        if not imp.load_source(name, filename):
            print 'Issue loading {} module from: {}'.format(name, filename)


def proto_names():
    return symbol_database.Default().pool._descriptors.iterkeys()


def get_prototype(name):
    db = symbol_database.Default()
    try:
        descriptor = db.pool.FindMessageTypeByName(name)
    except KeyError:
        closest = difflib.get_close_matches(name, proto_names(), n=1)
        if closest:
            msg = "Proto {} not found. Did you mean {}?".format(name,
                                                                closest[0])
        else:
            msg = "No protos registered."
        raise ValueError(msg)
    else:
        return db.GetPrototype(descriptor)


def select_fields(pb, field_names, index):
    values = []
    for field_name in field_names:
        value = pb
        if field_name == _KEY:
            value = index
        else:
            for subfield in field_name.split('.'):
                if not hasattr(value, subfield):
                    raise ValueError(
                        "Field: {} not present. Available fields: {}".format(
                            field_name, pb.DESCRIPTOR.fields_by_name.keys()))
                value = getattr(value, subfield)

        values.append((field_name, value))
    return values


def load_records(file_pattern, proto_cls):
    file_paths = glob.glob(file_pattern)
    if not file_paths:
        try:
            names = os.listdir(os.path.basename(file_pattern))
        except IOError:
            names = []
        raise ValueError("No files matching: {}. Present files: {}".format(
            file_pattern, names))

    for path in file_paths:
        file_obj = gzip.open(path, "rb") if path.endswith(".gz") else open(
            path, "r")
        with file_obj as fp:
            reader = reading.PyRecordReader(fp)
            for raw in reader.read():
                pb = proto_cls()
                pb.ParseFromString(raw)
                yield pb


def query(file_path, proto, select=None, limit=NO_LIMIT):
    if proto is None:
        raise ValueError("PB name has to provided.")

    proto_cls = get_prototype(proto)
    field_names = [f.strip() for f in select.split(",")] if select else []

    for i, pb in enumerate(load_records(file_path, proto_cls)):
        try:
            if field_names:
                yield "\n".join("{}:\t{}".format(k, v)
                                for k, v in select_fields(pb, field_names, i))
            else:
                yield "{}".format(pb)
        except (IOError, KeyboardInterrupt):
            pass  # Ignore broken pipe.
        if limit > 0 and i >= limit - 1:
            return


def query_and_save(file_path, output_path, proto, limit=NO_LIMIT):
    if proto is None:
        raise ValueError("PB name has to provided.")

    proto_cls = get_prototype(proto)

    with open(output_path, "w") as fp:
        for i, pb in enumerate(load_records(file_path, proto_cls)):
            try:
                fp.write("{}".format(pb))
            except (IOError, KeyboardInterrupt):
                pass  # Ignore broken pipe.
            if limit > 0 and i >= limit - 1:
                return
            fp.write("\n")
