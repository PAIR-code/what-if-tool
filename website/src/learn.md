---
title: WIT - Learn
layout: layouts/sub.liquid

hero-height: 245
hero-image: /assets/images/banner-learn.png
hero-title: "Model probing for understandable, reliable, and fair machine learning"
hero-copy: "Learn how to explore feature sensitivity, compare model performance, and stress-test hypotheticals. "

sub-nav: '<a href="#basics">Basics of the What-If Tool</a><a href="#analysis">Conducting analysis</a><a href="#resources">Related resources & posts</a>'
color: "#8A2A04"
---

<div class="mdl-cell--8-col mdl-cell--8-col-tablet mdl-cell--4-col-phone">

<a name="basics"></a>

## Discover the basics

{% include partials/tutorial-link-element c-title: "A Tour of the What-If Tool", link: "/learn/tutorials/tour",
c-copy: "Learn about different spaces and how they are used in the What-If Tool: tabs, workspaces, modules and playgrounds." %}

{% include partials/tutorial-link-element c-title: "A Walkthrough with UCI Census Data", link: "/learn/tutorials/walkthrough/",
c-copy: "Explore how the What-If Tool can help us learn about a model and dataset through a concrete example." %}

{% include partials/tutorial-link-element c-title: "How To: Edit A Datapoint", link: "/learn/tutorials/edit-datapoint",
c-copy: "Learn how to edit a datapoint in the What-If Tool." %}

{% include partials/tutorial-link-element c-title: "How To: Find A Counterfactual", link: "/learn/tutorials/counterfactual",
c-copy: "Learn the steps to find a counterfactual to a datapoint in the What-If Tool." %}

{% include partials/tutorial-link-element c-title: "How To: Customize the Datapoints Visualization", link: "/learn/tutorials/customize-datapoints",
c-copy: "Learn how to customize visualizations from features in a loaded dataset using the Datapoints visualization." %}

{% include partials/tutorial-link-element c-title: "Features Overview: Understanding Your Feature Distributions", link: "/learn/tutorials/features-overview",
c-copy: "Explore the functionality of the Features Overview dashboard in the What-If Tool." %}

{% include partials/tutorial-link-element c-title: "Technical Setup: Getting Started in Tensorboard", link: "/learn/tutorials/tensorboard",
c-copy: "Set up the What-If Tool inside of TensorBoard." %}

{% include partials/tutorial-link-element c-title: "Technical Setup: Getting Started in Notebooks", link: "/learn/tutorials/notebooks",
c-copy: "Set up the What-If Tool inside of notebook environments." %}

{% include partials/spacer height:50 %}

<a name="analysis"></a>

## Conducting analysis in the What-If Tool

{% include partials/tutorial-link-element c-title: "Understanding Performance Metrics For Classifiers", link: "/learn/tutorials/classifier-performance",
c-copy: "A brief overview of performance metrics for classification-based models." %}

{% include partials/tutorial-link-element c-title: "Adding Non-Input Features To Perform Analysis", link: "/learn/tutorials/non-input-features",
c-copy: "Learn how to add non-input features into the What-If Tool to analyze subgroups." %}

{% include partials/tutorial-link-element c-title: "Exploring Features Overview To Identify Biases", link: "/learn/tutorials/features-overview-bias",
c-copy: "Explore datapoints in Features Overview to identify sources of bias." %}

{% include partials/spacer height:50 %}

<a name="resources"></a>

## Related resources and posts

  <div class="mdl-grid no-padding">

  {% include partials/resource-card c-title: "Qwiklabs Quest: Explore Machine Learning Models with Explainable AI.", link: "https://www.qwiklabs.com/quests/126?catalog_rank=%7B%22rank%22%3A1%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&search_id=6021667", c-copy: "Introductory level, hands-on practice with Explainable AI from Google Cloud.", cta-copy:"Launch Quest", external:"true" %}

  {% include partials/resource-card c-title: "Using the ‘What-If Tool’ to investigate Machine Learning models.", link: "https://towardsdatascience.com/using-what-if-tool-to-investigate-machine-learning-models-913c7d4118f", c-copy: "A community-contributed run-through of the features of the What-If Tool.", cta-copy:"Go to article", external:"true" %}

  {% include partials/resource-card c-title: "Introducing the What-If Tool", link: "https://www.youtube.com/playlist?list=PLIivdWyY5sqK7Z5A2-sftWLlbVSXuyclr", c-copy: "Get familiar with the What-If Tool with a three-part video series.", cta-copy:"Watch the videos", external:"true" %}

  {% include partials/resource-card c-title: "What if AI model understanding were easy?", link: "https://towardsdatascience.com/what-if-ai-model-understanding-were-easy-57ba21163d0e", c-copy: "See analytics-for-AI in action as Cassie Kozyrkov walks us through the What-If Tool.", cta-copy:"Go to article", external:"true" %}

  </div>

  {% include partials/spacer height:30 %}

</div>