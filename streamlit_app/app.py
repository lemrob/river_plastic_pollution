# streamlit_app/app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---- 1. Load Data (Replace with your own) ----
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\\Users\\liamr\\OneDrive\\Documents\\Playground\\backup\\river_plastic_pollution\\data\\monthly_pollution_df.csv')
    return df

df = load_data()

# ---- 2. Streamlit UI ----
st.title("📊 Seasonal River Pollution in SE Asia")
st.subheader("Visualizing Top 10 Rivers from The Ocean Cleanup Ranking")

# Slider for month (you can customize with real month names if needed)
month = st.slider("Select month", 1, 12, 6)

# Toggle between normalized and raw
# pollution_type = st.radio("Pollution Type", ["Raw", "Normalized"])

# ---- 3. Filter Data Based on Selections ----
# col = 'pollution_raw' if pollution_type == 'Raw' else 'pollution_norm'
df_month = df[df['month'] == month]

# ---- 4. Map Creation ----
m = folium.Map(location=[10, 105], zoom_start=5, tiles="CartoDB positron")

# Plot each river
for _, row in df_month.iterrows():
    pollution_value = row['monthly_pollution']  # Adjust based on your data
    # folium.CircleMarker(
        # need to iterate through the lat and lon of each river
        # and create a circle marker for each one  
    for i in range(len(row['lat'])):
        folium.CircleMarker(
            location=[row['lat'][i], row['lon'][i]],
            radius=6 + pollution_value[i] * 10,  # Scaled size
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['rank']}<br>Country: {row['country']}<br>Pollution: {pollution_value:.2f}"
        ).add_to(m)



        # location=[row['lat'], row['lon']],
        # radius=6 + pollution_value * 10,  # Scaled size
        # color='red',
        # fill=True,
        # fill_opacity=0.7,
    

# Show map
st_data = st_folium(m, width=800, height=550)
