# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm

# Step 1: Load dataset
df = pd.read_csv('psam_US.csv')

# Step 2: Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# Step 3: Convert relevant columns to numeric
df['BROADBND'] = pd.to_numeric(df['BROADBND'], errors='coerce')  # Broadband access
df['WORKSTAT'] = pd.to_numeric(df['WORKSTAT'], errors='coerce')  # Work status
df['WKEXREL'] = pd.to_numeric(df['WKEXREL'], errors='coerce')  # Work experience
df['WGTP'] = pd.to_numeric(df['WGTP'], errors='coerce')  # Household weight
df['ST'] = pd.to_numeric(df['ST'], errors='coerce')  # State code

# Step 4: Categorize as Urban, Suburban, or Rural
def classify_area(x):
    if x == 1:
        return "Urban"
    elif x == 2:
        return "Suburban"
    else:
        return "Rural"

df['RuralUrban'] = df['ACR'].apply(classify_area)

# Drop missing values in BROADBND, WORKSTAT, and ST
df = df.dropna(subset=['BROADBND', 'WORKSTAT', 'ST'])

# Step 5: Create binary indicators
df['NoBroadband'] = df['BROADBND'].apply(lambda x: 2 if x == 0 else 0)  # 2 = No broadband
df['Unemployed'] = df['WORKSTAT'].apply(lambda x: 1 if x in [3, 6] else 0)  # Unemployed based on WORKSTAT

# Step 6: Aggregate broadband and unemployment rates by state & rural/urban
broadband_unemp = df.groupby(['ST', 'RuralUrban']).apply(
    lambda x: pd.Series({
        'NoBroadbandRate': (x['NoBroadband'] * x['WGTP']).sum() / x['WGTP'].sum() * 100,
        'UnemploymentRate': (x['Unemployed'] * x['WGTP']).sum() / x['WGTP'].sum() * 100
    })
).reset_index()

# Step 7: Perform Regression Analysis (Checking Relationship)
X = broadband_unemp['NoBroadbandRate']
y = broadband_unemp['UnemploymentRate']
X = sm.add_constant(X)  # Adds intercept term
model = sm.OLS(y, X).fit()
print(model.summary())  # Show regression results

# Step 8: Visualize Results with a Scatter Plot
plt.figure(figsize=(10, 6))
sns.regplot(x='NoBroadbandRate', y='UnemploymentRate', data=broadband_unemp, scatter_kws={"s": 50}, line_kws={"color": "red"})
plt.xlabel("Percentage of Households Without Broadband")
plt.ylabel("Unemployment Rate (%)")
plt.title("Broadband Access vs. Unemployment in Rural Areas")
plt.show()  # Display the plot
plt.savefig("Broadband Access vs. Unemployment in Rural Areas.png")

# Create a heatmap-ready pivot table
heatmap_data = broadband_unemp.pivot_table(
    index='ST', 
    columns='RuralUrban', 
    values='UnemploymentRate',
    aggfunc='mean'
)

# Plot heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.5)

plt.title("Heatmap: Unemployment Rate by State and Area Type")
plt.xlabel("Area Type")
plt.ylabel("State Code")
plt.tight_layout()
plt.show()  # Display the plot
plt.savefig('unemployment_heatmap.png')
plt.close()

# Step 9: Create an interactive map visualization using Plotly Express
# First, we need to add state names to our data
# Create a dictionary mapping state codes to state names
state_codes = {
    1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas', 6: 'California',
    8: 'Colorado', 9: 'Connecticut', 10: 'Delaware', 11: 'District of Columbia',
    12: 'Florida', 13: 'Georgia', 15: 'Hawaii', 16: 'Idaho', 17: 'Illinois',
    18: 'Indiana', 19: 'Iowa', 20: 'Kansas', 21: 'Kentucky', 22: 'Louisiana',
    23: 'Maine', 24: 'Maryland', 25: 'Massachusetts', 26: 'Michigan', 27: 'Minnesota',
    28: 'Mississippi', 29: 'Missouri', 30: 'Montana', 31: 'Nebraska', 32: 'Nevada',
    33: 'New Hampshire', 34: 'New Jersey', 35: 'New Mexico', 36: 'New York',
    37: 'North Carolina', 38: 'North Dakota', 39: 'Ohio', 40: 'Oklahoma',
    41: 'Oregon', 42: 'Pennsylvania', 44: 'Rhode Island', 45: 'South Carolina',
    46: 'South Dakota', 47: 'Tennessee', 48: 'Texas', 49: 'Utah', 50: 'Vermont',
    51: 'Virginia', 53: 'Washington', 54: 'West Virginia', 55: 'Wisconsin', 56: 'Wyoming'
}

# Add state names to the dataframe
broadband_unemp['State_Name'] = broadband_unemp['ST'].map(state_codes)

# Create a simplified dataset for the map - aggregate by state only (not by RuralUrban)
state_data = broadband_unemp.groupby('ST').agg({
    'UnemploymentRate': 'mean',
    'NoBroadbandRate': 'mean',
    'State_Name': 'first'  # Take the first state name for each state code
}).reset_index()

# Print the state data to verify it's correct
print("State data for map:")
print(state_data.head())

# Create an interactive choropleth map with the simplified data
fig = px.choropleth(
    state_data,
    locations='State_Name',
    locationmode='USA-states',
    color='UnemploymentRate',
    scope='usa',
    title='Unemployment Rate by State',
    color_continuous_scale='Reds',
    hover_data=['NoBroadbandRate']
)

# Update the layout for better visibility
fig.update_layout(
    title_text='Unemployment Rate by State',
    geo_scope='usa',
    height=600,
    width=1000
)

# Show the interactive map
fig.show()

# Save the interactive map as HTML file (can be opened in a browser)
fig.write_html("unemployment_map.html")

# Create a separate map for rural areas only
rural_data = broadband_unemp[broadband_unemp['RuralUrban'] == 'Rural'].copy()
rural_state_data = rural_data.groupby('ST').agg({
    'UnemploymentRate': 'mean',
    'NoBroadbandRate': 'mean',
    'State_Name': 'first'
}).reset_index()

# Create a map for rural areas
fig_rural = px.choropleth(
    rural_state_data,
    locations='State_Name',
    locationmode='USA-states',
    color='UnemploymentRate',
    scope='usa',
    title='Unemployment Rate in Rural Areas by State',
    color_continuous_scale='Reds',
    hover_data=['NoBroadbandRate']
)

# Update the layout
fig_rural.update_layout(
    title_text='Unemployment Rate in Rural Areas by State',
    geo_scope='usa',
    height=600,
    width=1000
)

# Show the rural map
fig_rural.show()

# Save the rural map
fig_rural.write_html("rural_unemployment_map.html")

