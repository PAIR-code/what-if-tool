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
# ==============================================================================
"""The plugin serving the interactive inference tab."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import io
import json
import logging
import math
import numpy as np
import os
import werkzeug
from werkzeug import wrappers
from six.moves import xrange  # pylint: disable=redefined-builtin

from google.protobuf import json_format
from grpc.framework.interfaces.face.face import AbortionError
from werkzeug import wrappers

import tensorflow as tf

from tensorboard.backend import http_util
from tensorboard.plugins import base_plugin
from utils import common_utils
from utils import inference_utils
from utils import platform_utils

logger = logging.getLogger('tensorboard')


# Max number of examples to scan along the `examples_path` in order to return
# statistics and sampling for features.
NUM_EXAMPLES_TO_SCAN = 50

# Max number of mutants to show per feature (i.e. num of points along x-axis).
NUM_MUTANTS = 10

# Max number of examples to send in a single response.
# TODO(jameswex): Make dynamic based on example size.
MAX_EXAMPLES_TO_SEND = 10000

class WhatIfToolPlugin(base_plugin.TBPlugin):
  """Plugin for understanding/debugging model inference.
  """

  # This string field is used by TensorBoard to generate the paths for routes
  # provided by this plugin. It must thus be URL-friendly. This field is also
  # used to uniquely identify this plugin throughout TensorBoard. See BasePlugin
  # for details.
  plugin_name = 'whatif'
  examples = []
  updated_example_indices = set()
  sprite = None
  example_class = tf.train.Example

  # The standard name for encoded image features in TensorFlow.
  image_feature_name = 'image/encoded'

  # The width and height of the thumbnail for any images for Facets Dive.
  sprite_thumbnail_dim_px = 32

  # The vocab of inference class indices to label names for the model.
  label_vocab = []

  def __init__(self, context):
    """Constructs an interactive inference plugin for TensorBoard.

    Args:
      context: A base_plugin.TBContext instance.
    """
    self._logdir = context.logdir
    self._wit_data_dir = context.flags.wit_data_dir if context.flags else None

    self.custom_predict_fn = None
    if context.flags and context.flags.custom_predict_fn:
      try:
        import importlib.util as iu
        spec = iu.spec_from_file_location("custom_predict_fn", context.flags.custom_predict_fn)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.custom_predict_fn = module.custom_predict_fn
        logger.info("custom_predict_fn loaded.")

      except Exception as e:
        logger.error(str(e))
        logger.error("Failed to load the custom predict function.")
        logger.error("Have you defined a function named custom_predict_fn?")

  def get_plugin_apps(self):
    """Obtains a mapping between routes and handlers. Stores the logdir.

    Returns:
      A mapping between routes and handlers (functions that respond to
      requests).
    """
    return {
        '/index.js': self._serve_js,
        '/wit_tb_bin.html': self._serve_wit,
        '/wit_tb_bin.js': self._serve_wit_js,
        '/infer': self._infer,
        '/update_example': self._update_example,
        '/examples_from_path': self._examples_from_path_handler,
        '/sprite': self._serve_sprite,
        '/duplicate_example': self._duplicate_example,
        '/delete_example': self._delete_example,
        '/infer_mutants': self._infer_mutants_handler,
        '/eligible_features': self._eligible_features_from_example_handler,
        '/sort_eligible_features': self._sort_eligible_features_handler,
    }

  def is_active(self):
    """Determines whether this plugin is active.

    Returns:
      A boolean. Whether this plugin is active.
    """
    # TODO(jameswex): Maybe enable if config flags were specified?
    return False

  def frontend_metadata(self):
    return base_plugin.FrontendMetadata(
      es_module_path="/index.js",
      tab_name='What-If Tool')

  @wrappers.Request.application
  def _serve_js(self, request):
    del request  # unused
    filepath = os.path.join(os.path.dirname(__file__), "static", "index.js")
    with io.open(filepath, encoding='utf-8') as infile:
      contents = infile.read()
    return werkzeug.Response(contents, content_type="application/javascript")
  
  @wrappers.Request.application
  def _serve_wit(self, request):
    del request  # unused
    filepath = os.path.join(os.path.dirname(__file__), "static", "wit_tb_bin.html")
    with io.open(filepath, encoding='utf-8') as infile:
      contents = infile.read()
    return werkzeug.Response(contents, content_type="text/html")

  @wrappers.Request.application
  def _serve_wit_js(self, request):
    del request  # unused
    filepath = os.path.join(os.path.dirname(__file__), "static", "wit_tb_bin.js")
    with io.open(filepath, encoding='utf-8') as infile:
      contents = infile.read()
    return werkzeug.Response(contents, content_type="application/javascript")
  def generate_sprite(self, example_strings):
    # Generate a sprite image for the examples if the examples contain the
    # standard encoded image feature.
    feature_list = (self.examples[0].features.feature
        if self.example_class == tf.train.Example
        else self.examples[0].context.feature)
    self.sprite = (
        inference_utils.create_sprite_image(example_strings)
        if (len(self.examples) and self.image_feature_name in feature_list) else
        None)

  @wrappers.Request.application
  def _examples_from_path_handler(self, request):
    """Returns JSON of the specified examples.

    Args:
      request: A request that should contain 'examples_path' and 'max_examples'.

    Returns:
      JSON of up to max_examples of the examples in the path.
    """
    start_example = (int(request.args.get('start_example'))
        if request.args.get('start_example') else 0)
    if not start_example:
      examples_count = int(request.args.get('max_examples'))
      examples_path = request.args.get('examples_path')
      sampling_odds = float(request.args.get('sampling_odds'))
      self.example_class = (tf.train.SequenceExample
          if request.args.get('sequence_examples') == 'true'
          else tf.train.Example)
      try:
        platform_utils.throw_if_file_access_not_allowed(examples_path,
                                                        self._logdir,
                                                        self._wit_data_dir)
        example_strings = platform_utils.example_protos_from_path(
            examples_path, examples_count, parse_examples=False,
            sampling_odds=sampling_odds, example_class=self.example_class)
        self.examples = [
            self.example_class.FromString(ex) for ex in example_strings]
        self.generate_sprite(example_strings)
        self.updated_example_indices = set(range(len(self.examples)))
      except common_utils.InvalidUserInputError as e:
        logger.error('Data loading error: %s', e.message)
        return http_util.Respond(request, e.message,
                                'application/json', code=400)
      except Exception as e:
        return http_util.Respond(request, str(e),
                                'application/json', code=400)

    # Split examples from start_example to + max_examples
    # Send next start_example if necessary
    end_example = start_example + MAX_EXAMPLES_TO_SEND
    json_examples = [
        json_format.MessageToJson(example) for example in self.examples[
          start_example:end_example]
    ]
    if end_example >= len(self.examples):
      end_example = -1
    return http_util.Respond(
        request,
        {'examples': json_examples,
         'sprite': True if (self.sprite and not start_example) else False,
         'next': end_example},
        'application/json')

  @wrappers.Request.application
  def _serve_sprite(self, request):
    return http_util.Respond(request, self.sprite, 'image/png')

  @wrappers.Request.application
  def _update_example(self, request):
    """Updates the specified example.

    Args:
      request: A request that should contain 'index' and 'example'.

    Returns:
      An empty response.
    """
    if request.method != 'POST':
      return http_util.Respond(request, 'invalid non-POST request',
                               'application/json', code=405)
    example_json = request.form['example']
    index = int(request.form['index'])
    if index >= len(self.examples):
      return http_util.Respond(request, 'invalid index provided',
                               'application/json', code=400)
    new_example = self.example_class()
    json_format.Parse(example_json, new_example)
    self.examples[index] = new_example
    self.updated_example_indices.add(index)
    self.generate_sprite([ex.SerializeToString() for ex in self.examples])
    return http_util.Respond(request, {}, 'application/json')

  @wrappers.Request.application
  def _duplicate_example(self, request):
    """Duplicates the specified example.

    Args:
      request: A request that should contain 'index'.

    Returns:
      An empty response.
    """
    index = int(request.args.get('index'))
    if index >= len(self.examples):
      return http_util.Respond(request, 'invalid index provided',
                               'application/json', code=400)
    new_example = self.example_class()
    new_example.CopyFrom(self.examples[index])
    self.examples.append(new_example)
    self.updated_example_indices.add(len(self.examples) - 1)
    self.generate_sprite([ex.SerializeToString() for ex in self.examples])
    return http_util.Respond(request, {}, 'application/json')

  @wrappers.Request.application
  def _delete_example(self, request):
    """Deletes the specified example.

    Args:
      request: A request that should contain 'index'.

    Returns:
      An empty response.
    """
    index = int(request.args.get('index'))
    if index >= len(self.examples):
      return http_util.Respond(request, 'invalid index provided',
                               'application/json', code=400)
    del self.examples[index]
    self.updated_example_indices = set([
        i if i < index else i - 1 for i in self.updated_example_indices])
    self.generate_sprite([ex.SerializeToString() for ex in self.examples])
    return http_util.Respond(request, {}, 'application/json')

  def _parse_request_arguments(self, request):
    """Parses comma separated request arguments

    Args:
      request: A request that should contain 'inference_address', 'model_name',
        'model_version', 'model_signature'.

    Returns:
      A tuple of lists for model parameters
    """
    inference_addresses = request.args.get('inference_address').split(',')
    model_names = request.args.get('model_name').split(',')
    model_versions = request.args.get('model_version').split(',')
    model_signatures = request.args.get('model_signature').split(',')
    if len(model_names) != len(inference_addresses):
      raise common_utils.InvalidUserInputError('Every model should have a ' +
                                                'name and address.')
    return inference_addresses, model_names, model_versions, model_signatures

  @wrappers.Request.application
  def _infer(self, request):
    """Returns JSON for the `vz-line-chart`s for a feature.

    Args:
      request: A request that should contain 'inference_address', 'model_name',
        'model_type, 'model_version', 'model_signature' and 'label_vocab_path'.

    Returns:
      A list of JSON objects, one for each chart.
    """
    start_example = (int(request.args.get('start_example'))
        if request.args.get('start_example') else 0)
    if not start_example:
      label_vocab = inference_utils.get_label_vocab(
        request.args.get('label_vocab_path'))
      try:
        if request.method != 'GET':
          logger.error('%s requests are forbidden.', request.method)
          return http_util.Respond(request, 'invalid non-GET request',
                                      'application/json', code=405)

        (inference_addresses, model_names, model_versions,
            model_signatures) = self._parse_request_arguments(request)

        self.indices_to_infer = sorted(self.updated_example_indices)
        examples_to_infer = [self.examples[index] for index in self.indices_to_infer]
        self.infer_objs = []
        self.extra_outputs = []
        for model_num in xrange(len(inference_addresses)):
          serving_bundle = inference_utils.ServingBundle(
              inference_addresses[model_num],
              model_names[model_num],
              request.args.get('model_type'),
              model_versions[model_num],
              model_signatures[model_num],
              request.args.get('use_predict') == 'true',
              request.args.get('predict_input_tensor'),
              request.args.get('predict_output_tensor'),
              custom_predict_fn=self.custom_predict_fn)
          (predictions, extra_output) = inference_utils.run_inference_for_inference_results(
              examples_to_infer, serving_bundle)
          self.infer_objs.append(predictions)
          self.extra_outputs.append(extra_output)
        self.updated_example_indices = set()
      except AbortionError as e:
        logging.error(str(e))
        return http_util.Respond(request, e.details,
                                'application/json', code=400)
      except Exception as e:
        logging.error(str(e))
        return http_util.Respond(request, str(e),
                                'application/json', code=400)

    # Split results from start_example to + max_examples
    # Send next start_example if necessary
    end_example = start_example + MAX_EXAMPLES_TO_SEND

    def get_inferences_resp():
      sliced_infer_objs = [
        copy.deepcopy(infer_obj) for infer_obj in self.infer_objs]
      if request.args.get('model_type') == 'classification':
        for obj in sliced_infer_objs:
          obj['classificationResult']['classifications'][:] = obj[
            'classificationResult']['classifications'][
              start_example:end_example]
      else:
        for obj in sliced_infer_objs:
          obj['regressionResult']['regressions'][:] = obj['regressionResult'][
            'regressions'][start_example:end_example]
      return {'indices': self.indices_to_infer[start_example:end_example],
              'results': sliced_infer_objs}

    def get_extra_outputs_resp():
      sliced_extra_objs = [
        copy.deepcopy(infer_obj) for infer_obj in self.extra_outputs]
      for obj in sliced_extra_objs:
        if obj is not None:
          for key in obj:
            obj[key][:] = obj[key][start_example:end_example]
      return sliced_extra_objs

    try:
      inferences_resp = get_inferences_resp()
      extra_outputs_resp = get_extra_outputs_resp()
      resp = {'inferences': json.dumps(inferences_resp),
              'extraOutputs': json.dumps(extra_outputs_resp)}
      if end_example >= len(self.examples):
        end_example = -1
      if start_example == 0:
        resp['vocab'] = json.dumps(label_vocab)
      resp['next'] = end_example
      return http_util.Respond(request, resp, 'application/json')
    except Exception as e:
      logging.error(e)
      return http_util.Respond(request, str(e),
                               'application/json', code=400)

  @wrappers.Request.application
  def _eligible_features_from_example_handler(self, request):
    """Returns a list of JSON objects for each feature in the example.

    Args:
      request: A request for features.

    Returns:
      A list with a JSON object for each feature.
      Numeric features are represented as {name: observedMin: observedMax:}.
      Categorical features are repesented as {name: samples:[]}.
    """
    features_list = inference_utils.get_eligible_features(
      self.examples[0: NUM_EXAMPLES_TO_SCAN], NUM_MUTANTS)
    return http_util.Respond(request, features_list, 'application/json')

  @wrappers.Request.application
  def _sort_eligible_features_handler(self, request):
    """Returns a sorted list of JSON objects for each feature in the example.

    The list is sorted by interestingness in terms of the resulting change in
    inference values across feature values, for partial dependence plots.

    Args:
      request: A request for sorted features.

    Returns:
      A sorted list with a JSON object for each feature.
      Numeric features are represented as
      {name: observedMin: observedMax: interestingness:}.
      Categorical features are repesented as
      {name: samples:[] interestingness:}.
    """
    try:
      features_list = inference_utils.get_eligible_features(
          self.examples[0: NUM_EXAMPLES_TO_SCAN], NUM_MUTANTS)
      example_index = int(request.args.get('example_index', '0'))
      (inference_addresses, model_names, model_versions,
          model_signatures) = self._parse_request_arguments(request)
      chart_data = {}
      for feat in features_list:
        chart_data[feat['name']] = self._infer_mutants_impl(
          feat['name'], example_index,
          inference_addresses, model_names, request.args.get('model_type'),
          model_versions, model_signatures,
          request.args.get('use_predict') == 'true',
          request.args.get('predict_input_tensor'),
          request.args.get('predict_output_tensor'),
          feat['observedMin'] if 'observedMin' in feat else 0,
          feat['observedMax'] if 'observedMin' in feat else 0,
          None, custom_predict_fn=self.custom_predict_fn)
      features_list = inference_utils.sort_eligible_features(
        features_list, chart_data)
      return http_util.Respond(request, features_list, 'application/json')
    except common_utils.InvalidUserInputError as e:
      return http_util.Respond(request, e.message,
                               'application/json', code=400)
    except Exception as e:
      return http_util.Respond(request, str(e),
                               'application/json', code=400)

  @wrappers.Request.application
  def _infer_mutants_handler(self, request):
    """Returns JSON for the partial dependence plots for a feature.

    Args:
      request: A request that should contain 'feature_name', 'example_index',
         'inference_address', 'model_name', 'model_type', 'model_version', and
         'model_signature'.

    Returns:
      A list of JSON objects, one for each chart.
    """
    try:
      if request.method != 'GET':
        logger.error('%s requests are forbidden.', request.method)
        return http_util.Respond(request, 'invalid non-GET request',
                                 'application/json', code=405)

      example_index = int(request.args.get('example_index', '0'))
      feature_name = request.args.get('feature_name')
      (inference_addresses, model_names, model_versions,
          model_signatures) = self._parse_request_arguments(request)
      json_mapping = self._infer_mutants_impl(feature_name, example_index,
          inference_addresses, model_names, request.args.get('model_type'),
          model_versions, model_signatures,
          request.args.get('use_predict') == 'true',
          request.args.get('predict_input_tensor'),
          request.args.get('predict_output_tensor'),
          request.args.get('x_min'), request.args.get('x_max'),
          request.args.get('feature_index_pattern'),
          custom_predict_fn=self.custom_predict_fn)
      return http_util.Respond(request, json_mapping, 'application/json')
    except common_utils.InvalidUserInputError as e:
      return http_util.Respond(request, e.message,
                               'application/json', code=400)
    except Exception as e:
      return http_util.Respond(request, str(e),
                               'application/json', code=400)

  def _infer_mutants_impl(self, feature_name, example_index, inference_addresses,
      model_names, model_type, model_versions, model_signatures, use_predict,
      predict_input_tensor, predict_output_tensor, x_min, x_max,
      feature_index_pattern, custom_predict_fn):
    """Helper for generating PD plots for a feature."""
    examples = (self.examples if example_index == -1
                else [self.examples[example_index]])
    serving_bundles = []
    for model_num in xrange(len(inference_addresses)):
      serving_bundles.append(inference_utils.ServingBundle(
          inference_addresses[model_num],
          model_names[model_num],
          model_type,
          model_versions[model_num],
          model_signatures[model_num],
          use_predict,
          predict_input_tensor,
          predict_output_tensor,
          custom_predict_fn=custom_predict_fn))

    viz_params = inference_utils.VizParams(
        x_min, x_max,
        self.examples[0:NUM_EXAMPLES_TO_SCAN], NUM_MUTANTS,
        feature_index_pattern)
    return inference_utils.mutant_charts_for_feature(
        examples, feature_name, serving_bundles, viz_params)
