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
  # Examples are not synced directly because large datasets cause websocket
  # issues. Instead, we indirectly update it through example_batch.
  examples = List([])
  frontend_ready = Int(0).tag(sync=True)
  examples_batch = List([]).tag(sync=True)
  examples_batch_id = Int(0).tag(sync=True)
  inferences = Dict(dict()).tag(sync=True)
  infer = Int(0).tag(sync=True)
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
      implementation but is included for API compatability between Colab and
      Jupyter implementations. Rendering in Jupyter is always delayed until
      the render method is called or the WitWidget object is directly evaluated
      in a notebook cell.
    """
    self.examples_generator = None
    # TODO(wit-dev) This should depend on the example size targeting less than
    # 10MB per batch to avoid websocket issues.
    self.batch_size = 1000

    widgets.DOMWidget.__init__(self, layout=Layout(height='%ipx' % height))
    base.WitWidgetBase.__init__(self, config_builder)
    self.error_counter = 0

    # Ensure the visualization takes all available width.
    display(HTML("<style>.container { width:100% !important; }</style>"))

  def render(self):
    """Render the widget to the display."""
    return self

  def set_examples(self, examples):
    base.WitWidgetBase.set_examples(self, examples)
    self.examples_generator = self.generate_next_example_batch()
    # If this is called after frontend is ready this makes sure examples are
    # updated.
    self._start_examples_sync()
    print('child called')
    self._generate_sprite()

  def generate_next_example_batch(self):
    n_examples = len(self.examples)
    n_batches = n_examples // self.batch_size
    batch_end = n_batches * self.batch_size
    for i in range(n_batches):
      yield self.examples[i*self.batch_size:(i+1)*self.batch_size]
    if batch_end != n_examples:
      yield self.examples[batch_end:]

  def _report_error(self, err):
    self.error = {
      'msg': repr(err),
      'counter': self.error_counter
    }
    self.error_counter += 1

  def _start_examples_sync(self):
    print(self.frontend_ready)
    print(self.examples_generator)
    if not self.frontend_ready or self.examples_generator is None:
      return
    self.examples_batch_id = 0
    # Send the first batch
    self.examples_batch = next(self.examples_generator, [])

  @observe('infer')
  def _infer(self, change):
    try:
      self.inferences = base.WitWidgetBase.infer_impl(self)
    except Exception as e:
      self._report_error(e)

  # Finish setup items that require frontend to be ready.
  @observe('frontend_ready')
  def _finish_setup(self, change):
    # Start examples transfer
    print('finished setup')
    self._start_examples_sync()

  # When frontend processes sent examples, it updates batch id to request the
  # next batch
  @observe('examples_batch_id')
  def _send_example_batch(self, change):
    # Do not trigger at the end or beginning of a transfer.
    print('send example batch')
    if self.examples_batch_id <= 0 or self.examples_generator is None:
      print('returned from send example batch {} {}'.format(self.examples_batch_id, self.examples_generator is None))
      return
    next_batch = next(self.examples_generator, [])
    print(len(next_batch))
    if next_batch:
      self.examples_batch = next_batch
    else:
      # Tell frontend that we are done with the transfer
      self.examples_batch_id = -1
      self.examples_batch = []
      self.examples_generator = None

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
