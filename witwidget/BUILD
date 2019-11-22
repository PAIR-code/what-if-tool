package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # Apache 2.0

py_library(
    name = "witwidget",
    srcs = glob([
        "__init__.py",
        "notebook/**/*.py",
    ]),
    srcs_version = "PY2AND3",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard:expect_absl_logging_installed",
        "@org_tensorflow_tensorboard//tensorboard:expect_tensorflow_installed",
        "//utils:inference_utils",
        "@com_google_protobuf//:protobuf_python",
        "@org_pythonhosted_six",
    ]
)

py_library(
    name = "version",
    srcs = ["version.py"],
    srcs_version = "PY2AND3",
)
