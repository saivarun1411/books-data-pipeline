# Titanic Analytics & Predictive Modeling

## Project Overview

This module analyzes the Titanic dataset and builds an end-to-end predictive modeling pipeline. The workflow covers data profiling, cleaning, exploratory data analysis, classification, class-imbalance handling, Random Forest hyperparameter tuning, regression, model comparison, and pipeline persistence.

The cleaned Titanic dataset is saved as `titanic.csv` inside the `analytics` directory as an offline fallback.

---

## Data Cleaning

The Titanic dataset was profiled for missing values, duplicate records, data types, and descriptive statistics.

Missing values were handled according to the assignment's percentage-based strategy. Columns with low missingness were handled using row removal where appropriate, while columns with moderate missingness were imputed. High-missingness fields were evaluated separately before deciding whether to retain or remove them.

The modeling pipeline performs its own missing-value handling using preprocessing fitted only on the training data.

---

## Exploratory Data Analysis

### Age and Fare

Histograms and box plots were used to examine the distributions of `age` and `fare`. The IQR method was used to identify potential outliers.

Fare showed a right-skewed distribution, with higher values extending the distribution toward the right side.

### Survival by Sex

Female passengers had a substantially higher survival rate than male passengers. This indicates that sex was one of the strongest descriptive factors associated with survival.

### Survival by Passenger Class

First-class passengers had the highest survival rate, followed by second-class passengers, while third-class passengers had the lowest survival rate. This indicates a strong relationship between passenger class and survival.

### Survival by Sex and Passenger Class

The combined analysis shows that female passengers generally had higher survival rates than male passengers across passenger classes. Passenger class also affected survival within each sex group.

### Age Distribution by Survival

The age distributions of survivors and non-survivors overlap, but survival patterns vary across different age groups. Age therefore provides useful information but is not by itself sufficient to explain survival.

---

## Correlation Analysis

The correlation heatmap was calculated using exactly:

- `survived`
- `pclass`
- `age`
- `sibsp`
- `parch`
- `fare`

The derived boolean columns `adult_male` and `alone` were excluded.

The two strongest absolute correlations were:

1. `fare` and `pclass`: **-0.548193**

   This negative correlation indicates that higher passenger classes are generally associated with higher fares, because the numerical encoding of `pclass` assigns first class a lower value than third class.

2. `sibsp` and `parch`: **+0.414542**

   This positive correlation indicates that passengers traveling with siblings/spouses were somewhat more likely to also travel with parents/children.

---

## Standardization Check

As an exploratory check, `age` and `fare` were standardized using z-score standardization.

After standardization, both variables have approximately:

- Mean = 0
- Standard deviation = 1

This exploratory transformation was separate from the actual modeling pipeline. The modeling pipeline performs its own train-only scaling.

---

# Predictive Modeling

## Train/Test Split

The data was split using a stratified train/test split.

- Training set: **711 rows**
- Testing set: **178 rows**

Stratification was used to preserve the survived/not-survived class proportion in both training and testing datasets.

The target variable was:

`survived`

The leakage-prone `alive` column was removed from the modeling features.

---

## Preprocessing Pipeline

The preprocessing pipeline contains:

- Median imputation for numeric variables
- Most-frequent imputation for categorical variables
- StandardScaler for numeric features
- OneHotEncoder for categorical features

The preprocessing is fitted only on the training data and then applied to the test data through a scikit-learn Pipeline and ColumnTransformer.

The final feature set excludes the target and the `alive` target-leakage column.

---

# Classification Models

Three classification models were trained on the same train/test split:

1. Logistic Regression
2. Decision Tree
3. Random Forest

The Decision Tree was also visualized using `plot_tree`.

## Classification Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8146 | 0.7966 | 0.6912 | 0.7402 | 0.8686 |
| Decision Tree | 0.8034 | 0.7538 | 0.7206 | 0.7368 | 0.7814 |
| Random Forest | 0.7697 | 0.7143 | 0.6618 | 0.6870 | 0.8110 |

Logistic Regression achieved the highest accuracy and ROC-AUC among the three baseline classifiers. Decision Tree achieved slightly higher recall than Logistic Regression, while Random Forest performed lower on the main classification metrics in this experiment.

---

# Class Imbalance Analysis

The target distribution was:

- Not survived: **439**
- Survived: **272**

Three approaches were compared:

| Approach | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Baseline | 0.8146 | 0.7966 | 0.6912 | 0.7402 |
| class_weight='balanced' | **0.8315** | 0.7794 | **0.7794** | **0.7794** |
| SMOTE | 0.8202 | 0.7813 | 0.7353 | 0.7576 |

The class-weighted approach performed best overall because it produced the highest accuracy, recall, and F1 score among the three imbalance strategies. It improved detection of the minority survived class without generating synthetic samples.

SMOTE was applied only to the training data to avoid test-set leakage.

---

# Random Forest Hyperparameter Tuning

GridSearchCV was used to tune the Random Forest.

Best parameters:

```text
max_depth = 10
max_features = sqrt
n_estimators = 100



## Regression Analysis

Two regression models were evaluated for predicting fare: Linear Regression and Ridge Regression.

| Model | MAE | RMSE | R² | Adjusted R² |
|---|---:|---:|---:|---:|
| Linear Regression | 20.6867 | 42.5706 | 0.3207 | 0.3050 |
| Ridge Regression | 20.6647 | 42.5697 | 0.3208 | 0.3051 |

Ridge Regression performed slightly better than Linear Regression, with marginally lower MAE and RMSE and slightly higher R² and Adjusted R². The residual analysis was also reviewed for heteroscedasticity.

## Final Model Recommendation

Class-weighted Logistic Regression is the recommended classifier for deployment. It achieved the highest accuracy of 83.15%, recall of 77.94%, and F1 score of 77.94% among the imbalance-handling approaches, providing a better balance between overall accuracy and minority-class detection. Baseline Logistic Regression achieved the highest ROC-AUC of 86.86%, showing strong overall discrimination, but its recall was lower at 69.12%. Therefore, class-weighted Logistic Regression is preferred when balanced classification performance and improved detection of survivors are prioritized.

## Pipeline Persistence

The complete preprocessing and classification pipeline was saved as:

`titanic_final_pipeline.joblib`

The saved pipeline was successfully reloaded using `joblib.load()` and tested on raw input data. The reloaded pipeline produced predictions successfully, confirming that the complete preprocessing and model workflow can be reused on new raw data.