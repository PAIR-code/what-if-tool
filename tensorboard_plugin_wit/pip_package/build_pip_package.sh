#!/bin/sh
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

set -e
if [ -z "${RUNFILES}" ]; then
  RUNFILES="$(CDPATH= cd -- "$0.runfiles" && pwd)"
fi

if [ "$(uname)" = "Darwin" ]; then
  sedi="sed -i ''"
else
  sedi="sed -i"
fi

set -x
command -v virtualenv >/dev/null
command -v npm >/dev/null
[ -d "${RUNFILES}" ]

plugin_runfile_dir="${RUNFILES}/ai_google_pair_wit"

dest="/tmp/wit-pip"
mkdir -p "$dest"
cd "$dest"

mkdir -p release
pushd release

rm -rf tensorboard_plugin_wit
# Copy over all necessary files from tensorboard_plugin_wit
cp -LR "$plugin_runfile_dir/tensorboard_plugin_wit" .
cp -LR "$plugin_runfile_dir/utils" .

# Move files related to pip building to pwd.
mv -f "tensorboard_plugin_wit/pip_package/README.rst" .
mv -f "tensorboard_plugin_wit/pip_package/setup.py" .

# Copy over other built resources
mkdir -p tensorboard_plugin_wit/static
mv -f "tensorboard_plugin_wit/pip_package/index.js" tensorboard_plugin_wit/static
rm -rf tensorboard_plugin_wit/pip_package
cp "$plugin_runfile_dir/wit_dashboard/wit_tb_bin.html" "$plugin_runfile_dir/wit_dashboard/wit_tb_bin.js" tensorboard_plugin_wit/static

find . -name __init__.py | xargs chmod -x  # which goes for all genfiles

# Copy interactive inference common utils over and ship it as part of the pip package.
mkdir -p tensorboard_plugin_wit/_utils
cp "$plugin_runfile_dir/utils/common_utils.py" tensorboard_plugin_wit/_utils
cp "$plugin_runfile_dir/utils/inference_utils.py" tensorboard_plugin_wit/_utils
cp "$plugin_runfile_dir/utils/platform_utils.py" tensorboard_plugin_wit/_utils
touch tensorboard_plugin_wit/_utils/__init__.py

mkdir -p tensorboard_plugin_wit/_vendor
>tensorboard_plugin_wit/_vendor/__init__.py
# Vendor tensorflow-serving-api because it depends directly on TensorFlow.
# TODO(jameswex): de-vendor if they're able to relax that dependency.
cp -LR "${RUNFILES}/org_tensorflow_serving_api/tensorflow_serving" tensorboard_plugin_wit/_vendor

# Fix the import statements to reflect the copied over path.
find tensorboard_plugin_wit -name \*.py |
  xargs $sedi -e '
    s/^from utils/from tensorboard_plugin_wit._utils/
    s/from tensorflow_serving/from tensorboard_plugin_wit._vendor.tensorflow_serving/
  '

virtualenv venv
export VIRTUAL_ENV=venv
export PATH="$PWD/venv/bin:${PATH}"
unset PYTHON_HOME

# # Require wheel for bdist_wheel command, and setuptools 36.2.0+ so that
# # env markers are handled (https://github.com/pypa/setuptools/pull/1081)
pip install -qU wheel 'setuptools>=36.2.0'

python setup.py bdist_wheel --python-tag py3 >/dev/null

ls -hal "$PWD/dist"
