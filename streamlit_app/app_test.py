# streamlit_app/app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---- 1. Load Data (Replace with your own) ----
@st.cache_data
def load_data():
    df = pd.read_pickle(r'C:\\Users\\liamr\\OneDrive\\Documents\\Playground\\backup\\river_plastic_pollution\\data\\monthly_pollution_gdf.pkl')
    return df

gdf = load_data()

# ---- 2. Streamlit UI ----
st.title("📊 Seasonal River Pollution in SE Asia")
st.subheader("Visualizing Top 10 Rivers from The Ocean Cleanup Ranking")

# ---- 3. Filter Data Based on Selections ----
# col = 'pollution_raw' if pollution_type == 'Raw' else 'pollution_norm'
# df_month = df[df['month'] == month]

col = 'monthly_pollution'
max_pollution = gdf['monthly_pollution'].max()
min_pollution = gdf['monthly_pollution'].min()

# Inside your loop

# Slider for month (you can customize with real month names if needed)
month = st.slider("Select month", 1, 12, 1)

# Create a geometry list from the GeoDataFrame
geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]


# Setting up the map to centre on Southeast Asia
map_center = [9.4581963681147, 120.76606274396]
m = folium.Map(location=map_center, zoom_start=4) # Add zoom_start for initial view


# Plot each river
for _, row in gdf.iterrows():
    pollution_value = row[col]
    normalized = (pollution_value - min_pollution) / (max_pollution - min_pollution)
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius = 5 + normalized * 15,  # Now radius is always between 5 and 20
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup=f"Pollution Rank: {row['rank']}<br>Pollution Volume: {pollution_value:.2f}"
    ).add_to(m)


# Use st_folium to render the map
st_data = st_folium(m, width=700, height=500)



#####

# Iterate through list and add a marker for each river mouth
# i = 0
# for coordinates in geo_df_list:
#         # Place the markers with the popup labels and data
#     m.add_child(
#         folium.Marker(
#             location=coordinates,
#             popup="Pollution: "
#             + str(gdf['monthly_pollution'][i])
#             + "<br>"
#             + "Country: "
#             + str(gdf['country'][i])
#             + "<br>"
#             + "Top 10 Rank: "
#             + str(gdf['rank'][i])
#             + "<br>"
#             + "Coordinates: "
#             + str(geo_df_list[i]),
#             icon=folium.Icon(color="%s" ),
#         )
#     )

#     i = i + 1