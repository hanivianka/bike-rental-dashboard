# Bike Rental Analysis Dashboard

This project is an interactive dashboard built with Streamlit that analyzes bike rental data from the Capital Bikeshare system in Washington D.C., USA, from 2011 to 2012.

## Features

The dashboard offers the following analysis types:

1. **Hourly Rental**: Displays the average bike rental per hour throughout the day.
2. **Daily Rental**: Analyzes the average bike rental per weekday.
3. **Regular Day vs Holiday**: Compares the total bike rentals on regular days versus holidays.
4. **Yearly Trend**: Shows the monthly bike rental trend for the years 2011 and 2012.
5. **Weather Impact**: Analyzes how different weather conditions affect bike rental.
6. **Seasonal Impact**: Analyzes how different season affect bike rental.
7. **Temperature Impact**: Shows the average bike rental by temperature ranges.

## Installation

To run this dashboard locally:

1. Ensure you have Python installed (Python 3.7 or higher).
2. Install the required Python packages:
    ```bash
    pip install streamlit pandas matplotlib seaborn
    ```
3. Place the `data_hour.csv` and `data_day.csv` files in the same directory as the Python script.

4. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
