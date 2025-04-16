import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Step 1: Load dataset
df = pd.read_csv('psam_US.csv')

# Step 2: Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# Step 3: Convert relevant columns to numeric
df['ACCESSINET'] = pd.to_numeric(df['ACCESSINET'], errors='coerce')
df['BROADBND'] = pd.to_numeric(df['BROADBND'], errors='coerce')
df['HISPEED'] = pd.to_numeric(df['HISPEED'], errors='coerce')
df['HINCP'] = pd.to_numeric(df['HINCP'], errors='coerce')    # Household income (proxy for education)
df['WGTP'] = pd.to_numeric(df['WGTP'], errors='coerce')      # Household weight
df['ACR'] = pd.to_numeric(df['ACR'], errors='coerce')        # Lot size proxy for rural/urban

# Step 4: Categorize as Urban, Suburban, or Rural
def classify_area(x):
    if x == 1:
        return "Urban"
    elif x == 2:
        return "Suburban"
    else:
        return "Rural"

df['RuralUrban'] = df['ACR'].apply(classify_area)

# Drop missing values
df = df.dropna(subset=['BROADBND', 'HINCP'])

# Step 5: Create a Binary Broadband Indicator
df['HasBroadband'] = df['BROADBND'].apply(lambda x: 1 if x == 1 else 0)

# Step 6: Compute Weighted Average Household Income by Broadband Access
summary = df.groupby(['RuralUrban', 'HasBroadband']).apply(
    lambda x: pd.Series({
        'AvgIncome': (x['HINCP'] * x['WGTP']).sum() / x['WGTP'].sum(),
        'Count': x['WGTP'].sum()
    })
).reset_index()

print("\nAverage Household Income in Rural Areas, by Broadband Access:")
print(summary)

# Step 7: Visualization – Bar Chart of Average Income by Broadband Access
plt.figure(figsize=(8, 5))
sns.barplot(x='HasBroadband', y='AvgIncome', hue='RuralUrban', data=summary, palette='Blues')
plt.title("Average Household Income in Rural, Suburban & Urban Areas\nby Broadband Access")
plt.xlabel("Has Broadband (1=Yes, 0=No)")
plt.ylabel("Weighted Average Household Income ($)")
plt.legend(title="Area Type")
plt.savefig('Weighted Average Household Income ($).png')
plt.show()

# Step 8: Regression Analysis: Broadband vs. Household Income
X = sm.add_constant(df[['HasBroadband']])  # Add intercept
y = df['HINCP']

model = sm.OLS(y, X).fit()  # Ordinary Least Squares
print(model.summary())

# Interpretation:
# - If coef(HasBroadband) is **positive and significant (p<0.05)**, higher income is linked to broadband.
