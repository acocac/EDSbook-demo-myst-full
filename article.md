---
# File metadata may be provided as frontmatter YAML
title: Learning the underlying physics of a simulation model of the ocean's temperature
subtitle: Computational Reproduction of "A Sensitivity Analysis of a Regression Model of Ocean Temperature" 
description: Computational Reproduction of "A Sensitivity Analysis of a Regression Model of Ocean Temperature" 
date: 2023-09-04
tags:
  - oceanography
  - interpretable-ML
  - model-sensitivity
thumbnail: images/la-palma-eruption-2022-paper.png
---

+++ {"part":"abstract"}

% The article should include an abstract block at the beginning. The block is delimited by `+++` before and after, and you must specify `"part": "abstract"` as JSON metadata on the block opener. This metadata is required for recognizing the content of this cell as the abstract.
% The abstract should begin with a short description of the problem addressed, briefly describe the new data or analyses, then briefly state the main conclusion(s) and how they are supported, and address any uncertainty.

Can data-driven models for weather and climate predictions learn the underlying physics of the system against which they are trained? Or are they simply capable of identifying statistical patterns without any clear link to the underlying physics? Furner, R. et al. (2022) run a sensitivity analysis of a regression-based ocean temperature model, trained against simulations from a 3D ocean model setup, demostrating that regression models are capable of learning much of the physics of the underlying system.

+++

# Introduction

## Purpose

The article aims to complement the science and methodological development embedded within the original paper, using an open infrastructure that allows users to combine interactive code with text and graphical objects, translating research outputs into findable, accessible, interoperable and reusable outputs and code.

## Description

The notebook demonstrates the inputs, the training of the regression model of ocean temperature and its sensitivity analysis.

## Highlights

* Load the necessary libraries and dependencies to run this notebook, i.e., numpy, xarray, etc.
* Fetch the original dataset used for training the regression models.
* Visualize the simulator outputs and inspect the temperature distributions near the equator, the poles, and the deep ocean.
* Showcase an example of model training for linear regression.
* Evaluate the performance of the regressors.
* Inspect the spatial distribution of the averaged errors.
* Perform a sensitivity analysis and run a series of withholding experiments.
* Summarize our findings.
* Provide contact information.

# Dataset

The training and validation data derive from running the Massachusetts Institute of Technology general circulation model ([MITgcm](https://zenodo.org/record/4672260#.ZFgb_S-B2pY)) —a physically based model capable of simulating the ocean or the atmosphere dynamics due to isomorphisms in the governing equations. This research project relies on a simple 2° sector configuration that captures the fundamental dynamics of the ocean, including a realistic overturning circulation. This configuration features a single ocean basin, with:
+ limited topography
+ simplified coastlines 
+ constant idealized forcing 

The domain runs from 60°S to 60° N, and is just over 20° wide in longitude. The domain is bounded by land along its northern and southern edges, and a strip of land runs along the eastern/western boundary from 60° N to 40° S.  Below this, in the southernmost 20°, the simulator has a periodic boundary condition, allowing flow that exits to the east and west to return to the domain at the western and eastern boundary. The domain has flat-bottom bathymetry of 5,000 m over most of the domain, with a 2° region of 2,500-m depth at the southernmost 20° of the eastern edge.

The simulator has:
+ 42 depth levels, with the surface layer being the thinnest at 10 m, and the bottom 10 levels being the maximum at 250 m. + 11 cells in the longitudinal direction
+ 78 cells in the latitudinal direction

The simulator has a 12-hr time step, with fields output daily. We focus on daily-mean outputs.

# Results

## Ocean dynamics ([Figure %s](#timeline))

The paper uses a  2° sector configuration to simulate ocean dynamics. This configuration features a single ocean basin, with limited topography, simplified coastlines, and constant idealized forcing. This has been used in a number of idealized simulations of Southern Ocean processes and their impacts on the global circulation. This configuration, while relatively simple, captures the fundamental dynamics of the ocean, including a realistic overturning circulation.

In the following script, we load the MITGCM DATASET and visualize the configuration used to simulate the ocean dynamics. Focusing particuarly on:

<ol style="list-style-type: lower-alpha">
<li>Temperature (°C) at 25 m below the surface for one particular day.</li>
<li>Change in temperature between over 1 day at 25 m below the surface.</li>
<li>Standard deviation in temperature at 25 m below the surface.</li>
<li>Temperature (°C) at 25 m below the surface and 13° E for one particular day.</li>
<li>Change in temperature between over 1 day in temperature at 25 m below the surface & 13° E.</li>
<li>Standard deviation in temperature at 25 m below the surface & 13° E.</li>
<li>Time series at 57° N, 17° E, and −25 m.</li>
<li>Time series at 55° S, 9° E, and −25 m.</li>
</ol>

```{figure} #figure-1
:name: fig-1

Computational reproduction of Figure 1.
```

# Conclusions

* There has been much recent interest in developing data-driven models for weather and climate predictions. However, there are open questions regarding their generalizability and robustness, highlighting a need to better understand how they make their predictions. In particular, it is important to understand whether data-driven models learn the underlying physics of the system against which they are trained, or simply identify statistical patterns without any clear link to the underlying physics. 
* In this notebook, we run a sensitivity analysis of a regression-based model of ocean temperature, trained against simulations from a 3D ocean model setup in a very simple configuration. 
* We show that the regressor heavily bases its forecasts on, and is dependent on, variables known to be key to the physics such as currents and density. By contrast, the regressor does not make heavy use of inputs such as location, which have limited direct physical impacts. 
* The model requires nonlinear interactions between inputs in order to show any meaningful skill—in line with the highly nonlinear dynamics of the ocean. Further analysis interprets the ways certain variables are used by the regression model. 
* We see that information about the vertical profile of the water column reduces errors in regions of convective activity, and information about the currents reduces errors in regions dominated by advective processes. 
* Our results demonstrate that even a simple regression model is capable of learning much of the physics of the system being modeled. We expect that a similar sensitivity analysis could be usefully applied to more complex ocean configurations.