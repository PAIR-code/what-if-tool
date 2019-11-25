load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def wit_workspace():
    # We use `mock==1.0.0` because later versions depend on `pbr`, which
    # doesn't work well in a hermetic context (it tries to look up some
    # global configuration files; see GitHub pull request #2132).
    #
    # This dependency can go away entirely once we drop Python 2 support
    # and can just depend on `unittest.mock`.
    http_archive(
        name = "org_pythonhosted_mock",
        urls = [
            "http://mirror.tensorflow.org/files.pythonhosted.org/packages/85/60/ec8c1af81337bab0caba188b218b6758bc94f125f49062f7c5f0647749d2/mock-1.0.0.tar.gz",
            "https://files.pythonhosted.org/packages/85/60/ec8c1af81337bab0caba188b218b6758bc94f125f49062f7c5f0647749d2/mock-1.0.0.tar.gz",
        ],
        sha256 = "2d9fbe67001d2e8f02692075257f3c11e1b0194bd838c8ce3f49b31fc6c3f033",
        strip_prefix = "mock-1.0.0",
        build_file = str(Label("//third_party:mock.BUILD")),
        patches = [
            # `mock==1.0.0` lacks some assertion methods present in
            # later versions of `mock` (see comment above for why we pin
            # to this version). Patch created by diffing the pinned
            # `mock.py` with GitHub head and identifying all the bits
            # that looked related to the methods in question.
            "//third_party:mock_call_assertions.patch",
        ],
    )

    http_archive(
        name = "org_pythonhosted_six",
        urls = [
            "http://mirror.tensorflow.org/pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
            "http://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
        ],
        sha256 = "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a",
        strip_prefix = "six-1.10.0",
        build_file = str(Label("//third_party:six.BUILD")),
    )
