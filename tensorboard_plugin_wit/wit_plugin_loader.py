# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
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
"""Wrapper around plugin to conditionally enable it."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorboard
from tensorboard.plugins import base_plugin


class WhatIfToolPluginLoader(base_plugin.TBLoader):
    """WhatIfToolPlugin factory.
    This class checks for `tensorflow` install and dependency.
    """

    def load(self, context):
        """Returns the plugin, if possible.
        Args:
          context: The TBContext flags.
        Returns:
          A WhatIfToolPlugin instance or None if it couldn't be loaded.
        """
        try:
            # pylint: disable=unused-import
            import tensorflow
        except ImportError:
            return

        # If TB version is before 2.2.0, then do not load the WIT plugin
        # as it is already included directly in TensorBoard.
        version_list = tensorboard.__version__.split(".")
        if (int(version_list[0]) < 2 or
            (int(version_list[0]) == 2 and int(version_list[1]) < 2)):
          return

        from tensorboard_plugin_wit.wit_plugin import WhatIfToolPlugin

        return WhatIfToolPlugin(context)
