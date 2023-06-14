import pandas as pd
import plotly.express as px

# Load the data into a DataFrame (assuming the data is stored in a CSV file)
data = pd.read_csv('Aemf1.csv')


def get_price_info(city):
    # Filter the data for the specified city
    city_data = data[data['City'] == city]

    # Calculate average price, cleanliness, and guest satisfaction for the city
    average_price = city_data['Price'].mean()
    average_cleanliness = city_data['Cleanliness Rating'].mean()
    average_guest_satisfaction = city_data['Guest Satisfaction'].mean()

    # Create a distribution plot for the price
    price_distribution = px.histogram(city_data, x='Price', nbins=20,
                                      title=f'Price Distribution in {city}')
    price_distribution.update_layout(
        xaxis=dict(title='Price'),
        yaxis=dict(title='Count'),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        font=dict(color='white'),
        title_font=dict(family='Arial', size=24, color='white')
    )

    return price_distribution, average_cleanliness, average_guest_satisfaction

def get_room(city):
    # Filter the data for the specified city
    city_data = data[data['City'] == city]

    # Count the occurrences of each room type
    room_counts = city_data['Room Type'].value_counts().reset_index()

    # Create a pie chart for room type distribution
    room_chart = px.pie(room_counts, values='Room Type', names='index',
                        title=f'Room Type Distribution in {city}', hole=0.5)
    room_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        font=dict(color='white'),
        title_font=dict(family='Arial', size=24, color='white')
    )

    return room_chart
