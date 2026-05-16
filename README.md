#  Agricultural Yield Forecasting & Rainfall Impact Analysis

A Data Science and Machine Learning project focused on analyzing the relationship between monsoon rainfall patterns, historical agricultural trends, and crop yield prediction across districts in Maharashtra, India.

The project combines rainfall statistics with crop production data to perform comparative machine learning experiments, regression analysis, feature engineering, interpretability studies, and time-series trend analysis.

---

#  Project Objectives

- Predict crop yield using rainfall, crop, seasonal, and historical yield data
- Analyze the standalone impact of rainfall on agricultural productivity
- Compare ensemble and regression-based machine learning models
- Study feature importance and temporal yield behavior
- Perform sensitivity and interpretability analysis on rainfall-related variables
- Visualize long-term agricultural and rainfall trends using time-series analysis

---

#  Dataset Overview

The project uses two primary datasets:

## 1. Rainfall Dataset
Contains:
- Monthly rainfall data (June–September)
- Actual rainfall
- Normal rainfall
- Percentage deviation from normal
- Division and district-level rainfall information

### Example Features
- `june_actual_rainfall`
- `august_percent_to_normal`
- `september_actual_rainfall`

---

## 2. Crop Dataset
Contains:
- District
- Crop type
- Season
- Area
- Production
- Yield
- Historical lag features

### Example Features
- `Yield_Lag1`
- `Yield_Lag2`
- `Yield_3yr_Avg`
- `Yield_3yr_Std`

---

# 3. Data Preprocessing & Cleaning

The datasets required extensive preprocessing before modeling.

## Steps Performed
- Standardized district names using lowercase normalization and whitespace cleaning
- Resolved naming inconsistencies between datasets manually
- Merged rainfall and crop datasets on:
  - District
  - Year
- Removed duplicate and inconsistent records
- Created experiment-specific feature subsets
- Applied encoding and feature scaling for regression models

---

# 4. District Mapping Challenges

Some districts had inconsistent naming conventions:

- `raigad → raigadh`
- `parbhani → parabhani`
- `ahilyanagar → ahmednagar`
- `dharashiv → osmanabad`

These mismatches were manually resolved prior to merging.

---

#  Tech Stack

## Languages & Libraries
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Matplotlib

---

# 5. Machine Learning & Statistical Models Used

## Ensemble Learning Models
- Random Forest Regressor
- XGBoost Regressor

## Regression Models
- Linear Regression
- Ridge Regression
- Lasso Regression

---

# 6. Experimental Design

The project was divided into multiple experiments to understand the contribution of different feature groups.

---

# 7. Experiment 1 — Rainfall-only Model

## Goal
Determine whether rainfall alone can predict crop yield.

## Features Used
- Monthly rainfall values
- Rainfall deviation percentages
- Seasonal indicators

## Features Removed
- Crop
- Area
- Production
- Historical yield features

## Result
- **R² ≈ -0.11**

## Observation
Rainfall alone was insufficient for accurate crop yield prediction.

---

#  Experiment 2 — Crop + Rainfall Model (No Lag)

## Goal
Analyze the combined effect of crop type and rainfall.

## Features Used
- Crop
- Season
- Rainfall features

## Features Removed
- Historical yield features
- Production
- Area

## Result
- **R² ≈ 0.94**
- Crop became the dominant predictive feature

## Observation
Crop type significantly improved model performance, while rainfall acted as a secondary contributor.

---

#  Experiment 3 — Full Historical Yield Model

## Goal
Build the highest-performing forecasting model.

## Features Used
- Historical yield features
- Crop
- Rainfall
- Seasonal information

## Features Removed
- Production
- Area

## Result
- **R² ≈ 0.98**
- `Yield_3yr_Avg` became the dominant feature

## Observation
Historical yield strongly influenced future predictions, indicating temporal stability in agricultural productivity.

---

#  Regression Model Analysis

In addition to ensemble learning models, multiple regression techniques were implemented for comparative analysis.

## Models Evaluated
- Linear Regression
- Ridge Regression
- Lasso Regression

## Purpose
- Compare linear and nonlinear modeling performance
- Study the effect of regularization
- Evaluate feature sparsity and coefficient shrinkage

## Observations
- Linear models underperformed compared to tree-based models
- Ridge Regression improved stability through regularization
- Lasso Regression reduced less important feature coefficients
- Ensemble models captured nonlinear relationships more effectively

---

#  Feature Engineering

Additional rainfall-based features were explored to improve environmental signal extraction.

## Engineered Features
- Seasonal rainfall aggregation
- Rainfall deviation metrics
- Rainfall variability indicators
- Drought/excess rainfall flags
- Early vs peak monsoon rainfall features

---

#  Model Evaluation Metrics

Models were evaluated using:

- R² Score
- RMSE (Root Mean Squared Error)

---

#  Time-Series Analysis

Time-series visualizations were used to analyze agricultural trends over multiple years.

## Analyses Performed
- District-wise yield trends over time
- Rainfall variation across years
- Yield vs rainfall temporal comparison

## Observations
- Agricultural yield exhibited relatively stable long-term trends
- Historical yield continuity explained the dominance of lag-based features
- Rainfall fluctuations affected deviations rather than baseline productivity

---

#  Interpretability & Sensitivity Analysis

The project also included analytical and interpretability techniques.

## 1. Feature Importance Analysis
Used to identify dominant predictive variables across experiments.

## 2. Residual Analysis
Studied model prediction errors under varying rainfall conditions.

## 3. Partial Dependence Plots (PDP)
Analyzed how changes in rainfall features influenced yield predictions.

## 4. Comparative Feature Analysis
Compared rainfall-only, no-lag, and historical-yield models to understand feature contribution hierarchy.

---

#  Key Insights

## 1. Historical Yield Dominates
Past yield values were the strongest predictors of future yield.

## 2. Crop Type Strongly Influences Yield
Different crops inherently follow different productivity patterns.

## 3️. Rainfall Has Limited Standalone Predictive Power
Rainfall alone was insufficient to explain yield variation.

## 4️. Rainfall Influences Variability
Rainfall contributes more toward fluctuations and extreme agricultural conditions rather than baseline yield.

## 5️. Nonlinear Models Perform Better
Tree-based ensemble methods outperformed traditional regression approaches due to complex nonlinear interactions between agricultural and environmental features.

---

#  Example Visualizations

- Predicted vs Actual Yield
- Residual Plots
- Feature Importance Graphs
- Rainfall vs Yield Scatter Plots
- Time-Series Yield Trends
- Partial Dependence Plots
- Regression Comparison Graphs

---

# Suggested Project Structure

```bash
project/
│
├── data/
│   └── final_dataset.csv
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_rainfall_only_model.ipynb
│   ├── 03_no_lag_model.ipynb
│   ├── 04_full_model.ipynb
│   ├── 05_regression_models.ipynb
│   └── 06_interpretability_analysis.ipynb
│
├── visuals/
├── models/
└── README.md
