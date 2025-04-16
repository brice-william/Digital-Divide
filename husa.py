#import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the datasets
df_husa = pd.read_csv('psam_husa.csv')
df_usb = pd.read_csv('psam_husb.csv')

# Concatenate the datasets
df_combined = pd.concat([df_husa, df_usb], ignore_index=True)

# Save the combined dataframe to a new CSV file
df_combined.to_csv('psam_US.csv', index=False)

# Show the first 5 rows of the combined dataframe
print("First 5 rows of the combined dataframe:")
print(df_combined.head())
print("Last 5 rows of the combined dataframe:")
print(df_combined.tail())

# Clean column names (remove spaces)
df_combined.columns = df_combined.columns.str.strip()

# Convert relevant columns to numeric
df_combined['BROADBND'] = pd.to_numeric(df_combined['BROADBND'], errors='coerce')  # Broadband access
df_combined['WGTP'] = pd.to_numeric(df_combined['WGTP'], errors='coerce')  # Household weight
df_combined['ST'] = pd.to_numeric(df_combined['ST'], errors='coerce')  # State code

# Categorize as Urban, Suburban, or Rural
def classify_area(x):
    if x == 1:
        return "Urban"
    elif x == 2:
        return "Suburban"
    else:
        return "Rural"

df_combined['RuralUrban'] = df_combined['ACR'].apply(classify_area)

# Drop missing values in BROADBND and ST
df_combined = df_combined.dropna(subset=['BROADBND', 'ST'])

# Create a binary column for lack of broadband
df_combined['NoBroadband'] = df_combined['BROADBND'].apply(lambda x: 1 if x == 0 else 0)

# Calculate weighted counts
broadband_counts = df_combined.groupby(['ST', 'RuralUrban']).apply(
    lambda x: (x['NoBroadband'] * x['WGTP']).sum()
).reset_index(name='NoBroadband')

total_households = df_combined.groupby(['ST', 'RuralUrban'])['WGTP'].sum().reset_index(name='TotalHouseholds')

# Merge data
broadband_stats = broadband_counts.merge(total_households, on=['ST', 'RuralUrban'])

# Compute percentage correctly
broadband_stats['Percent_No_Broadband'] = (broadband_stats['NoBroadband'] / broadband_stats['TotalHouseholds']) * 100

# State code to abbreviation mapping
state_codes = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE', 
    11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 
    19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 
    26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 
    33: 'NH', 34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 
    40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 46: 'SD', 47: 'TN', 
    48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA', 54: 'WV', 55: 'WI', 
    56: 'WY'
}

# Add state abbreviations to the dataframe
broadband_stats['StateAbbr'] = broadband_stats['ST'].map(state_codes)

# Create bar plot
plt.figure(figsize=(15, 8))
sns.barplot(x='StateAbbr', y='Percent_No_Broadband', hue='RuralUrban', 
            data=broadband_stats, palette="Blues")

plt.title("Percentage of Households Without Broadband Access Per State\n(Urban vs. Suburban vs. Rural)", 
          fontsize=14, pad=20)
plt.xlabel("State")
plt.ylabel("Percentage Without Broadband (%)")
plt.xticks(rotation=45, ha='right')  # Rotate state codes for readability
plt.legend(title="Area Type")
plt.tight_layout()  # Adjust layout to prevent label cutoff

# Save the plot
plt.savefig('broadband_access_by_state.png', bbox_inches='tight', dpi=300)
plt.close()

# Create choropleth map for rural areas
rural_data = broadband_stats[broadband_stats['RuralUrban'] == 'Rural'].copy()

# Create the choropleth map
fig = px.choropleth(
    rural_data,
    locations='StateAbbr',
    locationmode='USA-states',
    color='Percent_No_Broadband',
    scope="usa",
    color_continuous_scale="Reds",
    range_color=[0, rural_data['Percent_No_Broadband'].max()],
    title='Percentage of Rural Households Without Broadband Access by State',
    labels={'Percent_No_Broadband': 'Percentage Without Broadband (%)'}
)

# Update layout
fig.update_layout(
    title_x=0.5,
    geo=dict(
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    ),
    margin=dict(r=20, t=40, l=20, b=20)
)

# Show the interactive map
fig.show()

# Save the map as HTML
fig.write_html('rural_broadband_map.html')

# Print summary statistics
print("\nBroadband Access Summary Per State & Rural/Urban Classification:")
summary_stats = broadband_stats.sort_values(['StateAbbr', 'RuralUrban'])[
    ['StateAbbr', 'RuralUrban', 'Percent_No_Broadband']
].round(2)
print(summary_stats.to_string(index=False))
