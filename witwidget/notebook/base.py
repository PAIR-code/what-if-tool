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

import base64
import json
import googleapiclient.discovery
import os
import logging
import multiprocessing
import tensorflow as tf
from IPython import display
from google.protobuf import json_format
from numbers import Number
from oauth2client.client import GoogleCredentials
import google_auth
from google.oauth2 import service_account
from six import ensure_str
from six import integer_types
from utils import inference_utils

import google.cloud.aiplatform_v1
import google.cloud.aiplatform_v1beta1
from typing import Dict

from google.cloud import aiplatform
from google.cloud import aiplatform.gapic
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

# Constants used in mutant inference generation.
NUM_MUTANTS_TO_GENERATE = 10
NUM_EXAMPLES_FOR_MUTANT_ANALYSIS = 50

# Custom user agents for tracking number of calls to Cloud AI Platform
# and Vertex AI.
USER_AGENT_FOR_CAIP_TRACKING = 'WhatIfTool'
USER_AGENT_FOR_VERTEX_AI_TRACKING = 'WhatIfTool'

try:
  POOL_SIZE = max(multiprocessing.cpu_count() - 1, 1)
except Exception:
  POOL_SIZE = 1


class WitWidgetBase(object):
  """WIT widget base class for common code between Jupyter and Colab."""

  def __init__(self, config_builder):
    """Constructor for WitWidgetBase.

    Args:
      config_builder: WitConfigBuilder object containing settings for WIT.
    """
    tf.get_logger().setLevel(logging.WARNING)
    config = config_builder.build()
    copied_config = dict(config)
    self.estimator_and_spec = (
      dict(config.get('estimator_and_spec'))
      if 'estimator_and_spec' in config else {})
    self.compare_estimator_and_spec = (
      dict(config.get('compare_estimator_and_spec'))
      if 'compare_estimator_and_spec' in config else {})
    if 'estimator_and_spec' in copied_config:
      del copied_config['estimator_and_spec']
    if 'compare_estimator_and_spec' in copied_config:
      del copied_config['compare_estimator_and_spec']

    self.custom_predict_fn = config.get('custom_predict_fn')
    self.compare_custom_predict_fn = config.get('compare_custom_predict_fn')
    self.custom_distance_fn = config.get('custom_distance_fn')
    self.adjust_prediction_fn = config.get('adjust_prediction')
    self.compare_adjust_prediction_fn = config.get('compare_adjust_prediction')
    self.adjust_example_fn = config.get('adjust_example')
    self.compare_adjust_example_fn = config.get('compare_adjust_example')
    self.adjust_attribution_fn = config.get('adjust_attribution')
    self.compare_adjust_attribution_fn = config.get('compare_adjust_attribution')

    if 'custom_predict_fn' in copied_config:
      del copied_config['custom_predict_fn']
    if 'compare_custom_predict_fn' in copied_config:
      del copied_config['compare_custom_predict_fn']
    if 'custom_distance_fn' in copied_config:
      del copied_config['custom_distance_fn']
      copied_config['uses_custom_distance_fn'] = True
    if 'adjust_prediction' in copied_config:
      del copied_config['adjust_prediction']
    if 'compare_adjust_prediction' in copied_config:
      del copied_config['compare_adjust_prediction']
    if 'adjust_example' in copied_config:
      del copied_config['adjust_example']
    if 'compare_adjust_example' in copied_config:
      del copied_config['compare_adjust_example']
    if 'adjust_attribution' in copied_config:
      del copied_config['adjust_attribution']
    if 'compare_adjust_attribution' in copied_config:
      del copied_config['compare_adjust_attribution']

    examples = copied_config.pop('examples')
    self.config = copied_config
    self.set_examples(examples)

    # This tracks whether mutant inference is running in order to
    # skip calling for explanations for CAIP models when inferring
    # for mutant inference, for performance reasons.
    self.running_mutant_infer = False

    # If using AI Platform for prediction, set the correct custom prediction
    # functions.
    if self.config.get('use_aip'):
      self.custom_predict_fn = self._predict_aip_model
    if self.config.get('compare_use_aip'):
      self.compare_custom_predict_fn = self._predict_aip_compare_model

    # If using JSON input (not Example protos) and a custom predict
    # function, then convert examples to JSON before sending to the
    # custom predict function.
    if self.config.get('uses_json_input'):
      if self.custom_predict_fn is not None and not self.config.get('use_aip'):
        user_predict = self.custom_predict_fn
        def wrapped_custom_predict_fn(examples):
          return user_predict(self._json_from_tf_examples(examples))
        self.custom_predict_fn = wrapped_custom_predict_fn
      if (self.compare_custom_predict_fn is not None and
          not self.config.get('compare_use_aip')):
        compare_user_predict = self.compare_custom_predict_fn
        def wrapped_compare_custom_predict_fn(examples):
          return compare_user_predict(self._json_from_tf_examples(examples))
        self.compare_custom_predict_fn = wrapped_compare_custom_predict_fn

  def _get_element_html(self):
    return """
      <link rel="import" href="/nbextensions/wit-widget/wit_jupyter.html">"""

  def set_examples(self, examples):
    """Sets the examples shown in WIT.

    The examples are initially set by the examples specified in the config
    builder during construction. This method can change which examples WIT
    displays.
    """
    if self.config.get('uses_json_input'):
      tf_examples = self._json_to_tf_examples(examples)
      self.examples = [json_format.MessageToJson(ex) for ex in tf_examples]
    else:
      self.examples = [json_format.MessageToJson(ex) for ex in examples]
    self.updated_example_indices = set(range(len(examples)))

  def compute_custom_distance_impl(self, index, params=None):
    exs_for_distance = [
        self.json_to_proto(example) for example in self.examples]
    selected_ex = exs_for_distance[index]
    return self.custom_distance_fn(selected_ex, exs_for_distance, params)

  def json_to_proto(self, json):
    ex = (tf.train.SequenceExample()
          if self.config.get('are_sequence_examples')
          else tf.train.Example())
    json_format.Parse(json, ex)
    return ex

  def infer_impl(self):
    """Performs inference on examples that require inference."""
    indices_to_infer = sorted(self.updated_example_indices)
    examples_to_infer = [
        self.json_to_proto(self.examples[index]) for index in indices_to_infer]
    infer_objs = []
    extra_output_objs = []
    serving_bundle = inference_utils.ServingBundle(
      self.config.get('inference_address'),
      self.config.get('model_name'),
      self.config.get('model_type'),
      self.config.get('model_version'),
      self.config.get('model_signature'),
      self.config.get('uses_predict_api'),
      self.config.get('predict_input_tensor'),
      self.config.get('predict_output_tensor'),
      self.estimator_and_spec.get('estimator'),
      self.estimator_and_spec.get('feature_spec'),
      self.custom_predict_fn)
    (predictions, extra_output) = (
      inference_utils.run_inference_for_inference_results(
        examples_to_infer, serving_bundle))
    infer_objs.append(predictions)
    extra_output_objs.append(extra_output)
    if ('inference_address_2' in self.config or
        self.compare_estimator_and_spec.get('estimator') or
        self.compare_custom_predict_fn):
      serving_bundle = inference_utils.ServingBundle(
        self.config.get('inference_address_2'),
        self.config.get('model_name_2'),
        self.config.get('model_type'),
        self.config.get('model_version_2'),
        self.config.get('model_signature_2'),
        self.config.get('uses_predict_api'),
        self.config.get('predict_input_tensor'),
        self.config.get('predict_output_tensor'),
        self.compare_estimator_and_spec.get('estimator'),
        self.compare_estimator_and_spec.get('feature_spec'),
        self.compare_custom_predict_fn)
      (predictions, extra_output) = (
        inference_utils.run_inference_for_inference_results(
          examples_to_infer, serving_bundle))
      infer_objs.append(predictions)
      extra_output_objs.append(extra_output)
    self.updated_example_indices = set()
    return {
      'inferences': {'indices': indices_to_infer, 'results': infer_objs},
      'label_vocab': self.config.get('label_vocab'),
      'extra_outputs': extra_output_objs}

  def infer_mutants_impl(self, info):
    """Performs mutant inference on specified examples."""
    example_index = int(info['example_index'])
    feature_name = info['feature_name']
    examples = (self.examples if example_index == -1
                else [self.examples[example_index]])
    examples = [self.json_to_proto(ex) for ex in examples]
    scan_examples = [self.json_to_proto(ex) for ex in self.examples[0:50]]
    serving_bundles = []
    serving_bundles.append(inference_utils.ServingBundle(
      self.config.get('inference_address'),
      self.config.get('model_name'),
      self.config.get('model_type'),
      self.config.get('model_version'),
      self.config.get('model_signature'),
      self.config.get('uses_predict_api'),
      self.config.get('predict_input_tensor'),
      self.config.get('predict_output_tensor'),
      self.estimator_and_spec.get('estimator'),
      self.estimator_and_spec.get('feature_spec'),
      self.custom_predict_fn))
    if ('inference_address_2' in self.config or
        self.compare_estimator_and_spec.get('estimator') or
        self.compare_custom_predict_fn):
      serving_bundles.append(inference_utils.ServingBundle(
        self.config.get('inference_address_2'),
        self.config.get('model_name_2'),
        self.config.get('model_type'),
        self.config.get('model_version_2'),
        self.config.get('model_signature_2'),
        self.config.get('uses_predict_api'),
        self.config.get('predict_input_tensor'),
        self.config.get('predict_output_tensor'),
        self.compare_estimator_and_spec.get('estimator'),
        self.compare_estimator_and_spec.get('feature_spec'),
        self.compare_custom_predict_fn))
    viz_params = inference_utils.VizParams(
      info['x_min'], info['x_max'],
      scan_examples, 10,
      info['feature_index_pattern'])
    self.running_mutant_infer = True
    charts = inference_utils.mutant_charts_for_feature(
      examples, feature_name, serving_bundles, viz_params)
    self.running_mutant_infer = False
    return charts

  def get_eligible_features_impl(self):
    """Returns information about features eligible for mutant inference."""
    examples = [self.json_to_proto(ex) for ex in self.examples[
      0:NUM_EXAMPLES_FOR_MUTANT_ANALYSIS]]
    return inference_utils.get_eligible_features(
      examples, NUM_MUTANTS_TO_GENERATE)

  def sort_eligible_features_impl(self, info):
    """Returns sorted list of interesting features for mutant inference."""
    features_list = info['features']
    chart_data = {}
    for feat in features_list:
      chart_data[feat['name']] = self.infer_mutants_impl({
        'x_min': feat['observedMin'] if 'observedMin' in feat else 0,
        'x_max': feat['observedMax'] if 'observedMin' in feat else 0,
        'feature_index_pattern': None,
        'feature_name': feat['name'],
        'example_index': info['example_index'],
      })
    return inference_utils.sort_eligible_features(
      features_list, chart_data)

  def create_sprite(self):
    """Returns an encoded image of thumbnails for image examples."""
    # Generate a sprite image for the examples if the examples contain the
    # standard encoded image feature.
    if not self.examples:
      return None
    example_to_check = self.json_to_proto(self.examples[0])
    feature_list = (example_to_check.context.feature
                    if self.config.get('are_sequence_examples')
                    else example_to_check.features.feature)
    if 'image/encoded' in feature_list:
      example_strings = [
        self.json_to_proto(ex).SerializeToString()
        for ex in self.examples]
      encoded = ensure_str(base64.b64encode(
        inference_utils.create_sprite_image(example_strings)))
      return 'data:image/png;base64,{}'.format(encoded)
    else:
      return None

  def _json_from_tf_examples(self, tf_examples):
    json_exs = []
    feature_names = self.config.get('feature_names')
    for ex in tf_examples:
      # Create a JSON list or dict for each example depending on settings.
      # Strip out any explicitly-labeled target feature from the example.
      # This is needed because AI Platform models that accept JSON cannot handle
      # when non-input features are provided as part of the object to run
      # prediction on.
      if self.config.get('uses_json_list'):
        json_ex = []
        for feat in ex.features.feature:
          if feature_names and feat in feature_names:
            feat_idx = feature_names.index(feat)
          else:
            feat_idx = int(feat)
          if (feat == self.config.get('target_feature') or
              feat_idx == self.config.get('target_feature')):
            continue
          # Ensure the example value list is long enough to add the next feature
          # from the tf.Example.
          if feat_idx >= len(json_ex):
            json_ex.extend([None] * (feat_idx - len(json_ex) + 1))
          if ex.features.feature[feat].HasField('int64_list'):
            json_ex[feat_idx] = ex.features.feature[feat].int64_list.value[0]
          elif ex.features.feature[feat].HasField('float_list'):
            json_ex[feat_idx] = ex.features.feature[feat].float_list.value[0]
          else:
            json_ex[feat_idx] = ensure_str(
              ex.features.feature[feat].bytes_list.value[0])
      else:
        json_ex = {}
        for feat in ex.features.feature:
          if feat == self.config.get('target_feature'):
            continue
          if ex.features.feature[feat].HasField('int64_list'):
            json_ex[feat] = ex.features.feature[feat].int64_list.value[0]
          elif ex.features.feature[feat].HasField('float_list'):
            json_ex[feat] = ex.features.feature[feat].float_list.value[0]
          else:
            json_ex[feat] = ensure_str(
              ex.features.feature[feat].bytes_list.value[0])
      json_exs.append(json_ex)
    return json_exs

  def _json_to_tf_examples(self, examples):
    def add_single_feature(feat, value, ex):
      if isinstance(value, integer_types):
        ex.features.feature[feat].int64_list.value.append(value)
      elif isinstance(value, Number):
        ex.features.feature[feat].float_list.value.append(value)
      else:
        ex.features.feature[feat].bytes_list.value.append(value.encode('utf-8'))

    tf_examples = []
    for json_ex in examples:
      ex = tf.train.Example()
      # JSON examples can be lists of values (for xgboost models for instance),
      # or dicts of key/value pairs.
      if self.config.get('uses_json_list'):
        feature_names = self.config.get('feature_names')
        for (i, value) in enumerate(json_ex):
          # If feature names have been provided, use those feature names instead
          # of list indices for feature name when storing as tf.Example.
          if feature_names and len(feature_names) > i:
            feat = feature_names[i]
          else:
            feat = str(i)
          add_single_feature(feat, value, ex)
        tf_examples.append(ex)
      else:
        for feat in json_ex:
          add_single_feature(feat, json_ex[feat], ex)
        tf_examples.append(ex)
    return tf_examples

  def _predict_aip_model(self, examples):
    return self._predict_aip_impl(
      examples,
      self.config.get('inference_address'),
      self.config.get('model_name'),
      self.config.get('model_signature'),
      self.config.get('force_json_input'),
      self.adjust_example_fn,
      self.adjust_prediction_fn,
      self.adjust_attribution_fn,
      self.config.get('aip_service_name'),
      self.config.get('aip_service_version'),
      self.config.get('get_explanations'),
      self.config.get('aip_batch_size'),
      self.config.get('aip_api_key'))

  def _predict_aip_compare_model(self, examples):
    return self._predict_aip_impl(
      examples,
      self.config.get('inference_address_2'),
      self.config.get('model_name_2'),
      self.config.get('model_signature_2'),
      self.config.get('compare_force_json_input'),
      self.compare_adjust_example_fn,
      self.compare_adjust_prediction_fn,
      self.compare_adjust_attribution_fn,
      self.config.get('compare_aip_service_name'),
      self.config.get('compare_aip_service_version'),
      self.config.get('compare_get_explanations'),
      self.config.get('compare_aip_batch_size'),
      self.config.get('compare_aip_api_key'))

  def _predict_aip_impl(self, examples, project, model, version, force_json,
                        adjust_example, adjust_prediction, adjust_attribution,
                        service_name, service_version, get_explanations,
                        batch_size, api_key):
    """Custom prediction function for running inference through AI Platform."""

    # Set up environment for GCP call for specified project.
    os.environ['GOOGLE_CLOUD_PROJECT'] = project

    should_explain = get_explanations and not self.running_mutant_infer

    def predict(exs):
      """Run prediction on a list of examples and return results."""
      # Properly package the examples to send for prediction.
      discovery_url = None
      error_during_prediction = False
      if api_key is not None:
        discovery_url = (
          ('https://%s.googleapis.com/$discovery/rest'
           '?labels=GOOGLE_INTERNAL&key=%s&version=%s')
          % (service_name, api_key, 'v1'))
        credentials = GoogleCredentials.get_application_default()
        service = googleapiclient.discovery.build(
          service_name, service_version, cache_discovery=False,
          developerKey=api_key, discoveryServiceUrl=discovery_url,
          credentials=credentials)
      else:
        service = googleapiclient.discovery.build(
          service_name, service_version, cache_discovery=False)

      name = 'projects/{}/models/{}'.format(project, model)
      if version is not None:
        name += '/versions/{}'.format(version)

      if self.config.get('uses_json_input') or force_json:
        examples_for_predict = self._json_from_tf_examples(exs)
      else:
        examples_for_predict = [{'b64': base64.b64encode(
          example.SerializeToString()).decode('utf-8') }
          for example in exs]

      # If there is a user-specified input example adjustment to make, make it.
      if adjust_example:
        examples_for_predict = [
          adjust_example(ex) for ex in examples_for_predict]

      # Send request, including custom user-agent for tracking.
      request_builder = service.projects().predict(
          name=name,
          body={'instances': examples_for_predict}
      )
      user_agent = request_builder.headers.get('user-agent')
      request_builder.headers['user-agent'] = (
        USER_AGENT_FOR_CAIP_TRACKING +
        ('-' + user_agent if user_agent else ''))
      try:
        response = request_builder.execute()
      except Exception as e:
        error_during_prediction = True
        response = {'error': str(e)}

      # Get the attributions and baseline score if explaination is enabled.
      if should_explain and not error_during_prediction:
        try:
          request_builder = service.projects().explain(
            name=name,
            body={'instances': examples_for_predict}
          )
          request_builder.headers['user-agent'] = (
            USER_AGENT_FOR_CAIP_TRACKING +
            ('-' + user_agent if user_agent else ''))
          explain_response = request_builder.execute()
          explanations = ([explain['attributions_by_label'][0]['attributions']
              for explain in explain_response['explanations']])
          baseline_scores = []
          for i, explain in enumerate(explanations):
            baseline_scores.append(
              explain_response['explanations'][i][
                'attributions_by_label'][0]['baseline_score'])
          response.update(
            {'explanations': explanations, 'baseline_scores': baseline_scores})
        except Exception as e:
          pass
      return response

    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
          yield l[i:i + n]

    # Run prediction in batches in threads.
    if batch_size is None:
      batch_size = len(examples)
    batched_examples = list(chunks(examples, batch_size))

    pool = multiprocessing.pool.ThreadPool(processes=POOL_SIZE)
    responses = pool.map(predict, batched_examples)
    pool.close()
    pool.join()

    for response in responses:
      if 'error' in response:
        raise RuntimeError(response['error'])

    # Parse the results from the responses and return them.
    all_predictions = []
    all_baseline_scores = []
    all_attributions = []

    for response in responses:
      if 'explanations' in response:
        # If an attribution adjustment function was provided, use it to adjust
        # the attributions.
        if adjust_attribution is not None:
          all_attributions.extend([
            adjust_attribution(attr) for attr in response['explanations']])
        else:
          all_attributions.extend(response['explanations'])

      if 'baseline_scores' in response:
        all_baseline_scores.extend(response['baseline_scores'])

      # Use the specified key if one is provided.
      key_to_use = self.config.get('predict_output_tensor')

      for pred in response['predictions']:
        # If the prediction contains a key to fetch the prediction, use it.
        if isinstance(pred, dict):
          if key_to_use is None:
            # If the dictionary only contains one key, use it.
            returned_keys = list(pred.keys())
            if len(returned_keys) == 1:
              key_to_use = returned_keys[0]
            # Use a default key if necessary.
            elif self.config.get('model_type') == 'classification':
              key_to_use = 'probabilities'
            else:
              key_to_use = 'outputs'

          if key_to_use not in pred:
            raise KeyError(
              '"%s" not found in model predictions dictionary' % key_to_use)

          pred = pred[key_to_use]

        # If the model is regression and the response is a list, extract the
        # score by taking the first element.
        if (self.config.get('model_type') == 'regression' and
            isinstance(pred, list)):
          pred = pred[0]

        # If an prediction adjustment function was provided, use it to adjust
        # the prediction.
        if adjust_prediction:
          pred = adjust_prediction(pred)

        # If the model is classification and the response is a single number,
        # treat that as the positive class score for a binary classification
        # and convert it into a list of those two class scores. WIT only
        # accepts lists of class scores as results from classification models.
        if (self.config.get('model_type') == 'classification'):
          if not isinstance(pred, list):
            pred = [pred]
          if len(pred) == 1:
            pred = [1 - pred[0], pred[0]]

        all_predictions.append(pred)

    results = {'predictions': all_predictions}
    if all_attributions:
      results.update({'attributions': all_attributions})
    if all_baseline_scores:
      results.update({'baseline_score': all_baseline_scores})
    return results

  def create_selection_callback(self, examples, max_examples):
    """Returns an example selection callback for use with TFMA.

    The returned function can be provided as an event handler for a TFMA
    visualization to dynamically load examples matching a selected slice into
    WIT.

    Args:
      examples: A list of tf.Examples to filter and use with WIT.
      max_examples: The maximum number of examples to create.
    """
    def handle_selection(selected):
      def extract_values(feat):
        if feat.HasField('bytes_list'):
          return [v.decode('utf-8') for v in feat.bytes_list.value]
        elif feat.HasField('int64_list'):
          return feat.int64_list.value
        elif feat.HasField('float_list'):
          return feat.float_list.value
        return None

      filtered_examples = []
      for ex in examples:
        if selected['sliceName'] == 'Overall':
          filtered_examples.append(ex)
        else:
          values = extract_values(ex.features.feature[selected['sliceName']])
          if selected['sliceValue'] in values:
            filtered_examples.append(ex)
        if len(filtered_examples) == max_examples:
          break

      self.set_examples(filtered_examples)
    return handle_selection

