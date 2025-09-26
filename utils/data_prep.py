"""
Data preparation utilities for Roomify pricing dashboard.
Generates synthetic but realistic pricing data for hotel revenue optimization.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_pricing_data(start_date='2022-01-01', end_date='2023-12-31', seed=42):
    """
    Generate 2 years of synthetic hotel pricing data with realistic patterns.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        seed (int): Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Synthetic pricing data
    """
    np.random.seed(seed)
    random.seed(seed)
    
    # Create date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(date_range)
    
    data = []
    
    # Define seasonal patterns
    seasons = {
        'low': ['2022-01-01', '2022-03-15', '2022-11-01', '2022-12-15'],
        'medium': ['2022-03-16', '2022-05-31', '2022-09-01', '2022-10-31'],
        'high': ['2022-06-01', '2022-08-31', '2022-12-16', '2022-12-31'],
        'low_2023': ['2023-01-01', '2023-03-15', '2023-11-01', '2023-12-15'],
        'medium_2023': ['2023-03-16', '2023-05-31', '2023-09-01', '2023-10-31'],
        'high_2023': ['2023-06-01', '2023-08-31', '2023-12-16', '2023-12-31']
    }
    
    # Major holidays (simplified)
    holidays = [
        '2022-01-01', '2022-07-04', '2022-12-25', '2022-12-31',
        '2023-01-01', '2023-07-04', '2023-12-25', '2023-12-31',
        # Add some random holidays
        '2022-05-30', '2022-09-05', '2022-11-24', '2022-11-25',
        '2023-05-29', '2023-09-04', '2023-11-23', '2023-11-24'
    ]
    
    # Base parameters
    base_competitor_price = 150
    base_roomify_price = 160
    total_rooms = 200  # Hotel capacity
    
    for i, date in enumerate(date_range):
        day_of_week = date.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5
        date_str = date.strftime('%Y-%m-%d')
        is_holiday = date_str in holidays
        
        # Determine season
        season = 'low'
        for season_name, dates in seasons.items():
            if len(dates) == 4:  # Handle both years
                if (date >= pd.to_datetime(dates[0]) and date <= pd.to_datetime(dates[1])) or \
                   (date >= pd.to_datetime(dates[2]) and date <= pd.to_datetime(dates[3])):
                    season = season_name.replace('_2023', '').replace('_2022', '')
                    break
        
        # Price elasticity parameters
        if season == 'high':
            demand_base = 180
            price_elasticity = -0.8
            competitor_price_multiplier = 1.3
            roomify_price_multiplier = 1.25
        elif season == 'medium':
            demand_base = 120
            price_elasticity = -1.2
            competitor_price_multiplier = 1.1
            roomify_price_multiplier = 1.15
        else:  # low season
            demand_base = 80
            price_elasticity = -1.5
            competitor_price_multiplier = 0.9
            roomify_price_multiplier = 0.95
        
        # Weekend and holiday adjustments
        weekend_multiplier = 1.4 if is_weekend else 1.0
        holiday_multiplier = 1.6 if is_holiday else 1.0
        
        # Generate competitor price with some randomness
        competitor_price = base_competitor_price * competitor_price_multiplier
        competitor_price += np.random.normal(0, 15)  # Add noise
        competitor_price = max(80, competitor_price)  # Minimum price
        
        # Roomify price (usually higher than competitor)
        roomify_price = base_roomify_price * roomify_price_multiplier
        roomify_price += np.random.normal(0, 20)
        roomify_price = max(90, roomify_price)
        
        # Ensure Roomify stays competitive (not too far from competitor)
        if roomify_price > competitor_price * 1.5:
            roomify_price = competitor_price * 1.4
        elif roomify_price < competitor_price * 0.8:
            roomify_price = competitor_price * 0.9
        
        # Calculate demand based on price elasticity
        price_ratio = roomify_price / competitor_price
        demand = demand_base * weekend_multiplier * holiday_multiplier
        
        # Apply price elasticity effect
        if roomify_price > competitor_price:
            price_penalty = (roomify_price - competitor_price) / competitor_price
            demand *= (1 - price_penalty * 0.3)  # Reduce demand if price is much higher
        
        # Add some randomness to demand
        demand += np.random.normal(0, 20)
        demand = max(0, demand)
        
        # Calculate occupancy
        occupancy = min(100, (demand / total_rooms) * 100)
        
        # Add some correlation between demand and actual bookings
        booking_rate = 0.85 + np.random.normal(0, 0.1)  # 85% booking rate with noise
        bookings = demand * booking_rate
        
        data.append({
            'Date': date,
            'Day_of_Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day_of_week],
            'Season': season.title(),
            'Holiday': 'Yes' if is_holiday else 'No',
            'Competitor_Price': round(competitor_price, 2),
            'Roomify_Price': round(roomify_price, 2),
            'Demand': round(demand, 1),
            'Bookings': round(bookings, 1),
            'Occupancy_Percentage': round(occupancy, 1),
            'Total_Rooms': total_rooms,
            'Revenue': round(roomify_price * bookings, 2),
            'RevPAR': round((roomify_price * bookings) / total_rooms, 2)  # Revenue per available room
        })
    
    return pd.DataFrame(data)

def save_dataset(df, filepath='sample_data/pricing_data.csv'):
    """Save the generated dataset to CSV file."""
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to {filepath}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")

def load_dataset(filepath='sample_data/pricing_data.csv'):
    """Load the pricing dataset from CSV file."""
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

if __name__ == "__main__":
    # Generate and save the dataset
    df = generate_synthetic_pricing_data()
    save_dataset(df)
    
    # Display sample data
    print("\nSample data:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nBasic statistics:")
    print(df.describe())
