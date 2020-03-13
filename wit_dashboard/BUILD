package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "tf_web_library")
load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")

licenses(["notice"])  # Apache 2.0

tf_web_library(
    name = "wit_example_viewer",
    srcs = [
        "wit-example-viewer.html",
        "wit-example-viewer.ts",
    ],
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:d3",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "@org_polymer_iron_autogrow_textarea",
        "@org_polymer_iron_icons",
        "@org_polymer_paper_button",
        "@org_polymer_paper_card",
        "@org_polymer_paper_checkbox",
        "@org_polymer_paper_dialog",
        "@org_polymer_paper_icon_button",
        "@org_polymer_paper_input",
        "@org_polymer_paper_radio_button",
        "@org_polymer_paper_radio_group",
        "@org_polymer_paper_slider",
        "@org_tensorflow//tensorflow/core:example_protos_closure",
    ],
)

tf_web_library(
    name = "wit_dashboard",
    srcs = [
        "wit-dashboard.html",
    ],
    path = "/wit-dashboard",
    deps = [
        ":wit_attribution_table",
        ":wit_confusion_matrix",
        ":wit_example_viewer",
        ":wit_inference_panel",
        ":wit_inference_viewer",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_backend",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_dashboard_common",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_tensorboard:plugin_dialog",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_tensorboard:registry",
        "@org_tensorflow_tensorboard//tensorboard/components/vz_bar_chart",
        "@org_tensorflow_tensorboard//tensorboard/components/vz_line_chart2",
        "@ai_google_pair_facets//facets_dive/components/facets_dive",
        "@ai_google_pair_facets//facets_overview/components/facets_overview",
        "@org_polymer_iron_collapse",
        "@org_polymer_iron_icons",
        "@org_polymer_iron_pages",
        "@org_polymer_paper_button",
        "@org_polymer_paper_dialog",
        "@org_polymer_paper_dropdown_menu",
        "@org_polymer_paper_icon_button",
        "@org_polymer_paper_input",
        "@org_polymer_paper_item",
        "@org_polymer_paper_listbox",
        "@org_polymer_paper_progress",
        "@org_polymer_paper_radio_button",
        "@org_polymer_paper_radio_group",
        "@org_polymer_paper_slider",
        "@org_polymer_paper_styles",
        "@org_polymer_paper_tabs",
        "@org_polymer_paper_toast",
        "@org_polymer_paper_toggle_button",
    ],
)

tf_web_library(
    name = "wit_lib",
    srcs = [
        "wit.html",
    ],
    path = "/wit-dashboard",
    deps = [
        ":wit_dashboard",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
    ],
)

tensorboard_html_binary(
    name = "wit_bin",
    compile = True,
    input_path = "/wit-dashboard/wit.html",
    output_path = "/all/wit.html",
    deps = [
        ":wit_lib",
    ],
)

genrule(
    name = "wit_jupyter",
    srcs = [":wit_bin"],
    outs = ["wit_jupyter.html"],
    cmd = "sed 's|<!doctype html>|<!doctype html><script>define=undefined</script>|' $(location :wit_bin) > $@",
)

tf_web_library(
    name = "wit_tensorboard",
    srcs = [
        "wit-tensorboard.html",
    ],
    path = "/wit-dashboard",
    deps = [
        ":wit_dashboard",
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "@org_tensorflow_tensorboard//tensorboard/components:security",
    ],
)

tensorboard_html_binary(
    name = "wit_tb_bin",
    compile = True,
    input_path = "/wit-dashboard/wit-tensorboard.html",
    output_path = "/wit_tb_bin.html",
    js_path = "/wit_tb_bin.js",
    deps = [
        ":wit_tensorboard",
    ],
)
    

tf_web_library(
    name = "wit_inference_viewer",
    srcs = [
        "wit-inference-viewer.html",
    ],
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
        "@org_polymer_iron_icons",
    ],
)

tf_web_library(
    name = "wit_confusion_matrix",
    srcs = [
        "wit-confusion-matrix.html",
    ],
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
    ],
)

tf_web_library(
    name = "wit_attribution_table",
    srcs = [
        "wit-attribution-table.html",
    ],
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/tf_imports:polymer",
    ],
)

tf_web_library(
    name = "wit_inference_panel",
    srcs = [
        "wit-inference-panel.html",
    ],
    path = "/wit-dashboard",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/components/experimental/plugin_lib:plugin_lib_polymer_interop",
        "@org_polymer_paper_button",
        "@org_polymer_paper_input",
        "@org_polymer_paper_radio_button",
        "@org_polymer_paper_radio_group",
    ],
)
