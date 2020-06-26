---
title: WIT - Explore
layout: layouts/sub.liquid

hero-image: /assets/images/banner-explore.png
hero-title: "Take the What-If Tool for a spin!"
hero-copy: "Get a feel for the What-If Tool in a variety of demos in the browser or in notebook environments."

sub-nav: '<a href="#web">Web demos</a><a href="#notebook">Notebook demos</a><a href="#cloud-ai">Cloud AI models</a>'
color: "#FFFFFF"
---

<div class="mdl-cell--8-col mdl-cell--8-col-tablet mdl-cell--4-col-phone">

<a name="web"></a>

## Web demos

Play with the What-If Tool on a pre-loaded trained model and dataset right in the browser.

  <div class="mdl-grid no-padding">

  {% include partials/demo-card c-title: "Compare income classification on UCI census data", link: "/demos/uci.html", 
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income",
  c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "binary classification, model comparison", external:"true" %}

  {% include partials/demo-card c-title: "Explore age-prediction regression on UCI census data", link: "/demos/age.html",
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income", c-copy: "Explore the performance of a regression model which predicts a person's age from their census information. Slice your dataset to evaluate performance metrics such as aggregated inference error measures for each subgroup. Explore feature attributions calculated by vanilla gradients.", tags: "regression, attributions", external:"true" %}

  {% include partials/demo-card c-title: "Explore celebrity face image smile classification", link: "/demos/image.html",
  c-data-source: "CelebA Data Set", c-data-source-url:  "http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html", c-copy: "Predict whether an image contains a smiling face using this binary classification model on the CelebA dataset. Can you identify which group was missing from the training data, resulting in a biased model?", tags: "binary classification, image recognition", external:"true" %}

  {% include partials/demo-card c-title: "Explore flower image classification", link: "/demos/iris.html",
    c-data-source: "UCI Iris Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/iris", c-copy: "This multi-class classification model predicts the species of iris flowers from sepal and petal measurements. Look for correlations between different features and flower types.", tags: "mutli-class classification", external:"true" %}

  {% include partials/demo-card c-title: "Investigate fairness on recidivism classification", link: "/demos/compas.html",
  c-data-source: "COMPAS Dataset", c-data-source-url: "https://www.kaggle.com/danofer/compass", c-copy: "Inspired by Propublica, investigate fairness using this classifier that mimics the behavior of the COMPAS recidivism classifier. Trained on the COMPAS dataset, this model determines if a person belongs in the "Low" risk (negative) or "Medium or High" risk (positive) class for recidivism according to COMPAS.", tags: "binary classification", external:"true" %}

  </div>

  {% include partials/spacer height:30 %}

<a name="notebook"></a>

## Notebook Demos

Explore the What-If Tool’s interpretability features in utmost detail in Colaboratory, Jupyter and Cloud AI Notebooks.  

  <div class="mdl-grid no-padding">

  {% include partials/demo-card c-title: "Compare income classification on UCI census data", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb",
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income", c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "binary classification, model comparison", external:"true" %}

  {% include partials/demo-card c-title: "Explore age-prediction regression on UCI census data", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Age_Regression.ipynb", 
  c-data-source: "UCI Census Income Dataset", c-data-source-url: "http://archive.ics.uci.edu/ml/datasets/Census+Income", c-copy: "Explore the performance of a regression model which predicts a person's age from their census information. Slice your dataset to evaluate performance metrics such as aggregated inference error measures for each subgroup.", tags: "regression", external:"true" %}

  {% include partials/demo-card c-title: "Explore celebrity face image smile classification", link: "https://colab.research.google.com/github/PAIR-code/what-if-tool/blob/master/WIT_Smile_Detector.ipynb", 
  c-data-source: "CelebA Dataset", c-data-source-url:  "http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html", c-copy: "Predict whether an image contains a smiling face using this binary classification model on the CelebA dataset. Can you identify which group was missing from the training data, resulting in a biased model?", tags: "binary classification, image recognition, keras model, custom distance", external:"true" %}

  {% include partials/demo-card c-title: "Investigate fairness on recidivism classification", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS.ipynb",
   c-data-source: "COMPAS Dataset", c-data-source-url: "https://www.kaggle.com/danofer/compass", c-copy: "Inspired by Propublica, investigate fairness using this classifier that mimics the behavior of the COMPAS recidivism classifier. Trained on the COMPAS dataset, this model determines if a person belongs in the "Low" risk (negative) or "Medium or High" risk (positive) class for recidivism according to COMPAS.", tags: "binary classification", external:"true" %}

  {% include partials/demo-card c-title: "Investigate fairness on recidivism classification with attributions", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS_with_SHAP.ipynb",
   c-data-source: "COMPAS Dataset", c-data-source-url: "https://www.kaggle.com/danofer/compass", c-copy: "A version of the COMPAS notebook demo, using the SHAP library to get feature attributions for each prediction.", tags: "binary classification, attributions, keras model", external:"true" %}

  {% include partials/demo-card c-title: "Text toxicity classifiers", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Toxicity_Text_Model_Comparison.ipynb",
  c-data-source: "Wikpedia Comments Dataset", c-data-source-url: "https://figshare.com/articles/Wikipedia_Talk_Labels_Toxicity/4563973", c-copy: "Use the What-If Tool to compare two pre-trained models from ConversationAI that determine sentence toxicity, one of which was trained on a more balanced dataset. Examine their performance side-by-side on the Wikipedia Comments dataset. These are keras models which do not use TensorFlow examples as an input format.", tags: "binary classification, model comparison, keras model, custom distance", external:"true" %}

  </div>

<a name="cloud-ai"></a>

## Google Cloud AI models

Use the What-If Tool with Cloud AI models, and in conjunction with Explainable AI.

  <div class="mdl-grid no-padding">


  {% include partials/demo-card c-title: "Mortgage classification with AI Platform", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip.ipynb",
  c-data-source: "Home Mortgage Disclosure Act Dataset", c-data-source-url: "https://www.ffiec.gov/hmda/hmdaflat.htm", c-copy: "Explore a mortgage classification model that has been deployed on Cloud AI Platform. This model was created with the XGBoost platform and not TensorFlow.", tags: "binary classification, cloud ai platform", external:"true" %}

  {% include partials/demo-card c-title: "Training a mortgage classification model with AI Platform", link: "https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip_e2e.ipynb",
  c-data-source: "Home Mortgage Disclosure Act Dataset", c-data-source-url: "https://www.ffiec.gov/hmda/hmdaflat.htm", c-copy: "Train a mortgage classification model with XGBoost, deploy it to Cloud AI Platform, and use the What-If Tool to analyze it. This demo requires a Google Cloud Platform account.", tags: "binary classification, cloud ai platform, xgboost model", external:"true" %}

  {% include partials/demo-card c-title: "Training and comparing wine quality models with AI Platform", link: "https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/keras_sklearn_compare_caip_e2e.ipynb",
  c-data-source: "UCI Wine Quality Dataset", c-data-source-url: "https://archive.ics.uci.edu/ml/datasets/wine+quality", c-copy: "Train both a scikit-learn and keras model to predict wine quality and deploy them to Cloud AI Platform. Then use the What-If Tool to compare the two models. This demo requires a Google Cloud Platform account.", tags: "regression, model comparison, cloud ai platform, keras model, scikit-learn model", external:"true" %}
  </div>

{% include partials/spacer height:50 %}