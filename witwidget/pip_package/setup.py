# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
from setuptools import find_packages, setup

project_name = 'witwidget'
# Set when building the pip package
if '--project_name' in sys.argv:
  project_name_idx = sys.argv.index('--project_name')
  project_name = sys.argv[project_name_idx + 1]
  sys.argv.remove('--project_name')
  sys.argv.pop(project_name_idx)

_TF_REQ = [
    'tensorflow>=1.12.1',
]

REQUIRED_PACKAGES = [
    'absl-py >= 0.4',
    'google-api-python-client>=1.7.8',
    'ipywidgets>=7.0.0',
    'oauth2client>=4.1.3',
    'six>=1.12.0',
] + _TF_REQ

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_version():
  version_ns = {}
  with open(os.path.join('witwidget', 'version.py')) as f:
   exec(f.read(), {}, version_ns)
  return version_ns['VERSION'].replace('-', '')

setup(
  name=project_name,
  version=get_version(),
  description='What-If Tool notebook widget',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://whatif-tool.dev",
  author='Google Inc.',
  include_package_data=True,
  data_files=[
      ('share/jupyter/nbextensions/wit-widget', [
        'witwidget/static/extension.js',
        'witwidget/static/index.js',
        'witwidget/static/index.js.map',
        'witwidget/static/wit_jupyter.html',
      ],),
      ('etc/jupyter/nbconfig/notebook.d/', ['wit-widget.json'])
  ],
  packages=find_packages(),
  zip_safe=False,
  install_requires=REQUIRED_PACKAGES,
  keywords=[
      'ipython',
      'jupyter',
      'widgets',
  ],
  license='Apache 2.0',
  classifiers=[
      'Development Status :: 4 - Beta',
      'Framework :: IPython',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'Topic :: Multimedia :: Graphics',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
  ]
)
