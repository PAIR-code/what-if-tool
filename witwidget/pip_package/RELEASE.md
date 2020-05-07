# To release a new version of witwidget on PyPI and NPM:

1. Ensure updated version numbers have been merged to the master branch in
witwidget/version.py and witwidget/notebook/jupyter/js/package.json
2. Tag the commit that updates the version with version number and add release notes to the commit description.
3. Clone this repository and checkout the commit that set the new version numbers.
4. `bazel run witwidget/pip_package:build_pip_package`
5. Upload the whl files created by the previous step to PyPI as per instructions
at https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives.
6. Publish the new NPM package through running `npm publish` in the `js/` subdirectory of the package
files generated during the build step.
