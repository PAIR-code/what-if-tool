---
title: What-If Tool
layout: layouts/main.liquid
---

<div class="mdl-cell--8-col mdl-cell--12-col-tablet mdl-cell--8-col-phone">

{% include partials/display1 text:"A visual probe to <strong>interactively inspect trained machine learning models</strong> with minimal code." %} 

{% include partials/home-cta-button text:"Get started", link:"/get-started" %}

{% include partials/spacer height:60 %}

</div>

![overview of WIT](/assets/images/home-hero.gif)

{% include partials/spacer height:60 %}

<div class="mdl-cell--8-col mdl-cell--12-col-tablet mdl-cell--8-col-phone">

A key challenge in developing and deploying responsible Machine Learning (ML) systems is understanding their performance across a wide range of inputs. 

Using WIT, you can test performance in hypothetical situations, analyze the importance of different data features, and visualize model behavior across multiple models and subsets of input data, and for different ML fairness metrics. 

</div>

{% include partials/spacer height:50 %}

{% include partials/display2 text:"Model probing, from within any workflow  " %}

<div class="mdl-grid no-padding">

{% include partials/one-of-three-column title:"Platforms and Integrations", text: "

[Colaboratory notebooks](https://colab.research.google.com/)

[Jupyter notebooks](https://jupyter.org/)

[Cloud AI Notebooks](https://cloud.google.com/ai-platform-notebooks)

[TensorBoard](https://www.tensorflow.org/tensorboard)

[TFMA Fairness Indicators](https://www.tensorflow.org/tfx/guide/fairness_indicators)

" %}
{% include partials/one-of-three-column title:"Compatible models<br/> and frameworks", text: "

TF Estimators

Models served by TF serving

Cloud AI Platform Models 

Models that can be wrapped in a python function

" %}
{% include partials/one-of-three-column title:"Supported data and task types", text: "

Binary classification

Multi-class classification

Regression

Tabular, Image, Text data

" %}

</div>

{% include partials/spacer height:50 %}

## Ask and answer questions about models, features, and datapoints [Set 1]

{% include partials/spacer height:200 %}

TODO (interactive section)

{% include partials/spacer height:200 %}

## Explore the What-If Tool

<div class="mdl-grid no-padding">
  {% include partials/home-card image: '/assets/images/sample-home-card.png', action: 'CODE', 
  title: 'Github', desc: 'The What-If Tool is open to anyone who wants to help develop and improve it!', 
  cta-text:"View developer guide", link: 'https://github.com/PAIR-code/what-if-tool', external:"true" %}
  
  {% include partials/home-card image: '/assets/images/sample-home-card.png', action: 'FAQs', 
  title: 'Got questions?', desc: 'Find answers to common questions about the What-If Tool.', 
  cta-text:"Browse our FAQs", link: '/faqs/' %}

  {% include partials/home-card image: '/assets/images/sample-home-card.png', action: 'RESEARCH', 
  title: 'Systems Paper at IEEE VAST ‘19', desc: 'Read about what went into the What-If Tool in our systems papers, presented at IEEE VAST ‘19.', 
  cta-text:"Go to proceedings", link: '#' external:"true" %}

  {% include partials/home-card image: '/assets/images/sample-home-card.png', action: 'ARTICLE', 
  title: 'Playing with AI Fairness', desc: "The What-If Tool lets you try on five different types of fairness. What do they mean?", 
  cta-text:"Read the article", link: '#' %}

</div>