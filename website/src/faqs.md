---
title: WIT - FAQs
layout: layouts/sub.liquid

hero-height: 125
hero-image: /assets/images/banner-faqs.png
hero-title: "Frequently Asked Questions"

sub-nav: '<a href="https://github.com/pair-code/what-if-tool/issues/new" target="_blank">Ask a question</a>'
color: "#8A2A04"
---

<div class="mdl-cell--8-col mdl-cell--8-col-tablet mdl-cell--4-col-phone">

{% include partials/faq-element 
  f-title: "Where do I go to report a bug in the What-If Tool?", 
  f-copy: "

Submit bugs, ask questions, suggest content, and request features on our [Github issues list](https://github.com/pair-code/what-if-tool/issues/new)." %}

{% include partials/faq-element 
  f-title: "How many datapoints can the What-If Tool handle?", 
  f-copy: "

The number of datapoints depends on the size of the individual datapoints themselves. 
Some factors that impact the number of datapoints that can be handled are the per-page memory limit of web browsers and the front-end for simultaneous visualization.

For datapoints that contain tabular data or short text segments, the What-If Tool can handle tens of thousands of points. For datapoints that contain encoded images, the tool can only handle a few hundred datapoints, with the exact number depending on the size of the images.
" %}

{% include partials/faq-element 
    f-title: "What kinds of models can the What-If Tool handle?", 
    f-copy: "
    
The What-If Tool can work with any python-accessible model in Notebook environments, and will work with most models hosted by TF-serving in Tensorboard.

The What-If Tool supports:

* binary classification*
* multi-class classification
* regression tasks

\* Fairness optimization strategies are available only with binary classification models due to the nature of the strategies themselves." %}

{% include partials/faq-element 
  f-title: "Why is the What-If Tool loading so slowly?", 
  f-copy: "
  
The What-If Tool runs entirely in the browser, and may therefore load slowly for a variety of reasons. Some known causes are:

* if a loaded dataset has a high number of features
* if each data point in the loaded dataset is large in size (eg. large images)
* the model takes a long time to return predictions " %}

{% include partials/faq-element 
  f-title: "How can I share my scatter plot or ROC curve or confusion matrix with my team?", 
  f-copy: "
  
For now, there is no export feature in WIT. We recommend taking a screenshot and annotating it using a simple graphic editor tool. Alternatively, you can create a Colab, Jupyter or Cloud AI notebook with your analysis and share it with your peers. " %}

{% include partials/faq-element 
    f-title: "How are counterfactuals calculated?", 
    f-copy: "
    
In the What-If Tool, Counterfactuals are datapoints that are most similar to a selected datapoint, but are classified differently by a model. 

For binary classification models, counterfactuals are the most similar datapoint to a selected datapoint that is predicted in the opposite class or label by a model.

For regression models, counterfactuals are calculated when the difference in prediction score between the selected datapoint and a candidate counterfactual is equal or greater to the “counterfactual threshold”. The counterfactual threshold default is set to the standard deviation of the prediction values and can be adjusted by the user.

For multi-class models, the counterfactual is the most similar datapoint to a selected datapoint, but is classified as any class other than the selected datapoint’s class.

Read [this tutorial](/learn/tutorials/counterfactuals/) for more information. 

By default, features that are fully unique across the dataset (such as encoded images and long text strings) are ignored for this distance calculation. However, it is possible to define your own custom distance between datapoints by specifying it as a custom distance function when loading the What-If Tool in a notebook, as seen in [this example](https://colab.sandbox.google.com/github/pair-code/what-if-tool/blob/master/WIT_Toxicity_Text_Model_Comparison.ipynb#scrollTo=lVaMyc45HWwD).

Further reading: Wachter, S., Mittelstadt, B., & Russell, C. (2017). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. <br/>
[https://arxiv.org/abs/1711.00399](https://arxiv.org/abs/1711.00399)" %}


{% include partials/faq-element 
  f-title: "I have proprietary data. Is WIT secure for my team to use?", 
  f-copy: "
  
WIT uses pre-trained models and runs entirely in the browser. We don't store, collect or share datasets loaded into the What-If Tool. If using the tool inside TensorBoard, then access to that TensorBoard instance can be controlled through the authorized_groups command-line flag to TensorBoard. Anyone with access to the TensorBoard instance will be able to see data from the datasets that the instance has permissions to load from disk. If using WIT inside of colab, access to the data is controlled by the colab kernel, outside the scope of WIT. " %}


{% include partials/faq-element 
  f-title: "What are some examples of features people have added in the datapoint editor?", 
  f-copy: "
  
The What-If Tool uses trained models to investigate prediction results on uploaded dataset, and models do not learn anything from edits or injunctions in the What-If Tool. Therefore, any new features added to the datapoint editor has no bearing on the model itself. Users typically add new features to:

* describe or annotate datapoints using features that are irrelevant to the model
* see if there are any trends or correlations that might make a feature useful to include when training another iteration of the model outside of the What-If Tool.

 " %}

{% include partials/faq-element 
  f-title: "Can I use WIT with LIME or SHAP?", 
  f-copy: "
  
Yes! The What-If Tool supports feature attributions in notebook mode. You can use any feature attribution method, including LIME, SHAP, integrated gradients, and SmoothGrad, in your own custom predict function. Return these attributions along with the predictions for use in your analysis with the What-If Tool. See this [demo](https://colab.research.google.com/github/PAIR-code/what-if-tool/blob/master/WIT_COMPAS_with_SHAP.ipynb). " %}


{% include partials/faq-element 
  f-title: "Where can I find out more about the What-If Tool?", 
  f-copy: "
  
Read our systems paper submitted to IEEE VAST 2019 available at [https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8807255](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8807255):
Wexler, James, Mahima Pushkarna, Tolga Bolukbasi, Martin Wattenberg, Fernanda Viégas, and Jimbo Wilson. "The What-If Tool: Interactive probing of machine learning models." IEEE transactions on visualization and computer graphics 26, no. 1 (2019): 56-65.
 " %}

</div>
