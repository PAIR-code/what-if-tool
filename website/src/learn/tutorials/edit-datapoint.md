---
title: How To - Edit a Datapoint
layout: layouts/tutorial.liquid

hero-image: /assets/images/sample-banner.png
hero-title: "Edit a Datapoint"
hero-copy: "How To - Edit a Datapoint"

bc-anchor-category: "basics"
bc-category-title: "Basics of the What-If Tool"
bc-title: "Edit a Datapoint"

time: "5 minutes"
use-with: "Classification models<br/>Multi-class models<br/>Regression models"
before: "N/A"
related: "Binary Classification Model: UCI Census Income Prediction<br/><br/>Multi-class Classification Model: Flowers Species Identification<br/><br/>Regression Model: UCI Census Age Prediction"
takeaways: "Learn to edit a datapoint.<br/><br/>Get model predictions on an edited datapoint."
questions: "How does the prediction result on a datapoint change if a feature value is changed?<br/><br/>How do models behave when feature values are missing?"
---

## How To - Edit a Datapoint

This article describes the steps to edit a datapoint in the What-If Tool. 

1. **Select a data point** of interest in the custom *Datapoints* visualization by clicking on it. A list of all features and values associated with that datapoint will appear in the *Edit* module.

{% include partials/inset-image image: '/assets/images/EditDatapoint.gif', 
  caption: 'Above: Editing a data point.'%}

2. **To change a feature value**, click on it. This should highlight the value with a yellow stroke around it.

3. **To delete a feature value**, click on it to highlight. Then click on the delete icon to delete the feature value.

{% include partials/info-box title: 'Deleting a feature value', 
  text: 'Deleting a feature value can be tricky business. Missing feature values can cause some models to behave erroneously, unless they are set up to handle missing feature values.'%}

4. **To get model predictions**, click on the *Predict* button in the *Infer* module. This is known as a *Run*. Additionally, clicking the predict button will return predictions for multiple edited data points in a batch run. Until a prediction is available, any prediction-related features utilized in the Datapoint visualization are removed from the datapoint.

{% include partials/inset-image image: '/assets/images/EditBatchDatapoint.gif', 
  caption: 'Above: Editing three data points and then clicking the Predict button returns predictions for all three data points simultaneously. Edited data points are colored grey and displayed at inference score = 0 in the Datapoints visualization until predicted, indicating that there are no model predictions available for it.'%}

5. **To restore an edited datapoint** to its original values, click on the revert icon in the toolbar in the *Edit* module, and then click on the predict button in the *Infer* module to return model predictions. 

6. **To duplicate a selected datapoint**, click on the duplicate icon in the toolbar. A new instance of the datapoint should be added to the *Datapoints* visualization. Click on the predict button in the *Infer* module to return model predictions.

{% include partials/info-box title: 'Tracking edited data points', 
  text: 'The unique datapoint identity in the heading of the *Edit* module is handy when tracking an edited datapoint when working with a large dataset. The *Infer* module displays prediction results for all runs associated with a datapoint, highlighting the difference between two consecutive runs. However, it isn’t possible to save this information outside of the What-If Tool. '%}
