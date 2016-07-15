
py_library(
    name = "prototype",
    srcs = ["prototype.py"],
)

py_binary(
    name = "prototype_main",
    srcs = ["prototype_main.py"],
    deps = [":prototype"],
)

py_test(
    name = "prototype_test",
    srcs = ["prototype_test.py"],
    deps = [":prototype"],
    size = "small",
)