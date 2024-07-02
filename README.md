# Supply_Chain_Planning_Optimization

Working Url: TODO


## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
 For the purpose of this study an analysis on monthly food prices will be produced
 by examining an old repository that consists of global nationwide datapoints.
 Each row of this dataset provides a datapoint that consists of multiple variables
 that can be used to extract insights on food allocation per country per region.

 This codebase has all the necessary tools to create such analysis and interfaces the results through dash/plotly in an interactive manner. The repository consists of a business report aswell for the proposed results in a pdf format.

## Project Overview
The dataset consists of a 215MB file, with 2050638 rows and 18 columns /
features. This study focuses on a specific region and commodity, namely Region :
Afghanistan Commodity : Wheat– Retail The focus produces a reduced dataset
that consists of 2312 rows and 18 columns / features.

## Prerequisites

1. Python (version 3.6 or higher)
2. Global food prices, downloadable from `https://data.humdata.org/dataset/wfp-food-prices/resource/12d7c8e3-eff9-4db0-93b7-726825c4fe9a`

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

1.  Linear approach

In order to facilitate an easy approach a simple run via python main.py from
the src directory will produce all the results needed in a linear fashion. There
are 3 ways that we can define inputs:
	
1. Run python main.py and it will prompt for inputs.
2. Run python main.py ”Afghanistan” ”Wheat- Retail” or in general python main.py ”COUNTRY” ”COMMODITY”.
3. Run with python main.py a a a, Define inputs Manually at main.py line 39

2.  Interactive approach

A dash application is being provided that works for the target country =
Afghanistan and selected commodity = Wheat- Retail. Expansion is trivial
with a dictionary of pairs country- country id and commodity- commodity id.
Asimple python app.py will launch the test server at http://127.0.0.1:8050/
and from there a normal approach would be :
1. Fill: Type Country eg AFG block
2. Select: Commodity type
3. Press : LOAD/RELOAD DATA
4. Select: Dataset Focus


From then you can plot price, geographical plots, train arima model and predict
with confidence intervals. The geographical plots can be modified via the
difference in months input text that modifies the time horizon.
It is recommended to leave last the decomposition plot as the front end is
not stable enough for expansive resolutions (The result runs perfectly but the
screen expands and the user needs to slide down the page to find the rest of the
plots.