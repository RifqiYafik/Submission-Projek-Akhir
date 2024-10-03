import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set tema
sns.set_theme(style='dark')

# Function to create monthly rentals DataFrame
def create_monthly_rentals_df(df):
    monthly_rentals = df.groupby(['mnth', 'holiday'])['cnt'].sum().reset_index()
    monthly_rentals['holiday'] = monthly_rentals['holiday'].map({0: 'Working Day', 1: 'Holiday'})
    return monthly_rentals

# Function to create peak hours DataFrame
def create_peak_hours_df(df):
    peak_hours = df.groupby('hr')['cnt'].sum().reset_index()
    peak_hours = peak_hours.sort_values(by='cnt', ascending=False).head(5)
    return peak_hours

# Function to create hourly rentals DataFrame
def create_hourly_rentals_df(df):
    hourly_rentals = df.groupby('hr')['cnt'].sum().reset_index()
    return hourly_rentals

# Function to classify busy and quiet hours
def classify_busy_quiet_hours(df):
    busy_hours = df['cnt'] > df['cnt'].mean()
    df['hour_type'] = ['Busy' if busy else 'Quiet' for busy in busy_hours]
    return df

# Load data
day_data_cleaned = pd.read_csv("dashboard/day.csv")
day_data_cleaned = pd.read_csv("dashboard/hour.csv")

# Sidebar for filtering
with st.sidebar:
    day_data_cleaned["dteday"] = pd.to_datetime(day_data_cleaned["dteday"])
    min_date = day_data_cleaned["dteday"].min()
    max_date = day_data_cleaned["dteday"].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on the selected date range
day_data_cleaned = day_data_cleaned[(day_data_cleaned["dteday"] >= pd.to_datetime(start_date)) & (day_data_cleaned["dteday"] <= pd.to_datetime(end_date))]

st.header('Bike Sharing Dashboard :sparkles:')

# Monthly Rentals Comparison
monthly_rentals = create_monthly_rentals_df(day_data_cleaned)
st.subheader('1. Comparison of Bicycle Rentals on Weekdays and Holidays')
st.write('>>> Thisi Is The Bar Chart :')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='mnth', 
    y='cnt', 
    hue='holiday', 
    data=monthly_rentals, 
    palette={'Holiday': 'red', 'Working Day': 'grey'}, 
    ax=ax
)

plt.title('Total Bike Rentals per Month', fontsize=15)
plt.xlabel('Month')
plt.ylabel('Total Rentals (cnt)')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig)


# Hourly Rentals Analysis
hourly_rentals = create_hourly_rentals_df(day_data_cleaned)
hourly_rentals = classify_busy_quiet_hours(hourly_rentals)

# Line Chart for Hourly Rentals
st.subheader('2. Jam berapa saja waktu puncak untuk penyewaan sepeda?')
st.subheader('>>> Diagram Garisnya :')

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, marker='o', ax=ax)

plt.title('Total Rentals Per Hour', fontsize=15)
plt.xlabel('Hour of the Day')
plt.ylabel('Total Rentals (cnt)')
st.pyplot(fig)

# Peak Hours Analysis
peak_hours = create_peak_hours_df(day_data_cleaned)
st.write('>>> Bar Chart Top 5 Peak Hours for Bike Rentals')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='hr', 
    y='cnt', 
    data=peak_hours, 
    ax=ax
)

plt.title('Top 5 Peak Hours for Bike Rentals', fontsize=15)
plt.xlabel('Hour of the Day')
plt.ylabel('Total Rentals (cnt)')
st.pyplot(fig)


# Busy and Quiet Hours Analysis
st.subheader('>>>Comparison of Busy Hours VS Quiet Hours')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='hr', 
    y='cnt', 
    hue='hour_type', 
    data=hourly_rentals, 
    palette={'Busy': 'orange', 'Quiet': 'blue'}, 
    ax=ax
)

plt.title('Busy and Quiet Hours', fontsize=15)
plt.xlabel('Hour of the Day')
plt.ylabel('Total Rentals (cnt)')
st.pyplot(fig)

st.write('Rifqi Yafik')
