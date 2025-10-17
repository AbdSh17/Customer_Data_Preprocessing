#%%
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#Step1
data =  pd.read_csv("customer_data.csv")
#%% md
# ## Explore Data in general
#%% md
# ### Observations From data features
# - **CustomerID**: Unique Identifier, *irrelevant*.
# - **Age**: Numerical `int()` data, the outliers more of a domain knowledge. 
# - **Gender**: Categorical Data that's already Hot-Encoded.
# - **Income**: : Annual income of the customer (in USD), for outliers must plot and explore the data .
# - **Tenure**: Numerical `int()` data, the outliers mix of domain knowledge and data exploration.
# - **ProductType**: Categorical Data that's already Hot-Encoded.
# - **SupportCalls**: Numerical `int()` data, for outliers must plot and explore the data.
# - **ChurnStatus**: Categorical Data that's already Hot-Encoded.
#%%
data.head(7)
#%% md
# ### Observations From Data Info
# Just read the thing -_-
#%%
data.info()
#%% md
# ### Observations From Data `mean/std`
# - **CustomerID**: Unique Identifier, *irrelevant*.
# - **Age**: Customers Ages are very variant, most of them are old. 
# - **Gender**: Customers gender is so not random, both genders buy equally.
# - **Income**: : Customers incomes are very variant, std is even bigger than the mean four times, maybe there's a lot of outliers or *idk*.
# - **Tenure**: Customers tenure is variant but not *TOO* variant yk.
# - **ProductType**:Like gender.
# - **SupportCalls**: STD is really higher than the mean (: .
# - **ChurnStatus**: Most of them STAYED.
#%%
data.describe()
#%% md
# ### Data Plots - Numerical
#%%
import matplotlib.pyplot as plt
import math
numerical_features = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
numerical_features.remove("Gender")
numerical_features.remove("ProductType")
numerical_features.remove("ChurnStatus")