# service_region is required here
  def _predict_vertex_ai_model(self, examples):
    return self._predict_vertex_ai_impl(
      examples,
      self.config.get('inference_address'),
      self.config.get('model_name'),
      self.config.get('model_signature'),
      self.config.get('force_json_input'),
      self.adjust_example_fn,
      self.adjust_prediction_fn,
      self.adjust_attribution_fn,
      self.config.get('aip_service_region'),
      self.config.get('aip_service_name'),
      self.config.get('aip_service_version'),
      self.config.get('get_explanations'),
      self.config.get('aip_batch_size'),
      self.config.get('aip_api_key'))


  def _predict_vertex_ai_compare_model(self, examples):
    return self._predict_vertex_ai_impl(
      examples,
      self.config.get('inference_address_2'),
      self.config.get('model_name_2'),
      self.config.get('model_signature_2'),
      self.config.get('compare_force_json_input'),
      self.compare_adjust_example_fn,
      self.compare_adjust_prediction_fn,
      self.compare_adjust_attribution_fn,
      self.config.get('compare_aip_service_region'), # Does this exist yet?
      self.config.get('compare_aip_service_name'),
      self.config.get('compare_aip_service_version'),
      self.config.get('compare_get_explanations'),
      self.config.get('compare_aip_batch_size'),
      self.config.get('compare_aip_api_key'))


  def _predict_vertex_ai_impl(self, examples, project, model, endpoint,
                        force_json, adjust_example, adjust_prediction,
                        adjust_attribution, service_region, service_name,
                        service_version, get_explanations, batch_size, api_key):
    """Custom prediction function for running inference through Vertex AI."""

    # Set up environment for GCP call for specified project.
    os.environ['GOOGLE_CLOUD_PROJECT'] = project

    should_explain = get_explanations and not self.running_mutant_infer

    # Regional endpoint for prediction
    # For example, "us-central1-prediction-aiplatform.googleapis.com"
    api_endpoint = (
      ('%s-prediction-aiplatform.googleapis.com')
      % (service_region))

    def predict_vertex(exs):
      service_url = None
      error_during_prediction = False
      if api_key is not None: # Use provided api_key
        # Create Credentials object
        credentials = GoogleCredentials.get_application_default()
        # Update credentials to use google_auth library
        # credentials, proj = google.auth.default()
      else: # Just build the service
        client_options = {"api_endpoint": api_endpoint}
        # Initialize client that will be used to create and send requests.
        # This client only needs to be created once, and can be reused for multiple requests.
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

      # Preprocessing prediction examples
      if self.config.get('uses_json_input') or force_json:
        examples_for_predict = self._json_from_tf_examples(exs)
      else:
        examples_for_predict = [{'b64': base64.b64encode(
          example.SerializeToString()).decode('utf-8') }
          for example in exs]

      # If there is a user-specified input example adjustment to make, make it.
      if adjust_example:
        examples_for_predict = [
          adjust_example(ex) for ex in examples_for_predict]

      # Send request and send user agent for tracking
      endpoint = client.endpoint_path(
          project=project, location=service_region, endpoint=endpoint
      )
      parameters_dict = {}
      parameters = json_format.ParseDict(parameters_dict, Value())
      request_builder = client.predict(
          endpoint=endpoint, instances=examples_for_predict, parameters=parameters
      )
      user_agent = request_builder.headers.get('user-agent')
      request_builder.headers['user-agent'] = (
         USER_AGENT_FOR_VERTEX_AI_TRACKING +
         ('-' + user_agent if user_agent else ''))
      try:
        response = request_builder.execute()
      except Exception as e:
        error_during_prediction = True
        response = {'error': str(e)}

      if should_explain and not error_during_prediction:
        try:
          request_builder = service.projects().explain(
            name=name,
            body={'instances': examples_for_predict}
          )
          request_builder.headers['user-agent'] = (
            USER_AGENT_FOR_CAIP_TRACKING +
            ('-' + user_agent if user_agent else ''))
          explain_response = request_builder.execute()
          explanations = explain_response.explanations
          # Get a list of all the feature attributions from the explain response
          attributions = [explanation.attributions for explanation in explanations]
          baseline_scores = []
          for i, explain in enumerate(explanations):
            # Maybe use attribution.baseline_output_value
            baseline_scores.append(
              explain_response['explanations'][i][
                'attributions_by_label'][0]['baseline_score'])
          response.update(
            {'explanations': attributions, 'baseline_scores': baseline_scores})
        except Exception as e:
          pass
      return response

    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
          yield l[i:i + n]

    # Run prediction in batches in threads.
    if batch_size is None:
      batch_size = len(examples)
    batched_examples = list(chunks(examples, batch_size))

    pool = multiprocessing.pool.ThreadPool(processes=POOL_SIZE)
    responses = pool.map(predict, batched_examples)
    pool.close()
    pool.join()

    for response in responses:
      if 'error' in response:
        raise RuntimeError(response['error'])

    # Parse the results from the responses and return them.
    all_predictions = []
    all_baseline_scores = []
    all_attributions = []

    for response in responses:
      if 'explanations' in response:
        # If an attribution adjustment function was provided, use it to adjust
        # the attributions.
        if adjust_attribution is not None:
          all_attributions.extend([
            adjust_attribution(attr) for attr in response['explanations']])
        else:
          all_attributions.extend(response['explanations'])

      if 'baseline_scores' in response:
        all_baseline_scores.extend(response['baseline_scores'])

      # Use the specified key if one is provided.
      key_to_use = self.config.get('predict_output_tensor')

      for pred in response['predictions']:
        # If the prediction contains a key to fetch the prediction, use it.
        if isinstance(pred, dict):
          if key_to_use is None:
            # If the dictionary only contains one key, use it.
            returned_keys = list(pred.keys())
            if len(returned_keys) == 1:
              key_to_use = returned_keys[0]
            # Use a default key if necessary.
            elif self.config.get('model_type') == 'classification':
              key_to_use = 'probabilities'
            else:
              key_to_use = 'outputs'

          if key_to_use not in pred:
            raise KeyError(
              '"%s" not found in model predictions dictionary' % key_to_use)

          pred = pred[key_to_use]

        # If the model is regression and the response is a list, extract the
        # score by taking the first element.
        if (self.config.get('model_type') == 'regression' and
            isinstance(pred, list)):
          pred = pred[0]

        # If an prediction adjustment function was provided, use it to adjust
        # the prediction.
        if adjust_prediction:
          pred = adjust_prediction(pred)

        # If the model is classification and the response is a single number,
        # treat that as the positive class score for a binary classification
        # and convert it into a list of those two class scores. WIT only
        # accepts lists of class scores as results from classification models.
        if (self.config.get('model_type') == 'classification'):
          if not isinstance(pred, list):
            pred = [pred]
          if len(pred) == 1:
            pred = [1 - pred[0], pred[0]]

        all_predictions.append(pred)

    results = {'predictions': all_predictions}
    if all_attributions:
      results.update({'attributions': all_attributions})
    if all_baseline_scores:
      results.update({'baseline_score': all_baseline_scores})
    return results
