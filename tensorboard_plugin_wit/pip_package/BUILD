# Description:
#  Tools for building the WitWidget TensorBoard pip package.

package(default_visibility = ["//visibility:private"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "tf_web_library")

licenses(["notice"])  # Apache 2.0

# rm -rf /tmp/wit-pip
# bazel run //tensorboard_plugin_wit/pip_package:build_pip_package
sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = [
        "index.js",
        "README.rst",
        "setup.py",
        ":assets", # For HTML payload
        "//utils:inference_utils",  # Utility method that visualization code uses.
        "//tensorboard_plugin_wit:wit_plugin",  # WIT TensorBoard plugin code
    ],
    tags = [
        "local",
        "manual",
    ],
)

tf_web_library(
    name = "assets",
    srcs = [
        "//wit_dashboard:wit_tb_bin.html",
        "//wit_dashboard:wit_tb_bin.js",
    ],
    path = "/",
)
