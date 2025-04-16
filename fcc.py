#import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#load Fcc with BlockID.csv
df = pd.read_csv('Fcc with BlockID.csv')

#show the first 5 rows of the dataframe
print(df.head())

# Convert relevant speed/capacity columns to numeric, coercing errors if any
cols_to_convert = ['MaxAdDown', 'MaxAdUp']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Define a threshold for what is considered "adequate" broadband
adequate_download = 25  # for example, 25 Mbps minimum download speed

# Create a new flag column for adequate broadband service
df['Adequate_Broadband'] = df['MaxAdDown'] >= adequate_download

# Optionally, view statistics by technology type (e.g., DSL, cable, fiber) using TechCode
tech_stats = df.groupby('TechCode')[['MaxAdDown', 'MaxAdUp']].agg(['mean','median','min','max'])
print(tech_stats)

# Group by state using StateAbbr to compute average speeds
state_grouped = df.groupby('StateAbbr')[['MaxAdDown', 'MaxAdUp']].mean().reset_index()
print(state_grouped)

# Bar chart to compare average download speeds by state
plt.figure(figsize=(10,6))
sns.barplot(x='StateAbbr', y='MaxAdDown', data=state_grouped)
plt.title('Average Max Advertised Download Speed by State')
plt.xlabel('State')
plt.ylabel('Average Max Advertised Download Speed (Mbps)')
plt.xticks(rotation=45)
plt.savefig('Average Max Advertised Download Speed by State.png')
plt.close()

# Create choropleth map using plotly express
fig = px.choropleth(
    state_grouped,
    locations='StateAbbr',
    locationmode='USA-states',
    color='MaxAdDown',
    scope="usa",
    color_continuous_scale="Blues",  # Changed back to Blues for better visibility
    title='Broadband Speeds Across US States (Max Advertised Download Speed)',
    hover_name='StateAbbr',  # Show state abbreviation in hover
    hover_data={'StateAbbr': False,  # Hide duplicate state abbr
                'MaxAdDown': ':.1f'},  # Format speed to 1 decimal place
    labels={'MaxAdDown': 'Max Download Speed (Mbps)'}  # Better label for legend
)

# Update the layout for better visualization
fig.update_layout(
    geo=dict(
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    ),
    width=1000,
    height=600
)

# Customize the hover template
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>" +
    "Download Speed: %{z:.1f} Mbps<extra></extra>"
)

# Show the interactive map
fig.show()

# Save the map as an HTML file
fig.write_html('Broadband_Speeds_Across_US_States.html')