n_features = len(numerical_features)
n_cols = 2
n_rows = math.ceil(n_features / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
fig.suptitle('Distribution of Numerical Features', fontsize=16, fontweight='bold')
axes = axes.flatten() if n_features > 1 else [axes]
for idx, feature in enumerate(numerical_features):
    axes[idx].hist(data[feature], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'{feature} Distribution', fontweight='bold')
    axes[idx].set_xlabel(feature)
    axes[idx].set_ylabel('Frequency')
    axes[idx].axvline(data[feature].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {data[feature].mean():.2f}')
    axes[idx].axvline(data[feature].median(), color='green', linestyle='--', 
                      linewidth=2, label=f'Median: {data[feature].median():.2f}')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
for j in range(idx+1, len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
# plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
plt.show()
#%% md
# ### Data Plot - Categorical
#%%
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Categorical Features Analysis', fontsize=16, fontweight='bold')
# Gender distribution
gender_counts = data['Gender'].value_counts()
axes[0, 0].bar(['Male', 'Female'], gender_counts.values, color=['#3498db', '#e74c3c'])
axes[0, 0].set_title('Gender Distribution', fontweight='bold')
axes[0, 0].set_ylabel('Count')
axes[0, 0].grid(True, alpha=0.3, axis='y')
# Product Type distribution
product_counts = data['ProductType'].value_counts()
axes[0, 1].bar(['Basic', 'Premium'], product_counts.values, color=['#95a5a6', '#f39c12'])
axes[0, 1].set_title('Product Type Distribution', fontweight='bold')
axes[0, 1].set_ylabel('Count')
axes[0, 1].grid(True, alpha=0.3, axis='y')
# Churn Status distribution
churn_counts = data['ChurnStatus'].value_counts()
colors = ['#2ecc71', '#e74c3c']
axes[1, 0].bar(['Stayed', 'Churned'], churn_counts.values, color=colors)
axes[1, 0].set_title('Churn Status Distribution', fontweight='bold')
axes[1, 0].set_ylabel('Count')
axes[1, 0].grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()
#%%
data.isnull().sum()
#%% md
# ### Age
# #### Age: Dealing with **Outliers**
#%%
len(data[(data["Age"] < 18) | (data["Age"] > 90)])
#%% md
# #### Drop any age that is less than 18, because there are only two rows 
# #### (and they're not adults -_-)
#%%
data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
#%% md
# #### Age: Dealing with **Missing Values**
#%%
print(data_clean_age.isnull().sum())
#%%
data_clean_age["Age"].describe()
#%% md
# #### We noticed that the mean and median are relatively close 43.6 and 43 indicating that our data is symmetric, and it won’t really matter which we take so we took the mean which is 44 since the data is barely skewed
# 
#%%
skew_value = data_clean_age["Age"].skew()
print(f"Skewness of '{"Age"}': {skew_value}")
data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)

#%%
print(data_clean_age.isnull().sum())
#%%
skew_value = data_clean_age["Age"].skew()
print(f"Skewness of '{"Age"}': {skew_value}")
#%% md
# #### Gender ...
#%%

#%% md
# ### Income
# #### Income: Dealing with **Missing Values**
#%%
data_income = data_clean_age.copy()
skew_value = data_income["Income"].skew()
print(f"Skewness of '{"Income"}': {skew_value}")
#%%
data_income["Income"].median()
#%% md
# #### Looking at the histogram for the income we can see that the data is skewed so we decided to fill the missing data with the median
#%%
data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
#%%
print(data_income.isnull().sum())
#%% md
# #### Income: Dealing with **Outliers**
#%%
data_income["Income"].describe()
#%%
Q1 = data_income["Income"].quantile(0.25)
Q3 = data_income["Income"].quantile(0.75)
IQR = Q3 - Q1
income_lower_outliers_value = Q1 - 1.5 * IQR
income_lower_outliers_value
#%%
Q1 = data_income["Income"].quantile(0.25)
Q3 = data_income["Income"].quantile(0.75)
IQR = Q3 - Q1
income_upper_outliers_value = Q3 + 1.5 * IQR
income_upper_outliers_value
#%% md
# #### Printing the income outliers 
#%%
data_income[
    (data_income["Income"] > income_upper_outliers_value) |
    (data_income["Income"] < data_income["Income"].min())
]["Income"]
#%%
# --- Compute IQR and outliers ---
income = data_income['Income'].dropna()
Q1 = income.quantile(0.25)
Q3 = income.quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = income[(income < lower_bound) | (income > upper_bound)]

# --- Count repeated outlier values ---
if len(outliers) > 0:
    outlier_counts = outliers.value_counts().reset_index()
    outlier_counts.columns = ['Outlier Value', 'Count']
    outlier_counts = outlier_counts.sort_values('Outlier Value')
else:
    outlier_counts = pd.DataFrame(columns=['Outlier Value', 'Count'])

# --- Create figure ---
plt.figure(figsize=(11, 6))
box = plt.boxplot(
    income,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor='lightblue', color='blue'),
    medianprops=dict(color='red', linewidth=2),
    whiskerprops=dict(color='blue', linewidth=2),
    capprops=dict(color='blue', linewidth=2),
    flierprops=dict(marker='o', color='orange', alpha=0.7)
)

plt.title('Income Box Plot Focused on IQR (with Outlier Summary Table)')
plt.ylabel('Income')
plt.grid(True, alpha=0.3)

# Focus on IQR range
plt.ylim(Q1 - IQR, Q3 + IQR)

# --- Annotate quartiles and median ---
plt.text(1.1, Q1, f'Q1: {Q1:.2f}', color='green')
plt.text(1.1, income.median(), f'Median: {income.median():.2f}', color='red')
plt.text(1.1, Q3, f'Q3: {Q3:.2f}', color='green')

# --- Annotate actual whisker values from boxplot ---
lower_whisker = box['whiskers'][0].get_ydata()[1]  # bottom whisker
upper_whisker = box['whiskers'][1].get_ydata()[1]  # top whisker

plt.text(0.9, lower_whisker, f'Lower Whisker: {lower_whisker:.2f}', color='blue', fontsize=9, ha='right')
plt.text(0.9, upper_whisker, f'Upper Whisker: {upper_whisker:.2f}', color='blue', fontsize=9, ha='right')

# --- Plot visible outliers ---
visible_outliers = outliers[(outliers >= plt.ylim()[0]) & (outliers <= plt.ylim()[1])]
for val in visible_outliers:
    plt.plot(1, val, 'ro')
    plt.text(1.05, val, f'{val:.2f}', color='orange', fontsize=8)

# --- Side table of outliers ---
if not outlier_counts.empty:
    table_data = outlier_counts.round(2).astype(str).values.tolist()
    table_data.insert(0, ['Value', 'Count'])  # header row

    plt.table(
        cellText=table_data,
        colWidths=[0.15, 0.1],
        cellLoc='center',
        loc='right',
        colLabels=None,
        bbox=[1.05, 0.15, 0.3, 0.7]  # [x, y, width, height]
    )
else:
    plt.gcf().text(
        0.8, 0.5, "No outliers detected",
        fontsize=11, color='gray',
        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'),
        va='center', ha='left'
    )

plt.tight_layout(rect=[0, 0, 0.75, 1])  # leave space for table
plt.show()
#%%
from scipy import stats
import numpy as np

z_scores = np.abs(stats.zscore(data_income["Income"]))
threshold = 2 # 2 standard deviation away

income_outliers_zscore = data_income[z_scores > threshold]

income_outliers_zscore["Income"]
#%%
data_income[data_income["Income"] > income_upper_outliers_value]
#%% md
# #### Dropping —- No we will lose too much data
# #### Smoothing —- Data is too high smoothing wont work 
# #### Capping at upper whisker —-- Keeps the Data Rows but it helps deal with the outliers
#%%
data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
#%%
data_income[data_income["Income"] > income_upper_outliers_value]
#%% md
# #### New Skew Value
#%%
skew_value = data_income["Income"].skew()
print(f"Skewness of '{"Income"}': {skew_value}")
#%% md
# ### Tenure
# #### Tenure: Dealing with **Missing Values**
#%%
data_tenure = data_income.copy()
skew_value = data_tenure["Tenure"].skew()
print(f"Skewness of '{"Tenure"}': {skew_value}")
#%% md
# #### The values are approximately normally distributed with minimal skew, so we can use the mean. Since both the mean and median are around 5, we will fill the missing values with 5.
# 
#%%
data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
#%%
print(data_tenure.isnull().sum())
#%%
skew_value = data_tenure["Tenure"].skew()
print(f"Skewness of '{"Tenure"}': {skew_value}")
#%% md
# #### Tenure: Dealing with **Outliers**
# none
#%% md
# ### Support Calls
# #### Support Calls: Dealing with **Outliers**
#%%
data_sc = data_tenure.copy()
skew_value = data_sc["SupportCalls"].skew()
print(f"Skewness of '{"SupportCalls"}': {skew_value}")
#%%
data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
#%%
data_sc["SupportCalls"].mean(), data_sc["SupportCalls"].median()
#%% md
# #### Support Calls: Dealing with **Missing Values**
#%%
data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
#%%
print(data_sc.isnull().sum())

#%%
skew_value = data_sc["SupportCalls"].skew()
print(f"Skewness of '{"SupportCalls"}': {skew_value}")
#%%
data = data_sc.copy()
#%% md
# ## Re-print the data plots after pre-processing
#%% md
# ### Plotting **Numerical** Data
#%%
import matplotlib.pyplot as plt
import math
numerical_features = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
numerical_features.remove("Gender")
numerical_features.remove("ProductType")
numerical_features.remove("ChurnStatus")

n_features = len(numerical_features)
n_cols = 2
n_rows = math.ceil(n_features / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
fig.suptitle('Distribution of Numerical Features', fontsize=16, fontweight='bold')
axes = axes.flatten() if n_features > 1 else [axes]
for idx, feature in enumerate(numerical_features):
    axes[idx].hist(data[feature], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'{feature} Distribution', fontweight='bold')
    axes[idx].set_xlabel(feature)
    axes[idx].set_ylabel('Frequency')
    axes[idx].axvline(data[feature].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {data[feature].mean():.2f}')
    axes[idx].axvline(data[feature].median(), color='green', linestyle='--', 
                      linewidth=2, label=f'Median: {data[feature].median():.2f}')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
for j in range(idx+1, len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
plt.show()
#%% md
# ### Plotting **Categorical** Data
#%%
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Categorical Features Analysis', fontsize=16, fontweight='bold')
# Gender distribution
gender_counts = data['Gender'].value_counts()
axes[0, 0].bar(['Male', 'Female'], gender_counts.values, color=['#3498db', '#e74c3c'])
axes[0, 0].set_title('Gender Distribution', fontweight='bold')
axes[0, 0].set_ylabel('Count')
axes[0, 0].grid(True, alpha=0.3, axis='y')
# Product Type distribution
product_counts = data['ProductType'].value_counts()
axes[0, 1].bar(['Basic', 'Premium'], product_counts.values, color=['#95a5a6', '#f39c12'])
axes[0, 1].set_title('Product Type Distribution', fontweight='bold')
axes[0, 1].set_ylabel('Count')
axes[0, 1].grid(True, alpha=0.3, axis='y')
# Churn Status distribution
churn_counts = data['ChurnStatus'].value_counts()
colors = ['#2ecc71', '#e74c3c']
axes[1, 0].bar(['Stayed', 'Churned'], churn_counts.values, color=colors)
axes[1, 0].set_title('Churn Status Distribution', fontweight='bold')
axes[1, 0].set_ylabel('Count')
axes[1, 0].grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()
#%% md
# ## Normalizing The data - 
#%%
data_standardized = data.copy()
data_standardized["Income"] = (data_standardized["Income"] - data_standardized["Income"].mean()) / data_standardized["Income"].std()

data_standardized["Age"] = (data_standardized["Age"] - data_standardized["Age"].mean()) / data_standardized["Age"].std()

data_standardized["SupportCalls"] = (data_standardized["SupportCalls"] - data_standardized["SupportCalls"].mean()) / data_standardized["SupportCalls"].std()

data_standardized["Tenure"] = (data_standardized["Tenure"] - data_standardized["Tenure"].mean()) / data_standardized["Tenure"].std()

#%%
data = data_standardized
numerical_features = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
numerical_features.remove("Gender")
numerical_features.remove("ProductType")
numerical_features.remove("ChurnStatus")

n_features = len(numerical_features)
n_cols = 2
n_rows = math.ceil(n_features / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
fig.suptitle('Distribution of Numerical Features', fontsize=16, fontweight='bold')
axes = axes.flatten() if n_features > 1 else [axes]
for idx, feature in enumerate(numerical_features):
    axes[idx].hist(data[feature], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'{feature} Distribution', fontweight='bold')
    axes[idx].set_xlabel(feature)
    axes[idx].set_ylabel('Frequency')
    axes[idx].axvline(data[feature].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {data[feature].mean():.2f}')
    axes[idx].axvline(data[feature].median(), color='green', linestyle='--', 
                      linewidth=2, label=f'Median: {data[feature].median():.2f}')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
for j in range(idx+1, len(axes)):
    fig.delaxes(axes[j])
plt.tight_layout()
plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
plt.show()
#%% md
# ### Sactter Plot
#%%
data = data_sc.copy()
import seaborn as sns

numeric_cols = data.select_dtypes(include=["float64", "int64"]).columns.drop(["ChurnStatus", "ProductType", "Gender"])

for col in numeric_cols:
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=data, x=col, y="ChurnStatus", alpha=0.6)
    plt.title(f"{col} vs ChurnStatus (Scatter Plot)")
    plt.show()
#%%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

gender_churn = data.groupby('Gender')['ChurnStatus'].mean() * 100
axes[0].bar(['Male', 'Female'], gender_churn.values, color=['#3498db', '#e74c3c'], edgecolor='black')
axes[0].set_title('Churn Rate by Gender', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Churn Rate (%)', fontsize=12)
axes[0].set_ylim(0, 100)
for i, v in enumerate(gender_churn.values):
    axes[0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

product_churn = data.groupby('ProductType')['ChurnStatus'].mean() * 100
axes[1].bar(['Basic', 'Premium'], product_churn.values, color=['#95a5a6', '#f39c12'], edgecolor='black')
axes[1].set_title('Churn Rate by Product Type', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Churn Rate (%)', fontsize=12)
axes[1].set_ylim(0, 100)
for i, v in enumerate(product_churn.values):
    axes[1].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

#%%
numerical_features = ['Age', 'Income', 'Tenure', 'SupportCalls']
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()

for idx, col in enumerate(numerical_features):
    sns.boxplot(data=data, x='ChurnStatus', y=col, ax=axes[idx], palette=['#2ecc71', '#e74c3c'])
    axes[idx].set_title(f'{col} vs Churn Status', fontsize=14, fontweight='bold')
    axes[idx].set_xlabel('Churn Status (0=Stayed, 1=Churned)', fontsize=12)
    axes[idx].set_ylabel(col, fontsize=12)

plt.tight_layout()
plt.show()
    

#%%

# Drop unwanted column
data_corr_matrix = data.drop(["CustomerID"], axis=1)

# Compute correlation matrix
data_corr_matrix = data_corr_matrix.corr(method='pearson')

# Print correlation with ChurnStatus (sorted)
print("Correlation with ChurnStatus:")
print(data_corr_matrix['ChurnStatus'].sort_values(ascending=False))

# Define numeric columns you want in the heatmap
numerical_cols = ['Age', 'Gender', 'Income', 'Tenure', 'ProductType', 'SupportCalls', 'ChurnStatus']
correlation_matrix = data[numerical_cols].corr(method='pearson')

# Plot full heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)

ax.set_title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

#%%
