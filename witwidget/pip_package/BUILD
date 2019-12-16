# Description:
#  Tools for building the WitWidget Jupyter pip package.

package(default_visibility = ["//visibility:private"])

licenses(["notice"])  # Apache 2.0

# rm -rf /tmp/wit-pip
# bazel run //witwidget/pip_package:build_pip_package
sh_binary(
    name = "build_pip_package",
    srcs = ["build_pip_package.sh"],
    data = [
        "MANIFEST.in",
        "README.rst",
        "setup.py",
        "wit-widget.json",
        "//tf_interactive_inference_dashboard:wit_jupyter", # For HTML payload
        "//witwidget/notebook/jupyter/js:js_files",
        "//utils:inference_utils",  # Utility method that visualization code uses.
        "//witwidget",  # WitWidget code
        "//witwidget:version",  # Version module (read by setup.py)
    ],
    tags = [
        "local",
        "manual",
    ],
)
