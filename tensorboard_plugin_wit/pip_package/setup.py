# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorboard_plugin_wit",
    version="1.7.0",
    description="What-If Tool TensorBoard plugin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://whatif-tool.dev",
    author='Google Inc.',
    author_email='packages@tensorflow.org',
    packages=setuptools.find_packages(),
    license='Apache 2.0',
    package_data={
        "tensorboard_plugin_wit": ["static/**"],
    },
    entry_points={
        "tensorboard_plugins": [
            "wit = tensorboard_plugin_wit.wit_plugin_loader:WhatIfToolPluginLoader",
        ],
    },
)
