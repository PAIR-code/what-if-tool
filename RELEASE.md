# What-If Tool releases

## Release 1.5.1

This is the first release made from the source code since it was moved into
the pair-code/what-if-tool repository. This release ensures WitWidget will
work in the upcoming Chrome version 80, which removes HTML import support.

### Notable Bug Fixes
- #30 - Remove link element usage from notebook mode.

## Release 1.5.0

This release is the first official release with support for attribution
value display in the What-If Tool. This includes support for Cloud AI
Platform models that return attribution values through their explain endpoint.

### Notable Features
- #2882 - Cloud AI Platform attribution updates.
- #2909 - Attribution display improvements.
- #2897 - Update regression demo with attributions.

### Notable Bug Fixes
- #2901 - Fix JupyterHub widget display error.
- #2916 - WitWidget small fixes including PD plot range editing.

## Release 1.4.5

### Notable Bug Fixes
- #2846 - Fix an issue with setting examples in Jupyter notebooks.

## Release 1.4.4

### Notable Bug Fixes
- #2816 - Fix an issue with TFMA slicing callback.

## Release 1.4.3

### Notable Features
- #2787 - Add ml service name and version for CAIP.
- #2781 - Add callback creator for TFMA slicing usage.

### Notable Bug Fixes
- #2785 - Fix sliced intersection.

## Release 1.4.2

### Notable Features
- #2744 - Allow set_example to accept JSON.

### Notable Bug Fixes
- #2762 - Fix cloud model usage with JSON input.

## Release 1.4.1

Note that as of 1.4.1, if you provide a custom prediction function, and provide
your examples to WitConfigBuilder as JSON (not Example protos), then the
examples will be passed to your custom predict function in that JSON format.
This is technically a breaking API change but the existing behavior was
incorrect and this specific configuration is so rarely used that we wanted
to correct it immediately without any need for special code/flags.

### Notable Features
- #2716 - Better custom predict fn when provided JSON input.

### Notable Bug Fixes
- #2716 - Fix fairness threshold setting bug introduced in 1.4.0.

## Release 1.4.0

### Notable Features
- #2607 - Add ability to set custom distance function for counterfactuals and distance
  visualizations.
- #2461 - Add ability to sort PD plots by interestingness.
- #2660 - Add ability to consume arbitrary prediction-time information.
- #2678 - Can now slice by numeric features in Performance & Fairness tab.
- #2647 - Add counterfactual analysis for regression models.
- #2663 - Visual updates for displaying attributions.
- #2630 - Added developers guide documentation.
- #2698 - Add ability to adjust attributions.

### Notable Bug Fixes
- #2682 - Fix issue with threshold sliders not updating on fairness button presses.
- #2669 - Fix PD plots in python3.
- #2648 - Fix image handling broken from Polymer 2 update.
