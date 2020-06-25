---
title: WIT - Explore
layout: layouts/sub.liquid

hero-image: /assets/images/sample-banner.png
hero-title: "Play with the What-If Tool"
hero-copy: "Vivamus dolor justo, consectetur sed ante in, lacinia porttitor tellus. Vestibulum neque leo, volutpat sit amet velit ut, laoreet maximus tortor. "
---

<div class="mdl-cell--8-col mdl-cell--4-col-tablet mdl-cell--4-col-phone">
  
## Web demos

These demos run directly in the browser. Just click and explore!

  <div class="mdl-grid no-padding">

  {% include partials/demo-card c-title: "Income Classification", link: "/demos/uci.html", c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Age Prediction", link: "/demos/age.html", c-copy: "Explore the performance of a regression model which predicts a person's age from their census information. Slice your dataset to evaluate performance metrics such as aggregated inference error measures for each subgroup. Explore feature attributions calculated by vanilla gradients.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Smile Detection", link: "/demos/images.html", c-copy: "Predict whether an image contains a smiling face using this binary classification model on the CelebA dataset. Can you identify which group was missing from the training data, resulting in a biased model?", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Flower Species Classification", link: "/demos/iris.html", c-copy: "This multi-class classification model predicts the species of iris flowers from sepal and petal measurements. Look for correlations between different features and flower types.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "COMPAS Recidivism Classifier", link: "/demos/compas.html", c-copy: "Inspired by Propublica, investigate fairness using this classifier that mimics the behavior of the COMPAS recidivism classifier. Trained on the COMPAS dataset, this model determines if a person belongs in the "Low" risk (negative) or "Medium or High" risk (positive) class for recidivism according to COMPAS.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  </div>

  {% include partials/spacer height:30 %}

## Notebook Demos

These notebook demos will open in Colaboratory. Just run the notebook cells to see the What-If Tool in action.

  <div class="mdl-grid no-padding">

  {% include partials/demo-card c-title: "Income Classification", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb", c-copy: "Compare two binary classification models that predict whether a person earns more than $50k a year, based on their census information. Examine how different features affect each models' prediction, in relation to each other.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Age Prediction", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Age_Regression.ipynb", c-copy: "Explore the performance of a regression model which predicts a person's age from their census information. Slice your dataset to evaluate performance metrics such as aggregated inference error measures for each subgroup.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Smile Detection", link: "https://colab.research.google.com/github/PAIR-code/what-if-tool/blob/master/WIT_Smile_Detector.ipynb", c-copy: "Predict whether an image contains a smiling face using this binary classification model on the CelebA dataset. Can you identify which group was missing from the training data, resulting in a biased model?", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "COMPAS Recidivism Classifier", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS.ipynb", c-copy: "Inspired by Propublica, investigate fairness using this classifier that mimics the behavior of the COMPAS recidivism classifier. Trained on the COMPAS dataset, this model determines if a person belongs in the "Low" risk (negative) or "Medium or High" risk (positive) class for recidivism according to COMPAS.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "COMPAS Recidivism Classifier with Attributions", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS_with_SHAP.ipynb", c-copy: "A version of the COMPAS notebook demo, using the SHAP library to get feature attributions for each prediction.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Text Toxicity Classifiers", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Toxicity_Text_Model_Comparison.ipynb", c-copy: "Use the What-If Tool to compare two pre-trained models from ConversationAI that determine sentence toxicity, one of which was trained on a more balanced dataset. Examine their performance side-by-side on the Wikipedia Comments dataset. These are keras models which do not use TensorFlow examples as an input format.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Mortgage Classification with AI Platform", link: "https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip.ipynb", c-copy: "Explore a mortgage classification model that has been deployed on Cloud AI Platform. This model was created with the XGBoost platform and not TensorFlow.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Training a Mortgage Classification Model with AI Platform", link: "https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/xgboost_caip_e2e.ipynb", c-copy: "Train a mortgage classification model with XGBoost, deploy it to Cloud AI Platform, and use the What-If Tool to analyze it. This demo requires a Google Cloud Platform account.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}

  {% include partials/demo-card c-title: "Training and Comparing Wine Quality Models with AI Platform", link: "https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/keras_sklearn_compare_caip_e2e.ipynb", c-copy: "Train both a scikit-learn and keras model to predict wine quality and deploy them to Cloud AI Platform. Then use the What-If Tool to compare the two models. This demo requires a Google Cloud Platform account.", tags: "<b>tacos</b> <b>burritos</b> <b>stuff</b>", external:"true" %}
  </div>

{% include partials/spacer height:50 %}