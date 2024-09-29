import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
data_hour = pd.read_csv('dashboard/data_hour.csv')
data_day = pd.read_csv('dashboard/data_day.csv')
data_hour['date'] = pd.to_datetime(data_day['date'])
data_day['date'] = pd.to_datetime(data_day['date'])

# Helper function

def create_hourly_avg(data_hour):
    hourly_avg = data_hour.groupby('hour')['count'].mean().reset_index()
    hourly_avg.columns = ['hour', 'count_avg']
    hourly_avg = hourly_avg.sort_values(by='count_avg', ascending=False)
    return hourly_avg

def create_daily_avg(data_hour):
    daily_avg = data_hour.groupby('weekday')['count'].mean().reset_index()
    daily_avg.columns = ['weekday', 'count_avg']
    daily_avg = daily_avg.sort_values(by='count_avg', ascending=False)
    return daily_avg

def create_weather_rental(data_hour):
    clear = data_hour[data_hour['weathersit'] == 'Clear/Partly Cloudy']['count'].sum()
    mist = data_hour[data_hour['weathersit'] == 'Mist/Cloudy']['count'].sum()
    light = data_hour[data_hour['weathersit'] == 'Light Snow/Rain']['count'].sum()
    heavy = data_hour[data_hour['weathersit'] == 'Heavy Rain/Thunderstorm']['count'].sum()

    clear_percentage = (clear / (clear + mist + light + heavy)) * 100
    mist_percentage = (mist / (clear + mist + light + heavy)) * 100
    light_percentage = (light / (clear + mist + light + heavy)) * 100
    heavy_percentage = (heavy / (clear + mist + light + heavy)) * 100

    weather_rental = pd.DataFrame({
        'category': ['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Thunderstorm'],
        'count_sum': [clear, mist, light, heavy],
        'percentage': [clear_percentage, mist_percentage, light_percentage, heavy_percentage]
    })
    return weather_rental

def create_temp_rental(data_hour):
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    data_hour['temp_bin'] = pd.cut(data_hour['temp'], bins=bins, labels=labels, include_lowest=True)
    temp_rental = data_hour.groupby('temp_bin', observed=False)['count'].mean().reset_index()
    temp_rental.columns = ['category', 'count_avg']
    return temp_rental

def create_rental_day(data_day):
    regular_day = data_day[data_day['holiday'] == 0]['count'].sum()
    holiday = data_day[data_day['holiday'] == 1]['count'].sum()

    regular_day_percentage = (regular_day / (regular_day + holiday)) * 100
    holiday_percentage = (holiday / (regular_day + holiday)) * 100

    rental_day = pd.DataFrame({
        'category': ['Regular Day', 'Holiday'],
        'count_sum': [regular_day, holiday],
        'percentage': [regular_day_percentage, holiday_percentage]
    })
    return rental_day

def create_yearly_trend(data_day):
    data_day['year'] = data_day['date'].dt.year
    data_day['month'] = data_day['date'].dt.month
    yearly_trend = data_day.groupby(['year', 'month'])['count'].sum().reset_index()
    return yearly_trend

def create_season_rental(data_day):
    spring = data_day[data_day['season'] == 'Spring']['count'].sum()
    summer = data_day[data_day['season'] == 'Summer']['count'].sum()
    fall = data_day[data_day['season'] == 'Fall']['count'].sum()
    winter = data_day[data_day['season'] == 'Winter']['count'].sum()

    spring_percentage = (spring / (spring + summer + fall + winter)) * 100
    summer_percentage = (summer / (spring + summer + fall + winter)) * 100
    fall_percentage = (fall / (spring + summer + fall + winter)) * 100
    winter_percentage = (winter / (spring + summer + fall + winter)) * 100

    season_rental = pd.DataFrame({
        'category': ['Spring', 'Summer', 'Fall', 'Winter'],
        'count_sum': [spring, summer, fall, winter],
        'percentage': [spring_percentage, summer_percentage, fall_percentage, winter_percentage]
    })
    return season_rental

# Set up various dataframes
hourly_avg = create_hourly_avg(data_hour)
daily_avg = create_daily_avg(data_hour)
weather_rental = create_weather_rental(data_hour)
temp_rental = create_temp_rental(data_hour)
rental_day = create_rental_day(data_day)
yearly_trend = create_yearly_trend(data_day)
season_rental = create_season_rental(data_day)

# Sidebar
with st.sidebar:
    st.title("Bike Rental Analysis Dashboard")
    st.write("")
    st.image('dashboard/bike-rental.png', use_column_width=True)
    st.write("")
    st.markdown(
        """
        The dashboard analyzes bike rental data from the Capital Bikeshare system, 
        Washington D.C., USA from 2011 to 2012.
        """
    )

# Dropdown for selecting analysis type
st.title("Select Analysis Type")
option = st.selectbox(
    'Choose analysis type:',
    ('Hourly Rental', 'Daily Rental', 'Regular day and Holiday',  'Yearly Trend', 'Weather Impact', 'Seasonal Impact', 'Temperature Impact')
)

