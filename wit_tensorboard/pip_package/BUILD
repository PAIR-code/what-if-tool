# Description:
#  Tools for building the WitWidget TensorBoard pip package.

package(default_visibility = ["//visibility:private"])

licenses(["notice"])  # Apache 2.0

# rm -rf /tmp/wit-pip
# bazel run //wit_tensorboard/pip_package:build_pip_package
sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = [
        "MANIFEST.in",
        "README.rst",
        "setup.py",
        "//tf_interactive_inference_dashboard:wit_tb_bin", # For HTML payload
        "//utils:inference_utils",  # Utility method that visualization code uses.
        "//wit_tensorboard",  # WIT TensorBoard plugin code
    ],
    tags = [
        "local",
        "manual",
    ],
)
