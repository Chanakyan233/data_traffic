import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Traffic Accident Analytics", page_icon="🚗", layout="wide")

st.title("🚗 Traffic Accident Analytics Dashboard")
st.markdown("Analyze traffic accident data and identify major contributing factors, trends, and hotspots.")

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()
        
    df = pd.read_csv(file_path)
    
    # 1. Clean the dataset
    # Drop rows where critical columns are missing
    df = df.dropna(subset=['Latitude', 'Longitude', 'Date', 'Time']).copy()
    
    # Fill remaining missing values with 'Unknown'
    df['Weather_Condition'] = df['Weather_Condition'].fillna('Unknown')
    df['Road_Condition'] = df['Road_Condition'].fillna('Unknown')
    df['Severity'] = df['Severity'].fillna('Unknown')
    
    # Parse Date & Time
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.hour
    df['Month'] = df['Date'].dt.month_name()
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    return df

# Load the dummy dataset
DATA_FILE = "traffic_accidents.csv"
df = load_data(DATA_FILE)

if df.empty:
    st.warning(f"⚠️ Dataset '{DATA_FILE}' not found. Please run `python generate_data.py` first to create dummy data.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

# City filter
cities = ["All"] + list(df['City'].unique())
selected_city = st.sidebar.selectbox("Select City", cities)

# Weather filter
weathers = ["All"] + list(df['Weather_Condition'].dropna().unique())
selected_weather = st.sidebar.selectbox("Weather Condition", weathers)

# Severity filter
severities = ["All"] + list(df['Severity'].unique())
selected_severity = st.sidebar.selectbox("Severity Level", severities)

# Apply filters
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_weather != "All":
    filtered_df = filtered_df[filtered_df['Weather_Condition'] == selected_weather]
if selected_severity != "All":
    filtered_df = filtered_df[filtered_df['Severity'] == selected_severity]


# --- KPI CARDS (Overview) ---
st.markdown("### 📊 Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_accidents = len(filtered_df)
kpi1.metric(label="Total Accidents", value=total_accidents)

# Most dangerous hour
if not filtered_df.empty:
    dangerous_hour = int(filtered_df['Hour'].mode()[0])
    # Formatting hour nicely
    kpi2.metric(label="Most Dangerous Time", value=f"{dangerous_hour}:00")
else:
    kpi2.metric(label="Most Dangerous Time", value="N/A")

# Most affected location (City)
if not filtered_df.empty:
    most_affected_city = filtered_df['City'].mode()[0]
    kpi3.metric(label="Most Affected City", value=most_affected_city)
else:
    kpi3.metric(label="Most Affected City", value="N/A")

# Highest severity count
if not filtered_df.empty:
    fatal_severe = filtered_df[filtered_df['Severity'].isin(['Fatal', 'Severe'])].shape[0]
    kpi4.metric(label="Severe/Fatal Incidents", value=fatal_severe)
else:
    kpi4.metric(label="Severe/Fatal Incidents", value=0)

st.divider()

if filtered_df.empty:
    st.info("No data available for the applied filters.")
    st.stop()

# --- TABS FOR DIFFERENT SECTIONS ---
tab1, tab2, tab3 = st.tabs(["📉 Analysis Visualizations", "🗺️ Hotspots Map", "🔍 Correlation & Data Insights"])

with tab1:
    st.subheader("Data Distributions and Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart: Severity Distribution
        severity_counts = filtered_df['Severity'].value_counts().reset_index()
        severity_counts.columns = ['Severity', 'Count']
        fig_pie = px.pie(
            severity_counts, 
            names='Severity', 
            values='Count',
            title='Accident Severity Distribution',
            color='Severity',
            color_discrete_map={
                'Fatal': 'darkred',
                'Severe': 'red',
                'Moderate': 'orange',
                'Low': 'green',
                'Unknown': 'gray'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar Chart: Accidents by Weather Condition
        weather_counts = filtered_df['Weather_Condition'].value_counts().reset_index()
        weather_counts.columns = ['Weather Condition', 'Accident Count']
        fig_bar = px.bar(
            weather_counts, 
            x='Weather Condition', 
            y='Accident Count',
            title='Accidents by Weather Condition',
            color='Weather Condition'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart: Accidents over Time (Trend Tracker)
    st.markdown("#### Accidents Over Time (Trends)")
    time_series = filtered_df.groupby('Date').size().reset_index(name='Daily Accidents')
    fig_line = px.line(time_series, x='Date', y='Daily Accidents', title='Daily Accident Trend')
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar Chart: Time of Day
    st.markdown("#### Accidents by Hour of Day")
    hour_counts = filtered_df.groupby('Hour').size().reset_index(name='Count')
    fig_hour = px.bar(hour_counts, x='Hour', y='Count', title='Accidents by Time of Day')
    fig_hour.update_layout(xaxis_title='Hour of the Day (0-23)', yaxis_title='Number of Accidents')
    st.plotly_chart(fig_hour, use_container_width=True)

with tab2:
    st.subheader("Accident Hotspots Geospatial View")
    st.markdown("Interactive map showing accident locations. Use the zoom/pan features. Red = Fatal/Severe, Orange = Moderate, Blue = Low.")
    
    # Map colors
    def assign_color(severity):
        if severity == 'Fatal':
            return '#8B0000' # Dark Red
        elif severity == 'Severe':
            return '#FF0000' # Red
        elif severity == 'Moderate':
            return '#FFA500' # Orange
        else:
            return '#0000FF' # Blue (Low/Unknown)
            
    filtered_df['MapColor'] = filtered_df['Severity'].apply(assign_color)
    
    fig_map = px.scatter_mapbox(
        filtered_df, 
        lat="Latitude", 
        lon="Longitude", 
        color="Severity",
        hover_name="City",
        hover_data=["Date", "Time", "Weather_Condition", "Severity"],
        color_discrete_map={
            'Fatal': '#8B0000',
            'Severe': '#FF0000',
            'Moderate': '#FFA500',
            'Low': '#008000', # Green for low
            'Unknown': 'gray'
        },
        zoom=3.5 if selected_city == "All" else 10,
        height=600
    )
    
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.subheader("Data Insights & Correlations")
    
    st.markdown("### Processed Dataset Preview")
    st.dataframe(filtered_df.head(50)) # Show first 50 rows
    
    st.markdown("### Analyzing Frequency Patterns")
    # Cross-tabulation heatmap for hours vs severity
    st.markdown("#### Time vs. Severity Heatmap")
    
    pivot_table = pd.crosstab(filtered_df['Hour'], filtered_df['Severity'])
    fig_heatmap = px.imshow(
        pivot_table.T, 
        text_auto=True, 
        color_continuous_scale='Reds',
        aspect="auto",
        title="Severity vs Time of Day Heatmap"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("#### Weather vs. Road Condition Crosstab")
    weather_road = pd.crosstab(filtered_df['Weather_Condition'], filtered_df['Road_Condition'])
    st.dataframe(weather_road.style.background_gradient(cmap='Blues'))

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Python & Streamlit 🚀")
