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

import math
import ipywidgets as widgets
import tensorflow as tf
from IPython.core.display import display, HTML
from ipywidgets import Layout
from traitlets import Dict
from traitlets import Int
from traitlets import List
from traitlets import observe
from traitlets import Unicode
from traitlets import Set
from witwidget.notebook import base


@widgets.register
class WitWidget(widgets.DOMWidget, base.WitWidgetBase):
  """WIT widget for Jupyter."""
  _view_name = Unicode('WITView').tag(sync=True)
  _view_module = Unicode('wit-widget').tag(sync=True)
  _view_module_version = Unicode('^0.1.0').tag(sync=True)

  # Traitlets for communicating between python and javascript.
  config = Dict(dict()).tag(sync=True)
  # Examples and inferences are not synced directly because large datasets cause 
  # websocket issues. Instead, we indirectly update them through batch updates.
  examples = List([])
  frontend_ready = Int(0).tag(sync=True)
  examples_batch = List([]).tag(sync=True)
  examples_batch_id = Int(0).tag(sync=True)
  inferences = Dict(dict())
  inferences_batch = Dict(dict()).tag(sync=True)
  inferences_batch_id = Int(0).tag(sync=True)
  infer = Int(0).tag(sync=True)
  infer_counter = Int(0)
  update_example = Dict(dict()).tag(sync=True)
  delete_example = Dict(dict()).tag(sync=True)
  duplicate_example = Dict(dict()).tag(sync=True)
  updated_example_indices = Set(set())
  get_eligible_features = Int(0).tag(sync=True)
  sort_eligible_features = Dict(dict()).tag(sync=True)
  eligible_features = List([]).tag(sync=True)
  infer_mutants = Dict(dict()).tag(sync=True)
  mutant_charts = Dict([]).tag(sync=True)
  mutant_charts_counter = Int(0)
  sprite = Unicode('').tag(sync=True)
  error = Dict(dict()).tag(sync=True)
  compute_custom_distance = Dict(dict()).tag(sync=True)
  custom_distance_dict = Dict(dict()).tag(sync=True)

  def __init__(self, config_builder, height=1000, delay_rendering=False):
    """Constructor for Jupyter notebook WitWidget.

    Args:
      config_builder: WitConfigBuilder object containing settings for WIT.
      height: Optional height in pixels for WIT to occupy. Defaults to 1000.
      delay_rendering. Optional. This argument is ignored in the Jupyter
      implementation but is included for API compatibility between Colab and
      Jupyter implementations. Rendering in Jupyter is always delayed until
      the render method is called or the WitWidget object is directly evaluated
      in a notebook cell.
    """
    self.transfer_block = False
    self.examples_generator = None
    self.inferences_generator = None
    # TODO(wit-dev) This should depend on the example size targeting less than
    # 10MB per batch to avoid websocket issues.
    self.batch_size = 10000

    widgets.DOMWidget.__init__(self, layout=Layout(height='%ipx' % height))
    base.WitWidgetBase.__init__(self, config_builder)
    self.error_counter = 0

    # Ensure the visualization takes all available width.
    display(HTML("<style>.container { width:100% !important; }</style>"))

  def render(self):
    """Render the widget to the display."""
    return self

  def set_examples(self, examples):
    if self.transfer_block:
      print('Cannot set examples while transfer is in progress.')
      return
    base.WitWidgetBase.set_examples(self, examples)
    self.examples_generator = self.generate_next_example_batch()
    # If this is called after frontend is ready this makes sure examples are
    # updated.
    self._start_examples_sync()
    self._generate_sprite()

  def generate_next_example_batch(self):
    n_examples = len(self.examples)
    n_batches = n_examples // self.batch_size
    batch_end = n_batches * self.batch_size
    num_remaining = n_batches + (batch_end!=n_examples)
    for i in range(n_batches):
      num_remaining -= 1
      yield self.examples[i*self.batch_size:(i+1)*self.batch_size], num_remaining
    if batch_end != n_examples:
      num_remaining -= 1
      yield self.examples[batch_end:], num_remaining

  def _report_error(self, err):
    self.error = {
      'msg': repr(err),
      'counter': self.error_counter
    }
    self.error_counter += 1

  def _start_examples_sync(self):
    if not self.frontend_ready or self.examples_generator is None or self.transfer_block:
      return
    # Send the first batch
    next_batch, self.examples_batch_id = next(self.examples_generator, ([], -1))
    self.transfer_block = True
    self.examples_batch = next_batch

  @observe('infer')
  def _infer(self, change):
    try:
      self.inferences = base.WitWidgetBase.infer_impl(self)
      self.inferences_generator = self.generate_next_inference_batch()
      self._start_inferences_sync()
    except Exception as e:
      self._report_error(e)

  def generate_next_inference_batch(self):
    # Parse out the inferences from the returned structure and empty the
    # structure of contents, keeping its nested structure.
    # Chunks of the inference results will be sent to the front-end and
    # re-assembled.
    indices = self.inferences['inferences']['indices'][:]
    self.inferences['inferences']['indices'] = []
    res2 = []
    extra = {}
    extra2 = {}
    model_inference = self.inferences['inferences']['results'][0]
    if ('extra_outputs' in self.inferences and len(self.inferences['extra_outputs']) and
        self.inferences['extra_outputs'][0]):
      for key in self.inferences['extra_outputs'][0]:
        extra[key] = self.inferences['extra_outputs'][0][key][:]
        self.inferences['extra_outputs'][0][key] = []
    if 'classificationResult' in model_inference:
      res = model_inference['classificationResult']['classifications'][:]
      model_inference['classificationResult']['classifications'] = []
    else:
      res = model_inference['regressionResult']['regressions'][:]
      model_inference['regressionResult']['regressions'] = []

    if len(self.inferences['inferences']['results']) > 1:
      if ('extra_outputs' in self.inferences and
          len(self.inferences['extra_outputs']) > 1 and
          self.inferences['extra_outputs'][1]):
        for key in self.inferences['extra_outputs'][1]:
          extra2[key] = self.inferences['extra_outputs'][1][key][:]
          self.inferences['extra_outputs'][1][key] = []
      model_2_inference = self.inferences['inferences']['results'][1]
      if 'classificationResult' in model_2_inference:
        res2 = model_2_inference['classificationResult']['classifications'][:]
        model_2_inference['classificationResult']['classifications'] = []
      else:
        res2 = model_2_inference['regressionResult']['regressions'][:]
        model_2_inference['regressionResult']['regressions'] = []

    num_pieces = math.ceil(len(indices) / self.batch_size)
    i = 0

    while num_pieces > 0:
      num_pieces -= 1

      piece = [res[i : i + self.batch_size]]
      extra_piece = [{}]
      for key in extra:
        extra_piece[0][key] = extra[key][i : i + self.batch_size]
      if res2:
        piece.append(res2[i : i + self.batch_size])
        extra_piece.append({})
        for key in extra2:
          extra_piece[1][key] = extra2[key][i : i + self.batch_size]
      ind_piece = indices[i : i + self.batch_size]
      data = {'results': piece, 'indices': ind_piece, 'extra': extra_piece,
              'counter': self.infer_counter}
      self.infer_counter += 1
      # For the first segment to send, also send the blank inferences
      # structure to be filled in. This was cleared of contents above but is
      # used to maintain the nested structure of the results.
      if i == 0:
        data['inferences'] = self.inferences
      i += self.batch_size
      yield data, num_pieces

  def _start_inferences_sync(self):
    if self.inferences_generator is None or self.transfer_block:
      return
    # Send the first batch
    next_batch, self.inferences_batch_id = next(
      self.inferences_generator, ({}, -1))
    self.transfer_block = True
    self.inferences_batch = next_batch

  # When frontend processes sent inferences, it updates batch id to request the
  # next batch
  @observe('inferences_batch_id')
  def _send_inferences_batch(self, change):
    if not self.transfer_block:
      return
    # Do not trigger at the end of a transfer.
    if self.inferences_batch_id < 0 or self.inferences_generator is None:
      self.transfer_block = False
      return
    self.inferences_batch, num_remaining = next(
      self.inferences_generator, ({}, -1))
    if num_remaining == 0:
      self.inferences_generator = None
      self.transfer_block = False

  # Finish setup items that require frontend to be ready.
  @observe('frontend_ready')
  def _finish_setup(self, change):
    # Start examples transfer
    self._start_examples_sync()

  # When frontend processes sent examples, it updates batch id to request the
  # next batch
  @observe('examples_batch_id')
  def _send_example_batch(self, change):
    if not self.transfer_block:
      return
    # Do not trigger at the end of a transfer.
    if self.examples_batch_id < 0 or self.examples_generator is None:
      self.transfer_block = False
      return
    self.examples_batch, num_remaining = next(self.examples_generator, ([], -1))
    if num_remaining == 0:
      self.examples_generator = None
      self.transfer_block = False

  # Observer callbacks for changes from javascript.
  @observe('get_eligible_features')
  def _get_eligible_features(self, change):
    features_list = base.WitWidgetBase.get_eligible_features_impl(self)
    self.eligible_features = features_list

  @observe('sort_eligible_features')
  def _sort_eligible_features(self, change):
    info = self.sort_eligible_features
    features_list = base.WitWidgetBase.sort_eligible_features_impl(self, info)
    self.eligible_features = features_list

  @observe('infer_mutants')
  def _infer_mutants(self, change):
    info = self.infer_mutants
    try:
      json_mapping = base.WitWidgetBase.infer_mutants_impl(self, info)
      json_mapping['counter'] = self.mutant_charts_counter
      self.mutant_charts_counter += 1
      self.mutant_charts = json_mapping
    except Exception as e:
      self._report_error(e)

  @observe('update_example')
  def _update_example(self, change):
    index = self.update_example['index']
    self.updated_example_indices.add(index)
    self.examples[index] = self.update_example['example']
    self._generate_sprite()

  @observe('duplicate_example')
  def _duplicate_example(self, change):
    self.examples.append(self.examples[self.duplicate_example['index']])
    self.updated_example_indices.add(len(self.examples) - 1)
    self._generate_sprite()

  @observe('delete_example')
  def _delete_example(self, change):
    index = self.delete_example['index']
    self.examples.pop(index)
    self.updated_example_indices = set([
        i if i < index else i - 1 for i in self.updated_example_indices])
    self._generate_sprite()

  @observe('compute_custom_distance')
  def _compute_custom_distance(self, change):
    info = self.compute_custom_distance
    index = info['index']
    params = info['params']
    callback_fn = info['callback']
    try:
      distances = base.WitWidgetBase.compute_custom_distance_impl(self, index,
                                                       params['distanceParams'])
      self.custom_distance_dict = {'distances': distances,
                                   'exInd': index,
                                   'funId': callback_fn,
                                   'params': params['callbackParams']}
    except Exception as e:
      self._report_error(e)

  def _generate_sprite(self):
    sprite = base.WitWidgetBase.create_sprite(self)
    if sprite is not None:
      self.sprite = sprite
