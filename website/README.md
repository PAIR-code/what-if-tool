# What-If Tool Homepage and Demos

This repository contains the code for the What-If Tool landing page and demo websites, which is hosted as a github page.

Check out all the web demos and colab demos here: https://pair-code.github.io/what-if-tool/#demos

## Building the Demos

The What-If Tool demo source code is in the [TensorBoard](https://github.com/tensorflow/tensorboard/tree/master/tensorboard/plugins/interactive_inference) respository and is built from there using `bazel` and copied over.

## Local Testing of the Homepage and Demos

1. Install 11ty to your machine (globally if you have permissions), run `npm install -g @11ty/eleventy`. You may need to use sudo in front of this command, depending on the setup of npm on your computer of choice.
2. From this directory, run `./local.sh`
3. Navigate to `http://localhost:8080`
