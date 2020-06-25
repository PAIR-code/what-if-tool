---
title: How To - Find a Counterfactual
layout: layouts/tutorial.liquid

hero-image: /assets/images/sample-banner.png
hero-title: "Find a Counterfactual"
hero-copy: "How To - Find a Counterfactual"

bc-anchor-category: "basics"
bc-category-title: "Basics of the What-If Tool"
bc-title: "Find a Counterfactual"

time: "7 minutes"
use-with: "Classification models<br/>Multi-class models<br/>Regression models"
before: "N/A"
related: "Binary Classification Model: UCI Census Income Prediction<br/><br/>Multi-class Classification Model: Flowers Species Identification<br/><br/>Regression Model: UCI Census Age Prediction"
takeaways: "Learn to find a counterfactual for a datapoint.<br/><br/>Configure metrics and models used when calculating counterfactuals."
questions: "What needs to be different in a datapoint to be classified differently?<br/><br/>What differences between two data points cause models to behave differently?<br/><br/>Which two data points are most similar but have different classifications?"
---

## How To - Find a Counterfactual

The datapoint editor is dedicated to a variety of datapoint-level analyses, and visualizes individual data points in the loaded data set. One such functionality is the ability to find counterfactuals for a selected datapoint. In the What-If Tool, a *Counterfactual* is the most similar datapoint of a different classification (for classification models) or of a difference in prediction greater than a specified threshold (for regression models).

1. Select a data point of interest in the custom *Datapoints* visualization by clicking on it. A list of all features and values associated with that datapoint will appear in the Edit module.
   
2. In the *Visualize* module, turn on the counterfactual toggle by clicking on it:
  a. In the custom *Datapoints* visualization, the nearest counterfactual datapoint will be highlighted.
  b. In the *Edit* module, a list of feature values associated with the counterfactual will appear alongside the selected datapoint. Feature values that are different from the selected datapoint are displayed in green. 
  c. In the *Infer* module, the prediction values associated with the counterfactual are displayed alongside the selected datapoint. 

{% include partials/inset-image image: '/assets/images/Counterfactuals.gif', 
  caption: 'Above: Find different counterfactuals to a selected data point by model and distance.'%}

3. **Change the similarity metric**  by selecting from the options provided.
  a. You can select between L1 Norm distance and L2 Norm distance between data points. More information on how these distances are calculated will be included in a follow-on tutorial.
  b. When using the What-If Tool in notebook mode,  you can provide a custom distance metric to calculate distance between datapoints. In that case, it will be used instead of L1/L2 Norm to find the closest counterfactual.

4. **Change the model used for prediction results** for finding counterfactuals by selecting from the dropdown menu, if comparing multiple models.

{% include partials/inset-image image: '/assets/images/SimilarityFeature.gif', 
  caption: 'Above: Using the similarity modal to create a new similarity feature and use it in the Datapoints visualization.'%}

5. **In regression models, change the threshold value** using the counterfactual threshold slider. By default, the threshold for finding a counterfactual data point is set to the standard deviation of the prediction scores.

{% include partials/info-box title: 'Make a selected datapoint the center of your visualization', 
  text: 'You can evaluate how similar all data points are to a given selection by creating a similarity feature. Click on the “Create similarity feature” to open a window. Here you can rename this feature, decide which distance type to use, and directly apply it to the *Datapoints* visualization. This feature is particularly useful when you want to find clusters of data points that are near a data point of interest. '%}
