import streamlit as st
import requests
import datetime
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Quick reference", # => Quick reference - Streamlit
    page_icon="image/taxi.png",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

st.sidebar.markdown(f"""
    # Book a taxi
    # Book an hotel
    # Book an parc

    """)

FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: 32px !important;
}}
</style>
"""
st.write(FONT_SIZE_CSS, unsafe_allow_html=True)

# Coordonnées centrales de Manhattan
manhattan_center = [40.7831, -73.9712]

# Créer une carte folium centrée sur Manhattan
m = folium.Map(location=manhattan_center, zoom_start=13)
folium.TileLayer('cartodbpositron').add_to(m)

# Ajouter des limites de Manhattan pour référence
manhattan_geojson = "https://raw.githubusercontent.com/dwillis/nyc-maps/master/manhattan.geojson"
#folium.GeoJson(
#    manhattan_geojson,
#    name='Manhattan',
#    style_function=lambda x: {'fillColor': 'transparent', 'color': '#3186cc', 'weight': 2}
#).add_to(m)

folium_static(m)

d = st.date_input(
    "When do you want ?",
    datetime.date(2025, 3, 14))
st.write('the date is :', d)

t = st.time_input('What time ?', datetime.time(8, 45))

st.write('time is :', t)

lonpick = st.number_input('What is the starting longitude?')
st.write('The longitude is :', lonpick)

latpick = st.number_input('What is the starting latitude?')
st.write('The longitude is :', latpick)


londrop = st.number_input('what is the arriving longitude ?')
st.write('The longitude is :', londrop)

latdrop = st.number_input('what is the arriving latitude ?')
st.write('The longitude is :', latdrop)

def get_select_box_data():

    return pd.DataFrame({
          'first column': list(range(1, 5)),
        })

df = get_select_box_data()

option = st.selectbox('Select number of passengers', df['first column'])
filtered_df = df[df['first column'] == option]

#st.write(filtered_df)


#datetime = str(d) + ' ' + str(t)
datetime_ = f"{d} {t}"
url = 'https://taxifare.lewagon.ai/predict'
params = {
        'pickup_datetime':pd.Timestamp(datetime_, tz='UTC'),
        'pickup_longitude':lonpick,
        'pickup_latitude': latpick,
        'dropoff_longitude': londrop,
        'dropoff_latitude': latdrop,
        'passenger_count': filtered_df
}


if londrop and lonpick and latpick and latdrop:
    response = requests.get(url, params=params).json()
    st.write('estimated cost is :', response.get('fare',0))
