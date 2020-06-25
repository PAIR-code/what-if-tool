---
title: Getting Started in Notebooks
layout: layouts/tutorial.liquid

hero-image: /assets/images/sample-banner.png
hero-title: "Notebooks"
hero-copy: "Getting Started in Notebooks"
---

# Getting Started in Notebooks

The What-If Tool can be used inside of notebook environments, including Colaboratory, Jupyter, JupyterLab, and Cloud AI Platform notebooks. The use of the What-If Tool in notebooks, as opposed to inside of TensorBoard, offers more flexibility due to the ability to add your own custom code for connecting the tool to your model(s) and data.

## Installation

The setup instructions for the What-If Tool differ slightly depending on which notebook environment you are in:

### Colaboratory
You need to install the witwidget package in a notebook cell before making use of it, by running the command `!pip install witwidget`.

### Jupyter
You need to install the witwidget package and enable the notebook extension in the environment where you launch your notebook kernels. This only needs to be done a single time for any Jupyter installation. Run the following commands on the command line, and then future launches of Jupyter notebooks will be able to use the tool:
```
pip install witwidget
jupyter nbextension install --py --symlink --sys-prefix witwidget
jupyter nbextension enable --py --sys-prefix witwidget
```

### JupyterLab
You need to install the witwidget package and enable the notebook extension inside of your notebook. Note, you may need to refresh the notebook page after running a cell containing these commands before the tool appears properly.
```
!pip install witwidget
!jupyter labextension install wit-widget
!jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Note that you may need to run `!sudo jupyter labextension …` commands depending on your notebook setup.

### Cloud AI Platform
AI Platform notebook instances launched with the TensorFlow backend come pre-installed with the What-If Tool. No installation steps are necessary.

The What-If Tool in notebook mode is invoked through the creation of a WitWidget object, with the configuration options set through use of a WitConfigBuilder object, which is provided to the WitWidget constructor.

After installation, the classes can be imported for use in a notebook through the import statement `from witwidget.notebook.visualization import WitWidget, WitConfigBuilder`. The list of all available configuration methods for WitConfigBuilder, along with method documentation can be found in the [source code](https://github.com/PAIR-code/what-if-tool/blob/master/witwidget/notebook/visualization.py).

## Loading Data

The dataset that the tool will use is specified by the list of data points you provide to the WitConfigBuilder constructor. These datapoints can be in a number of formats, depending on what the input to your model is. The datapoints will be sent in the provided format to the models (or custom prediction functions) you supply to the tool. The accepted formats are:
- tf.Example protocol buffers.
- tf.SequenceExample protocol buffers. In this case, be sure to call 
- Dictionary objects where the keys are feature names and the values are the feature values.
- Lists of feature values. In this case you can optionally also provide a list of strings as the column_names parameter that gives a display-friendly name to each list element for use in the tool.

All datapoints provided will be used by the tool, so be sure to sample your dataset down to a smaller list if you have a large dataset to test with. The number of datapoints the tool can handle is dependent on the size of each datapoint, but in general the tool can support on the order of 10,000 datapoints.

### Model Configuration

In notebook mode, the What-If Tool can support many different model configurations. The steps for setting up the tool for your specific situation depends on how your models will be queried by the tool but all involve calling methods on the WitConfigBuilder object which you will pass to the WitWidget constructor which creates the What-If Tool instance.

The What-If Tool defaults to assuming the model(s) are binary classification models. If using it for regression, call `set_model_type(“regression”`([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Age_Regression.ipynb)). If using it for multi-class classification, call `set_multi_class(True)`. In this case, you can set the maximum number of highest-scoring classes to display for each data point through the `set_max_classes_to_display` function.

For classification models, by default the classes are displayed as “class 0”, “class 1”, and so on. You can optionally give string labels to each class by providing a label vocabulary list through the `set_label_vocab` method, to provide a better experience to users trying to understand the model`s outputs. This method accepts a list of strings which has one entry for every class that the model can return. If you provide this list, the tool will display those user-friendly class names throughout, as opposed to the class indices ([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb)).

### TensorFlow Serving

Just as within TensorBoard, notebook mode can support models served by TensorFlow Serving. In this case, the address and port of the model server (as `[host]:[port]`) should be set through the `set_inference_address` method and the model name through the `set_model_name` method. 

You can optionally specify the model version, through `set_model_version`, and signature, through `set_model_signature`, if you need to query an older version of a model, or you need to query the non-default signature of the model.

If the served model uses the TensorFlow Serving Predict API (as opposed to the standard Classify or Regression APIs, then call `set_uses_predict_api(True)` and provide the names of the input and output tensors that the What-If Tool should use for sending data points to the model, and for parsing model results from the output of the model, through the `set_predict_input_tensor` and `set_predict_output_tensor` methods.

TensorFlow Estimators

TensorFlow Estimators are supported through the method `set_estimator_and_feature_spec` which requires an estimator object and the corresponding feature spec object, which contains the information on how to extract model inputs from the provided tf.Example protocol buffers ([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb)).

Cloud AI Platform Prediction

Models that have been deployed to Cloud AI Platform Prediction can be used in notebook mode through use of the `set_ai_platform_model` method, which has arguments for project name and model name. It also contains a large number of optional arguments that can be found in the code documentation, including ways to adjust the input datapoints before being sent to the served model, if necessary ([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip.ipynb)).

If the AI Platform model being served has [explanations](https://cloud.google.com/ai-platform/prediction/docs/ai-explanations/overview) enabled, then the returned attribution information will automatically be visualized by the What-If Tool, with no additional setup required.

Custom Prediction Functions

For models that don`t fit the above configurations, you can define your own custom prediction function, through the `set_custom_predict_fn` method which accepts a list of datapoints to send to the model and should return a list of predictions from the model, one for each datapoint provided. In this way, notebook mode supports any model that you can query through python code that you provide. Datapoints are provided as input to this function in the same format they were provided to the WitConfigBuilder object. For regression models, the returned list should contain a single score for each datapoint. For classification models, the returned list should contain a class score list for each datapoint. This class score list is a list of classification scores (between 0 and 1) for each class index that the model can classify, with the index in the list corresponding to the index of the class that the score represents ([example notebook](https://colab.research.google.com/github/PAIR-code/what-if-tool/blob/master/WIT_Smile_Detector.ipynb)).

Additionally, with custom prediction functions, the model can return more than just prediction scores. If you have a way to calculate feature attribution scores for each prediction (such as through SHAP or Integrated Gradients), those can be returned as well. To do this, instead of returning a list of scores from the custom prediction function, the function should return a dictionary, where the predictions list is stored under the key `predictions`, and the attributions are stored under the key `attributions`. The attributions should also be a list with one entry per datapoint. Each entry should be a dictionary with the keys being the names of the input features to the model (matching the features in the input data), and the values being the attribution scores for those features for the specific datapoint. For single-valued features (where each feature contains a single value as a number or string), the attribution should be a single number for that feature. For multi-valent features, such as can be specified in a tf.Example feature value list, the attribution for that feature should be a list with an attribution score for each feature value in the input datapoint ([example notebook](https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS_with_SHAP.ipynb)).

Lastly, custom prediction functions can return arbitrary prediction-time information for each datapoint. This can be useful in the case that you can calculate an additional metric per-datapoint at prediction time and wish to display it in the What-If Tool. One example of this could be a score calculated for each datapoint at prediction time for how similar each datapoint is to some anchor datapoint or concept, according to the internals of the model (see the TCAV paper for one example of such a metric). To do so, have the custom prediction function return a dictionary, where the predictions list is stored under the key `predictions`. Any other metric can be included by adding an additional key (this key will be used to display the metric) to the dictionary, and having its value be a list with one entry for each datapoint provided to the custom prediction function. The list entry should be a single number or string for display in the tool. Any returned metrics will be listed in the datapoint viewer in the Datapoint Editor workspace, and also usable for creating charts in the datapoints visualization, and for slicing datapoints in the Performance workspace.

## Model Comparison

In order to provide a second model to compare to the initial model, there are methods to set the model configuration for a second model. These methods follow the same naming convention as all of the methods mentioned above, except they begin with the prefix `set_compare_`, such as the methods `set_compare_inference_address` or `set_compare_custom_predict_function` ([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb)).

## Custom Distance Functions

As described in the counterfactual tutorial, the What-If Tool can use the distance between datapoints to calculate closest counterfactuals and to organize datapoints by similarity. The default way that distance between datapoints is calculated can be found in that tutorial. Providing a custom distance function can be valuable when the default behavior doesn’t correctly capture distance in a way you desire. One example is if your inputs contain either images or unique text strings in each datapoint, because in this case, the default distance behavior will ignore those unique features. In the case of images, you could imagine using distance between image embeddings (such as those that can be provided by modules at  tf.hub) as a way to calculate distance between image datapoints.

If you wish to calculate your own distance between datapoints, you can provide a function to do this through the `set_custom_distance_fn` method. The method you provide must take three arguments: an anchor datapoint to calculate distance from, and a list of datapoints to calculate the distance to, and an optionally parameters dictionary that is currently unused. It should return a list, the length of the number of destination datapoints, containing a distance to each of the provided destination datapoints from the provided anchor point. If you provide a custom distance function, the What-If Tool will automatically make use of it ([example notebook](https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Toxicity_Text_Model_Comparison.ipynb)).

## Displaying the Tool

To display the tool, pass the WitConfigBuilder object to the WitWidget constructor. There are two additional optional parameters to the constructor.

The first, height, is a numeric parameter, and sets the height of the displayed tool in pixels, and defaults to 1000.

The second, delay_rendering, is a boolean parameter that defaults to False. With this default of False, the What-If Tool is immediately displayed in the cell in which the WitWidget object is created. If set to True, then the What-If Tool is not displayed in the output of the notebook cell in which the WitWidget object is created. Instead, the widget is only displayed when you call the ‘render’ method on the constructed WitWidget object.

{% include partials/info-box title: 'Using the tool without a model', 
  text: 'You can use the What-If Tool without a served model, to just analyze a dataset. The dataset can even contain results from running a model offline, for use by the What-If Tool. In this case, since there is no model to query, some features of the tool, such as partial dependence plots, will be disabled. If the data points in the dataset contain a feature named “predictions”, the numbers in this feature will be interpreted by the tool as the results of a regression model. If they contain a feature named “predictions__probabilities”, the list of numbers in this feature will be interpreted as the results of a classification model, with the first entry being the score for class 0, the second entry being the score for class 1, and so on. If there are any features with the prefix “attributions__”, the numbers in those features will be interpreted as attribution scores for each corresponding input feature and will be used for the feature attribution-based capabilities of the What-If Tool. An example would be a feature named “attributions__age” containing attribution values for the input feature “age”.
'%}
