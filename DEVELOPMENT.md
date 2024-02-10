# What-If Tool Development Guide

Building the What-If Tool has been verified to work with bazel version 0.27.
Later versions of bazel are currently untested and may fail to build the package.

## First-time Setup

1. Install [Bazel](https://docs.bazel.build/versions/master/install.html)
(for building OSS code) and [npm](https://www.npmjs.com/get-npm).
1. Install pip and virtualenv
   `sudo apt-get install python-pip python3-pip virtualenv`
1. Create a python 3 virtualenv for WIT development
   `virtualenv -p python3 ~/tf` (or wherever you want to save this environment)
1. Create a fork of the official What-If Tool github repo through the GitHub UI
1. Clone your fork to your computer
   `cd ~/github && git clone https://github.com/[yourGitHubUsername]/what-if-tool.git`
1. Install TensorFlow through pip `pip install tensorflow` to get TensorFlow and
   TensorBoard.

### Additional setup for testing WIT in TensorBoard

To test WIT in TensorBoard, you need to use Docker to host TensorFlow models
using [TensorFlow Serving](https://github.com/tensorflow/serving).

1. Install [Docker](https://docs.docker.com/install/).
1. Install TensorFlow Serving through docker:
   `docker pull tensorflow/serving` 


## Development Workflow
These steps have been tested when using the bash shell and may not work in other shells.  The build steps for local development mostly mirror production builds.  To speed this up, you can add the [`compilation_level="BUNDLE"` flag](https://github.com/PAIR-code/what-if-tool/issues/89) to the relevant `tf_tensorboard_html_binary` build tasks.


1. Enter your development virtualenv
   `source ~/tf/bin/activate`
1. Run TensorBoard, WIT notebooks, and/or WIT demos
   `cd ~/github/what-if-tool`
    - For WIT demos, follow the directions in the [README](./README.md#i-dont-want-to-read-this-document-can-i-just-play-with-a-demo).
        1. `bazel run wit_dashboard/demo:<demoRule>`
        1. Navigate to `http://localhost:6006/wit-dashboard/<demoName>.html`
    - For use in notebook mode, build the witwidget pip package locally and use it in a notebook.
        1. `rm -rf /tmp/wit-pip` (if it already exists)
        1. `bazel run witwidget/pip_package:build_pip_package`
        1. Install the package
            - For use in Jupyter notebooks, install and enable the locally-build pip package per instructions in the [README](./README.md#how-do-i-enable-it-for-use-in-a-jupyter-notebook), but instead use `pip install <pathToBuiltPipPackageWhlFile>`, then launch the jupyter notebook kernel.
            - For use in Colab notebooks, upload the package to the notebook and install it from there
                1. In a notebook cell, to upload a file from local disk, run
                    ```
                    from google.colab import files
                    uploaded = files.upload()
                    ```
                1. In a notebook cell, to install the uploaded pip package, run `!pip install <nameOfPackage.whl>`.
                   If witwidget was previously installed, uninstall it first.<br>
    - For TensorBoard use, build and install the tensorboard_plugin_wit package, then run tensorboard with any logdir (e.g. ./), as WIT does not rely on logdir.<br>
        1. Build the tensorboard_plugin_wit pip package as per instuctions in the
           [tensorboard_plugin_wit release instructions](tensorboard_plugin_wit/pip_package/RELEASE.md).
        1. Install the locally-build tensorboard_plugin_wit pip package with `pip install /tmp/wit-pip/release/dist/<packageName>`
        1. WIT needs a served model to query, so serve your trained model through the TF serving docker container.<br>
           `sudo docker run -p 8500:8500 --mount type=bind,source=<pathToSavedModel>,target=/models/my_model/ -e MODEL_NAME=my_model -t tensorflow/serving`
            - When developing model comparison, serve multiple models at once using the proper config as seen in the appendix.<br>
                `sudo docker run -p 8500:8500 --mount type=bind,source=<pathToSavedModel1>,target=/models/my_model1 -e When you want to shutdown the served model, find the container ID and stop the container.MODEL_NAME=my_model_1 --mount type=bind,source=<pathToSavedModel2>,target=/models/my_model_2 -e MODEL_NAME=my_model_2 When you want to shutdown the served model, find the container ID and stop the container.--mount type=bind,source=<pathToConfigFile>,target=/models/models.config -t tensorflow/serving --model_config_file="/models/models.config"`
        1. Run TensorBoard `tensorboard --logdir /tmp`
        1. Navigate to the WIT tab in TensorBoard and set-up WIT (`http://localhost:6006/#whatif&inferenceAddress=localhost%3A8500&modelName=my_model`).<br>
           The inferenceAddress and modelName settings point to the model you served in the previous step. Set all other appropriate options and click “accept”.
        1. When you want to shutdown the served model, find the container ID and stop the container.
            ```
            sudo docker container ls
            sudo docker stop <containerIdFromLsOutput>
            ```
1. The python code has unit tests
   ```
   bazel test ...
   ```
1. Add/commit your code changes on a branch in your fork and push it to github.
1. In the github UI for the master what-if-tool repo, create a pull request from your pushed branch.

For notebook users to see new changes to the code, we need to push out a new version of the witwidget pip packages.
Instructions for that can be found in the [witwidget release instructions](witwidget/pip_package/RELEASE.md).

For TensorBoard users to see new changes to the code, we need to push out a new version of the tensorboard_plugin_wit pip packages,
and then TensorBoard must be updated to use the new tensorboard_plugin_wit package version.
Instructions for building and releasing new tensorboard_plugin_wit packages can be found in the [tensorboard_plugin_wit release instructions](tensorboard_plugin_wit/pip_package/RELEASE.md).

## Code Overview

### Backend (Python)

[wit_plugin.py](wit_plugin.py) - the python web backend code for the WIT plugin to TensorBoard. Handles requests from the browser (like load examples, infer examples, …). Loads data from disk. Sends inference requests to servo. Sends responses back to the browser.<br>
[wit_plugin_test.py]() - UT<br>

[utils/common_utils.py](./utils/common_utils.py) - utilities common to other python files<br>
[utils/inference_utils.py](./utils/inference_utils.py) - utility functions for running inference requests through a model<br>
[utils/inference_utils_test.py](./utils/inference_utils_test.py) - UT<br>
[utils/platform_utils.py](./utils/platform_utils.py) - functions specific to the open-source implementation (loading examples from disk, calling to servo)<br>
[utils/test_utils.py](./utils/test_utils.py) - helper functions for UTs<br>

[witwidget/notebook/base.py](witwidget/notebook/base.py) - WitWidgetBase class definition for using WIT in notebooks. Shared base class for both jupyter and colab implementations<br>
[witwidget/notebook/visualization.py](witwidget/notebook/visualization.py) - WitConfigBuilder class definition for using WIT in notebooks<br>

[witwidget/notebook/colab/wit.py](witwidget/notebook/colab/wit.py) - backend for running in colab, along with front-end glue code to display WIT in colab<br>

[witwidget/notebook/jupyter/wit.py](witwidget/notebook/jupyter/wit.py) - backend for running in jupyter<br>
[witwidget/notebook/jupyter/js/lib/wit.js](witwidget/notebook/jupyter/js/lib/wit.js) - front-end glue code to display WIT in jupyter<br>

### Front-end

[wit_dashboard/wit-dashboard.html](wit_dashboard/wit-dashboard.html) - top-level polymer element and most of the code for the WIT front-end<br>
[wit_dashboard/wit-confusion-matrix.html](wit_dashboard/wit-confusion-matrix.html) - polymer element for the confusion matrix<br>
[wit_dashboard/wit-inference-panel.html](wit_dashboard/wit-inference-panel.html) - polymer element for the set-up controls<br>
[wit_dashboard/wit-inference-viewer.html](wit_dashboard/wit-inference-viewer.html) - polymer element for the inference results table<br>
[wit_dashboard/wit-example-viewer.html](wit_dashboard/wit-example-viewer.html) - HTML code for polymer element for the individual example viewer/editor<br>
[wit_dashboard/wit-example-viewer.ts](wit_dashboard/wit-example-viewer.ts) - Typescript code for polymer element for the individual example viewer/editor<br>

### Demos

[wit_dashboard/demo/wit-*-demo.html](wit_dashboard/demo/) - the code for the standalone web demos of WIT that load a tensorflow.js model and some data from json and runs WIT<br>

## Appendix

### Serving multiple models: models.config contents

```
model_config_list: {

config: {
    name: "my_model_1",
    base_path: "/models/my_model_1",
    model_platform: "tensorflow"
    },
config: {
    name: "my_model_2",
    base_path: "/models/my_model_2",
    model_platform: "tensorflow"
    }
}
```
