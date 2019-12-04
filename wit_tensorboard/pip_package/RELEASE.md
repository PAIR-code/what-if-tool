# To release a new version of wit_tensorboard on PyPI:

1. Ensure the updated version number have been merged to the master branch in
wit_tensorboard/pip_package/setup.py.
2. Clone this repository and checkout the commit that set the new version numbers.
3. `bazel run wit_tensorboard/pip_package:build_pip_package`
4. Upload the whl files created by the previous step to PyPI as per instructions
at https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives.
