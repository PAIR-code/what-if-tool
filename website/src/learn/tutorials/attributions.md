---
title: Exploring Attributions in the What-If Tool
layout: layouts/tutorial.liquid

hero-image: /assets/images/sample-banner.png
hero-title: "Exploring Attributions"
hero-copy: "Exploring Attributions in the What-If Tool"

bc-anchor-category: "analysis"
bc-category-title: "Conducting Analysis in the What-If Tool"
bc-title: "Exploring Attributions"

time: "15 minutes"
use-with: "Classification models<br/>Multi-class models<br/>Regression models"
before: "Have a trained model with logic that returns predictions and feature attributions and test dataset for analyzing."
related: "Regression Model: UCI Census Age Prediction"
takeaways: "Learn how to analyze feature attributions in the What-If Tool."
questions: "How do I view feature attributions in the What-If Tool?"
---

## Exploring Attributions in the What-If Tool

Exploring feature attributions is a great way to understand what features a model is relying on when making a prediction. Many techniques exist to get feature attributions from a model’s predictions, such as [LIME](https://christophm.github.io/interpretable-ml-book/lime.html), [integrated gradients](https://github.com/ankurtaly/Integrated-Gradients), and [shapley values](https://github.com/slundberg/shap). WIT allows users to consume feature attributions from any technique along with model predictions, and then uses those attributions to enhance its visualizations.

The feature attributions can be provided to WIT in one of two ways:
1. Through a Cloud AI Platform model that has [explanations](https://cloud.google.com/ai-platform/prediction/docs/ai-explanations/overview) enabled. Details on setting up WIT for a Cloud AI Platform model can be found in the [Getting Started in Notebooks tutorial](https://pair-code.github.io/what-if-tool/learn/tutorials/notebooks/).
2. Through a custom prediction function that returns feature attributions for each prediction, in addition to the standard prediction results. This can be done for WIT in either TensorBoard or notebooks. See the tutorial on [custom prediction functions](../custom-prediction) in WIT for details on how to set this up. The user defines how the attributions are calculated and WIT then takes those attributions and adds them to its visualizations.

### Attribution Visualizations

When attributions are returned along with predictions, new visualizations are enabled in WIT. When selecting a datapoint, the Datapoint Editor will do three things with the attribution information:
1. Features in the datapoint will be sorted by their attribution values, with the features with the highest attributions being at the top of the list. This sort order can be changed by a dropdown at the top of the Datapoint Editor.
2. The exact attribution values for each feature will be listed next to each feature value.
3. The feature values will have their background colored by their feature attribution scores, to allow at-a-glance understanding of the individual feature attributions.

{% include partials/inset-image image: '/assets/images/datapoint_attrs.png', 
  caption: 'Attribution values in the Datapoint Editor.'%}

Additionally, the feature attribution values can be used in the datapoints visualization, as a way to organize the datapoints, using those values to control scatter plot axes, datapoint binning, or datapoint coloring.

{% include partials/inset-image image: '/assets/images/attr-scatters.png', 
  caption: 'Exploring an age-prediction regression model. Scatter plots of age versus predicted age for a test dataset, faceted into two plots by how important the “hours per week” feature was to each prediction.'%}

In the “Performance” tab, in addition to the standard metrics that are calculated and shown, there will be a table of mean feature attributions across the entire dataset, sorted with the highest-attributed feature at the top. If you slice a dataset in this tab, each slice will have its own mean attributions table. This table uses the same color scale as the attribution value-based background colors in the Datapoint Editor. You can also use the feature attributions as a dimension to slice your dataset on in this tab, such as slicing the dataset into those with high attribution on a specific feature, versus those with low attribution on that feature, in order to compare the performance metrics on those two slices.

{% include partials/inset-image image: '/assets/images/mean_attrs.png', 
  caption: 'Mean attribution tables in the Performance tab for a regression model.'%}

### Attribution-based Counterfactuals

When attributions are provided to WIT, its counterfactual-generating capabilities are enhanced. In addition to being able to [find nearest counterfactuals through datapoint feature value similarity](../counterfactual), you can find nearest counterfactuals through attribution similarity. Switching to using attribution-based distance is controlled by a dropdown in the counterfactual controls area in the Vizualize module in the Datapoint Editor tab.

When finding nearest counterfactuals by attribution distance, WIT calculates the distance between two datapoints based on the difference in attribution values for each feature of a datapoint, instead of the difference in feature values. This gives you another way to explore the decision boundary of a model for a given datapoint, based purely on attributions from whatever methodology you are using to calculate feature-wise attributions.

{% include partials/inset-image image: '/assets/images/counterfactual-attr.png', 
  caption: 'Finding the closest counterfactual datapoint based on feature attributions as opposed to feature values.'%}
