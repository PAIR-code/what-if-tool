---
title: WIT - Getting Started
layout: layouts/sub.liquid

hero-image: /assets/images/banner-getting-started.png
hero-title: "pip install wit-widget"
hero-copy: "Use the What If Tool directly in your Notebooks, in TensorBoard, and with Cloud AI models."

sub-nav: '<a href="#notebooks">With notebooks</a><a href="#cloud-ai">With Google Cloud</a><a href="#tensorboard">On Tensorboard</a>'
color: "#FFFFFF"
---

<div class="mdl-cell--8-col mdl-cell--8-col-tablet mdl-cell--4-col-phone">

<a name="notebooks"></a>

## Model understanding in Notebooks

The What-If Tool is available as an extension in Jupyter, Colaboratory, and Cloud AI Platform notebooks. Use the What-If Tool to analyze classification or regression models on datapoints as inputs directly from within the notebook.
 
A custom prediction function can be used to load any model, and provide additional customizations to the What-If Tool, including feature attribution methods like SHAP, Integrated Gradients, or SmoothGrad.

{% include partials/link-to text:"See setup guide", link:"/learn/tutorials/notebooks/" %}

{% include partials/spacer height:30 %}

<div class="section-action">Explore</div>

### Notebooks

  <div class="mdl-grid no-padding">

  {% include partials/external-demo-card c-title: "Compare income classification on UCI census data", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb",
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income", c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "binary classification, model comparison", external:"true" %}

  {% include partials/external-demo-card c-title: "Text toxicity classifiers", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Toxicity_Text_Model_Comparison.ipynb",
  c-data-source: "Wikpedia Comments Dataset", c-data-source-url: "https://figshare.com/articles/Wikipedia_Talk_Labels_Toxicity/4563973", c-copy: "Use the What-If Tool to compare two pre-trained models from ConversationAI that determine sentence toxicity, one of which was trained on a more balanced dataset. Examine their performance side-by-side on the Wikipedia Comments dataset. These are keras models which do not use TensorFlow examples as an input format.", tags: "binary classification, model comparison, keras model, custom distance", external:"true" %}

  </div>

{% include partials/spacer height:50 %}

<a name="cloud-ai"></a>

## Easily explore Cloud AI model results

The What-If Tool can be easily configured to analyze AI Platform Prediction-hosted classification or regression models.

Use the What-If Tool to display and investigate attribution values for individual input features in relation to model predictions.

{% include partials/link-out text:"Visit Cloud AI", link:"https://cloud.google.com/ai-platform/prediction/docs/using-what-if-tool" %}

{% include partials/spacer height:30 %}

<div class="section-action">Explore</div>

### Notebooks

  <div class="mdl-grid no-padding">

  {% include partials/external-demo-card c-title: "Mortgage classification with AI Platform", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip.ipynb",
  c-data-source: "Home Mortgage Disclosure Act Dataset", c-data-source-url: "https://www.ffiec.gov/hmda/hmdaflat.htm", c-copy: "Explore a mortgage classification model that has been deployed on Cloud AI Platform. This model was created with the XGBoost platform and not TensorFlow.", tags: "binary classification, cloud ai platform", external:"true" %}

  {% include partials/external-demo-card c-title: "Training and comparing wine quality models with AI Platform", link: "https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/keras_sklearn_compare_caip_e2e.ipynb",
  c-data-source: "UCI Wine Quality Dataset", c-data-source-url: "https://archive.ics.uci.edu/ml/datasets/wine+quality", c-copy: "Train both a scikit-learn and keras model to predict wine quality and deploy them to Cloud AI Platform. Then use the What-If Tool to compare the two models. This demo requires a Google Cloud Platform account.", tags: "regression, model comparison, cloud ai platform, keras model, scikit-learn model", external:"true" %}

  </div>

{% include partials/spacer height:50 %}

<a name="tensorboard"></a>

## Use the What-If Tool in TensorBoard

Quickly explore your models in the What-If Tool from directly within TensorBoard, by providing the What-If Tool with a model server host and port, and a dataset for the model to perform predictions on.
 
The What-If Tool accepts a variety of data types. Upload data as tf.Examples, tf.SequenceExamples, or even a CSV file.

{% include partials/link-to text:"See setup guide", link:"/learn/tutorials/tensorboard/" %}

{% include partials/spacer height:30 %}

<div class="section-action">Explore</div>

### Web demos

  <div class="mdl-grid no-padding">

  {% include partials/demo-card c-title: "Compare income classification on UCI census data", link: "/demos/uci.html",
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income", c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "binary classification, model comparison", external:"true" %}

  {% include partials/demo-card c-title: "Explore celebrity face image smile classification", link: "/demos/image.html",
  c-data-source: "CelebA Dataset", c-data-source-url:  "http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html", c-copy: "Predict whether an image contains a smiling face using this binary classification model on the CelebA dataset. Can you identify which group was missing from the training data, resulting in a biased model?", tags: "binary classification, image recognition", external:"true" %}

  </div>

</div>