package(default_visibility = ["//visibility:public"])

licenses(["notice"])  # Apache 2.0

py_library(
    name = "wit_plugin",
    srcs = ["wit_plugin.py"],
    srcs_version = "PY2AND3",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard:expect_numpy_installed",
        "@org_tensorflow_tensorboard//tensorboard/backend:http_util",
        "@org_tensorflow_tensorboard//tensorboard/plugins:base_plugin",
        "//utils:common_utils",
        "//utils:inference_utils",
        "//utils:platform_utils",
        "@org_pocoo_werkzeug",
    ],
)

py_test(
    name = "wit_plugin_test",
    size = "small",
    srcs = ["wit_plugin_test.py"],
    deps = [
        ":wit_plugin",
        "@org_tensorflow_tensorboard//tensorboard:expect_numpy_installed",
        "@org_tensorflow_tensorboard//tensorboard/backend:application",
        "@org_tensorflow_tensorboard//tensorboard/backend/event_processing:event_multiplexer",
        "//utils:inference_utils",
        "//utils:platform_utils",
        "//utils:test_utils",
        "@org_pocoo_werkzeug",
        "@org_pythonhosted_mock",
        "@org_pythonhosted_six",
    ],
)