if option == 'Hourly Rental':
    st.subheader('Average Hourly Bike Rental')
    max_avg = hourly_avg['count_avg'].max()
    max_hour = hourly_avg[hourly_avg['count_avg'] == max_avg]['hour'].values[0]

    plt.figure(figsize=(5, 3))
    bars = plt.bar(hourly_avg['hour'], hourly_avg['count_avg'], color='skyblue')

    for bar in bars:
        if bar.get_x() + bar.get_width()/2 == max_hour:
            bar.set_color('salmon')

    plt.text(max_hour, max_avg, "{:.2f}".format(max_avg), ha='center', va='bottom', color='black', fontsize=7)

    plt.xlabel('Hours', fontsize=8)
    plt.ylabel('Average Amount of Rental', fontsize=8)
    plt.xticks(hourly_avg['hour'], fontsize=7)
    plt.yticks(fontsize=8)
    plt.grid(axis='y')
    
    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            From the “Average Hourly Bike Rental” chart, it can be seen that the average bike rental varies throughout the day. 
            18:00 shows the highest amount of rental, with the average value reaching 461.45, indicated in red.
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Daily Rental':
    st.subheader('Average Daily Bike Rental')
    daily_avg = daily_avg.sort_values(by='weekday')

    max_avg = daily_avg['count_avg'].max()
    max_day = daily_avg[daily_avg['count_avg'] == max_avg]['weekday'].values[0]

    day_labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    plt.figure(figsize=(7, 4))
    bars = plt.barh(daily_avg['weekday'], daily_avg['count_avg'], color='skyblue')

    for bar in bars:
        if bar.get_width() == max_avg:
            bar.set_color('salmon')

    plt.text(max_avg, max_day, "{:.2f}".format(max_avg), ha='right', va='center', color='black')

    plt.xlabel('Average Amount of Rental')
    plt.ylabel('Days')
    plt.yticks(ticks=daily_avg['weekday'], labels=day_labels)
    plt.grid(axis='x')

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            Based on the “Average Daily Bike Rental” chart, the analysis shows that Thursday is the most popular day to rent a bike, 
            with the average reaching 196.44, indicated in red.
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Regular day and Holiday':
    st.subheader('Comparison of Bike Rental on Regular Day and Holiday')
    plt.figure(figsize=(5, 3))
    plt.pie(rental_day['percentage'], labels=rental_day['category'], autopct='%1.2f%%', colors=['skyblue', 'orange'], textprops={'fontsize': 8})
    plt.axis('equal')
    plt.legend(rental_day['category'], fontsize=8)

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            The “Comparison of Bike Rental on Regular Day and Holiday” chart shows that 97.62% of bike rental occurs on regular days, 
            indicating a very high preference compared to holidays.
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Yearly Trend':
    st.subheader('Bike Rental Trend between 2011 and 2012')
    data_2011 = yearly_trend[yearly_trend['year'] == 2011]
    data_2012 = yearly_trend[yearly_trend['year'] == 2012]

    plt.figure(figsize=(7, 5))
    plt.plot(data_2011['month'], data_2011['count'], marker='o', label='2011')
    plt.plot(data_2012['month'], data_2012['count'], marker='o', label='2012')
    plt.xlabel('Month')
    plt.ylabel('Rental Amount')
    plt.xticks(ticks=data_2011['month'], labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year')
    plt.grid()

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            From the “Bike Rental Trend between 2011 and 2012” chart, it can be seen that bike rental fluctuates from month to month. 
            However, overall, there is an increasing trend in the amount of bike rental from year to year.
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Weather Impact':
    st.subheader('Bike Rental Distribution by Weather')
    plt.figure(figsize=(7, 5))
    plt.pie(weather_rental['percentage'], labels=weather_rental['category'], autopct='%1.2f%%', colors=['skyblue', 'lightgreen', 'orange', 'salmon'])
    plt.axis('equal')
    plt.legend(weather_rental['category'], bbox_to_anchor=(1, 1), loc="upper left")

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            The “Bike Rental Distribution by Weather” chart shows that 71.01% of renters choose to rent a bike during “Clear/Partly Cloudy” weather, followed by 24.17% during “Mist/Cloudy”, 
            4.81% during “Light Snow/Rain”, and only 0.01% during “Heavy Rain/Thunderstorm”.
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Seasonal Impact':
    st.subheader('Bike Rental Distribution by Seaso')
    plt.figure(figsize=(5, 3))
    plt.pie(season_rental['percentage'], labels=season_rental['category'], autopct='%1.2f%%', colors=['lightgreen', 'salmon', 'orange', 'lightblue'], textprops={'fontsize': 8})
    plt.axis('equal')
    plt.legend(season_rental['category'], fontsize=6)

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            From the “Bike Rental Distribution by Season” chart, Fall is the most popular season with 32.23% of the total rentals, 
            followed by Summer (27.90%), Winter (25.56%), and Spring (14.32%).
        </div>
        """, 
        unsafe_allow_html=True
    )

elif option == 'Temperature Impact':
    st.subheader('Average Bike Rental by Temperature Range')
    max_avg = temp_rental['count_avg'].max()
    max_bin = temp_rental[temp_rental['count_avg'] == max_avg]['category'].values[0]

    plt.figure(figsize=(5, 3))
    bars = plt.bar(temp_rental['category'], temp_rental['count_avg'], color='lightblue')

    for bar in bars:
        if bar.get_x() + bar.get_width()/2 == temp_rental[temp_rental['category'] == max_bin].index[0]:
            bar.set_color('salmon')
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', color='black', fontsize=8)

    plt.xlabel('Temperature Range', fontsize=8)
    plt.ylabel('Average Amount of Rental', fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(axis='y')

    st.pyplot(plt)

    st.markdown(
        """
        <div style='font-size:18px;'>
            <b>Insight:</b><br>
            There is a trend that the higher the temperature, the more bikes are rented. The temperature 
            category “Very High” shows the highest average bike rental with 326.28.
        </div>
        """, 
        unsafe_allow_html=True
    )
