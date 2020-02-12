package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "tf_web_library")
load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")

licenses(["notice"])  # Apache 2.0

tf_web_library(
    name = "multidemo",
    testonly = True,
    srcs = [
        "multi_index.html",
        "wit-multi-demo.html",
        "@org_tf_tfjs//:tf.min.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "multidemoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/multi_index.html",
    output_path = "/wit-dashboard/multi_demo.html",
    deps = [":multidemo"],
)

tf_web_library(
    name = "demo",
    testonly = True,
    srcs = [
        "index.html",
        "wit-demo.html",
        "@org_tf_tfjs//:tf.min.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "demoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/index.html",
    output_path = "/wit-dashboard/demo.html",
    deps = [":demo"],
)

tf_web_library(
    name = "imagedemo",
    testonly = True,
    srcs = [
        "image_index.html",
        "wit-image-demo.html",
        "@org_tf_tfjs//:tf.min.js",
        "@org_tf_tfjs_mobilenet//:mobilenet.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "imagedemoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/image_index.html",
    output_path = "/wit-dashboard/image_demo.html",
    deps = [":imagedemo"],
)

tf_web_library(
    name = "irisdemo",
    testonly = True,
    srcs = [
        "iris_index.html",
        "wit-iris-demo.html",
        "@org_tf_tfjs//:tf.min.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "irisdemoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/iris_index.html",
    output_path = "/wit-dashboard/iris_demo.html",
    deps = [":irisdemo"],
)

tf_web_library(
    name = "agedemo",
    testonly = True,
    srcs = [
        "age_index.html",
        "wit-age-demo.html",
        "@org_tf_tfjs//:tf.min.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "agedemoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/age_index.html",
    output_path = "/wit-dashboard/age_demo.html",
    deps = [":agedemo"],
)

tf_web_library(
    name = "compasdemo",
    testonly = True,
    srcs = [
        "compas_index.html",
        "wit-compas-demo.html",
        "@org_tf_tfjs//:tf.min.js",
    ] + glob(["data/**"]),
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "//wit_dashboard",
    ],
)

tensorboard_html_binary(
    name = "compasdemoserver",
    testonly = True,  # Keeps JavaScript somewhat readable
    compile = True,  # Run Closure Compiler
    input_path = "/wit-dashboard/compas_index.html",
    output_path = "/wit-dashboard/compas_demo.html",
    deps = [":compasdemo"],
)