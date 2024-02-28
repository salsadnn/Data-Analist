import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from streamlit_lottie import st_lottie
import requests

# Page configuratio
st.set_page_config(
    page_title="Bicycle Rental Data",
    layout="wide",
    initial_sidebar_state="expanded")

# Load data
df = pd.read_csv('Dashbord/day.csv')
df['dteday'] = pd.to_datetime(df['dteday'])  # Convert 'dteday' to datetime
#animasi
def load_lottieurl(url):
	r = requests.get(url)
	if r.status_code != 200:
		return None
	return r.json()
lottie_bike = load_lottieurl("https://lottie.host/850ab89a-534b-4e08-a782-0e92fce6a82e/worx94cr32.json")
# --- Header Section ---
with st.container():
    st.header("Bicycle Rental Data 🚲")
with st.container():
	st.write("---")
	left_column, right_column = st.columns(2)
	with left_column:
		st.subheader("Below is Bike Sharing Data")
		st.write("##")
		st.write(
		"""
        Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return 
        back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return 
        back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of 
        over 500 thousands bicycles.
		"""
		)
	with right_column:
		st_lottie(lottie_bike, height=300, key="coding")
# Sidebar
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()
with st.sidebar:
    st.title('Bicycle Rental Data 🚲')
    st.image("Dashbord/Image/salsa.jpg")
    # Input tanggal untuk rentang waktu
    selected_dates = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Mengambil start_date & end_date dari input tanggal
    start_date, end_date = selected_dates
    st.sidebar.header("Please Filter Here:")
    season = st.sidebar.multiselect(
        "Select the Season:",
        options=df["season"].unique(),
        default=df["season"].unique()
    )

    weather = st.sidebar.multiselect(
        "Select the Weather Situation:",
        options=df["weathersit"].unique(),
        default=df["weathersit"].unique(),
    )

    working_day = st.sidebar.multiselect(
        "Select Working Day or Not:",
        options=df["workingday"].unique(),
        default=df["workingday"].unique()
    )

    # Filter data berdasarkan pilihan pengguna
    df_selection = df.query(
        "season == @season & weathersit == @weather & workingday == @working_day & @start_date <= dteday <= @end_date"
    )

# Visualizations
# Grafik total penyewaan berdasarkan musim (season)
rentals_by_season = df_selection.groupby(by=["season"])[["cnt"]].sum()
fig_season_rentals = px.bar(
    rentals_by_season,
    x=rentals_by_season.index,
    y="cnt",
    title="<b>Rentals by Season</b>",
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig_season_rentals.update_layout(
    xaxis_title="Season",
    yaxis_title="Total Rentals",
)

# Grafik total penyewaan berdasarkan kondisi cuaca (weather situation)
rentals_by_weather = df_selection.groupby(by=["weathersit"])[["cnt"]].sum()
fig_weather_rentals = px.bar(
    rentals_by_weather,
    x=rentals_by_weather.index,
    y="cnt",
    title="<b>Rentals by Weather Situation</b>",
    color_discrete_sequence=px.colors.qualitative.Alphabet,
)
fig_weather_rentals.update_layout(
    xaxis_title="Weather Situation",
    yaxis_title="Total Rentals",
)

# Grafik total penyewaan berdasarkan hari kerja (working day)
rentals_by_working_day = df_selection.groupby(by=["workingday"])[["cnt"]].sum()
fig_working_day_rentals = px.bar(
    rentals_by_working_day,
    x=rentals_by_working_day.index,
    y="cnt",
    title="<b>Rentals by Working Day</b>",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)
fig_working_day_rentals.update_layout(
    xaxis_title="Working Day",
    yaxis_title="Total Rentals",
)

# Grafik total penyewaan berdasarkan libur (holiday)
rentals_by_holiday = df_selection.groupby(by=["holiday"])[["cnt"]].sum()
fig_holiday_rentals = px.bar(
    rentals_by_holiday,
    x=rentals_by_holiday.index,
    y="cnt",
    title="<b>Rentals by Holiday</b>",
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig_holiday_rentals.update_layout(
    xaxis_title="Holiday",
    yaxis_title="Total Rentals",
)

# Grafik total penyewaan berdasarkan musim (season) dengan tipe grafik histogram
fig_season_rentals_bar = px.histogram(
    df_selection,
    x="season",
    y="cnt",
    title="Rentals by Season",
    color_discrete_sequence=px.colors.qualitative.T10,
)
fig_season_rentals_bar.update_layout(
    xaxis_title="Season",
    yaxis_title="Total Rentals",
)

# Grafik total penyewaan berdasarkan hari dalam seminggu (weekday)
fig_day_of_week_rentals = px.bar(
    df_selection.groupby(by=["weekday"])[["cnt"]].sum(),
    x=df_selection.groupby(by=["weekday"])[["cnt"]].sum().index,
    y="cnt",
    title="Rentals by Day of Week",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig_day_of_week_rentals.update_layout(
    xaxis_title="Day of Week",
    yaxis_title="Total Rentals",
)

# Menampilkan visualisasi
col1, col2 = st.columns(2)
col1.plotly_chart(fig_season_rentals, use_container_width=True)
col2.plotly_chart(fig_weather_rentals, use_container_width=True)

st.plotly_chart(fig_working_day_rentals, use_container_width=True)
st.plotly_chart(fig_holiday_rentals, use_container_width=True)
st.plotly_chart(fig_season_rentals_bar, use_container_width=True)
st.plotly_chart(fig_day_of_week_rentals, use_container_width=True)
