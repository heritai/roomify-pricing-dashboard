"""
Pricing model and revenue optimization for Roomify dashboard.
Implements demand curve estimation and revenue maximization algorithms.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class DemandPredictor:
    """Predicts hotel demand based on pricing and contextual factors."""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
    def prepare_features(self, df):
        """Prepare features for model training/prediction."""
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['Day_of_Week', 'Season', 'Holiday']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col + '_encoded'] = self.label_encoders[col].fit_transform(df_processed[col])
            else:
                df_processed[col + '_encoded'] = self.label_encoders[col].transform(df_processed[col])
        
        # Create additional features
        df_processed['Price_Ratio'] = df_processed['Roomify_Price'] / df_processed['Competitor_Price']
        df_processed['Price_Difference'] = df_processed['Roomify_Price'] - df_processed['Competitor_Price']
        df_processed['Is_Weekend'] = df_processed['Day_of_Week'].isin(['Saturday', 'Sunday']).astype(int)
        df_processed['Is_Holiday'] = (df_processed['Holiday'] == 'Yes').astype(int)
        
        # Extract date features
        df_processed['Month'] = df_processed['Date'].dt.month
        df_processed['Day_of_Year'] = df_processed['Date'].dt.dayofyear
        
        # Define feature columns
        self.feature_columns = [
            'Roomify_Price', 'Competitor_Price', 'Price_Ratio', 'Price_Difference',
            'Day_of_Week_encoded', 'Season_encoded', 'Is_Weekend', 'Is_Holiday',
            'Month', 'Day_of_Year'
        ]
        
        return df_processed[self.feature_columns]
    
    def train(self, df):
        """Train the demand prediction model."""
        X = self.prepare_features(df)
        y = df['Demand']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        
        return {
            'mse': mse,
            'r2': r2,
            'feature_importance': dict(zip(self.feature_columns, self.model.feature_importances_))
        }
    
    def predict_demand(self, roomify_price, competitor_price, day_of_week, season, is_holiday):
        """Predict demand for given parameters."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create input dataframe
        input_data = pd.DataFrame({
            'Date': [pd.Timestamp.now()],
            'Day_of_Week': [day_of_week],
            'Season': [season],
            'Holiday': ['Yes' if is_holiday else 'No'],
            'Roomify_Price': [roomify_price],
            'Competitor_Price': [competitor_price],
            'Demand': [0]  # Placeholder
        })
        
        X = self.prepare_features(input_data)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)[0]

class RevenueOptimizer:
    """Optimizes pricing to maximize revenue."""
    
    def __init__(self, demand_predictor):
        self.demand_predictor = demand_predictor
        self.total_rooms = 200
        
    def calculate_revenue(self, price, competitor_price, day_of_week, season, is_holiday):
        """Calculate expected revenue for given price."""
        predicted_demand = self.demand_predictor.predict_demand(
            price, competitor_price, day_of_week, season, is_holiday
        )
        
        # Cap demand at total rooms
        bookings = min(predicted_demand, self.total_rooms)
        revenue = price * bookings
        
        return revenue, bookings, predicted_demand
    
    def find_optimal_price(self, competitor_price, day_of_week, season, is_holiday, 
                          price_range=(80, 400), step=5):
        """Find price that maximizes revenue."""
        best_price = competitor_price
        best_revenue = 0
        best_bookings = 0
        
        results = []
        
        for price in range(price_range[0], price_range[1] + 1, step):
            revenue, bookings, demand = self.calculate_revenue(
                price, competitor_price, day_of_week, season, is_holiday
            )
            
            results.append({
                'price': price,
                'revenue': revenue,
                'bookings': bookings,
                'demand': demand,
                'occupancy': (bookings / self.total_rooms) * 100
            })
            
            if revenue > best_revenue:
                best_revenue = revenue
                best_price = price
                best_bookings = bookings
        
        return {
            'optimal_price': best_price,
            'max_revenue': best_revenue,
            'optimal_bookings': best_bookings,
            'price_analysis': pd.DataFrame(results)
        }
    
    def price_elasticity_analysis(self, base_price, competitor_price, day_of_week, season, is_holiday):
        """Analyze price elasticity around base price."""
        price_changes = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
        
        results = []
        base_revenue, base_bookings, base_demand = self.calculate_revenue(
            base_price, competitor_price, day_of_week, season, is_holiday
        )
        
        for change in price_changes:
            new_price = base_price * (1 + change / 100)
            revenue, bookings, demand = self.calculate_revenue(
                new_price, competitor_price, day_of_week, season, is_holiday
            )
            
            revenue_change = ((revenue - base_revenue) / base_revenue) * 100
            booking_change = ((bookings - base_bookings) / base_bookings) * 100
            
            results.append({
                'price_change_pct': change,
                'new_price': new_price,
                'revenue_change_pct': revenue_change,
                'booking_change_pct': booking_change,
                'revenue': revenue,
                'bookings': bookings
            })
        
        return pd.DataFrame(results)

class PricingInsights:
    """Generate business insights from pricing analysis."""
    
    @staticmethod
    def generate_insights(optimization_result, elasticity_result, current_price):
        """Generate business insights from pricing analysis."""
        optimal_price = optimization_result['optimal_price']
        max_revenue = optimization_result['max_revenue']
        
        # Calculate current metrics
        current_revenue = None
        for _, row in optimization_result['price_analysis'].iterrows():
            if abs(row['price'] - current_price) < 5:  # Find closest price
                current_revenue = row['revenue']
                break
        
        insights = []
        
        # Price recommendation
        if optimal_price > current_price:
            price_increase = ((optimal_price - current_price) / current_price) * 100
            insights.append(f"💰 **Revenue Opportunity**: Increase price by ${optimal_price - current_price:.0f} ({price_increase:.1f}%) to maximize revenue")
        elif optimal_price < current_price:
            price_decrease = ((current_price - optimal_price) / current_price) * 100
            insights.append(f"💰 **Revenue Opportunity**: Decrease price by ${current_price - optimal_price:.0f} ({price_decrease:.1f}%) to maximize revenue")
        else:
            insights.append("✅ **Optimal Pricing**: Current price is already optimal for revenue maximization")
        
        # Revenue impact
        if current_revenue:
            revenue_improvement = ((max_revenue - current_revenue) / current_revenue) * 100
            insights.append(f"📈 **Revenue Impact**: Optimizing price could increase revenue by ${max_revenue - current_revenue:.0f} ({revenue_improvement:.1f}%)")
        
        # Elasticity insights
        elasticity_df = elasticity_result
        high_impact_changes = elasticity_df[abs(elasticity_df['revenue_change_pct']) > 10]
        
        if not high_impact_changes.empty:
            best_increase = high_impact_changes[high_impact_changes['price_change_pct'] > 0]['revenue_change_pct'].max()
            best_decrease = high_impact_changes[high_impact_changes['price_change_pct'] < 0]['revenue_change_pct'].max()
            
            if best_increase > 0:
                insights.append(f"⚡ **High Impact Increase**: {best_increase:.1f}% revenue increase possible with moderate price increase")
            if best_decrease > 0:
                insights.append(f"⚡ **High Impact Decrease**: {best_decrease:.1f}% revenue increase possible with price reduction")
        
        # Competitive insights
        avg_competitor_price = 150  # This could be dynamic
        if optimal_price > avg_competitor_price * 1.2:
            insights.append("⚠️ **Competitive Risk**: Optimal price significantly above competitor average - monitor market position")
        elif optimal_price < avg_competitor_price * 0.9:
            insights.append("🎯 **Competitive Advantage**: Optimal price below competitor average - strong market position")
        
        return insights

def train_pricing_model(df):
    """Train the complete pricing model pipeline."""
    predictor = DemandPredictor()
    optimizer = RevenueOptimizer(predictor)
    insights = PricingInsights()
    
    # Train demand predictor
    training_metrics = predictor.train(df)
    
    return predictor, optimizer, insights, training_metrics

def save_model(predictor, filepath='models/pricing_model.pkl'):
    """Save trained model to file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(predictor, filepath)

def load_model(filepath='models/pricing_model.pkl'):
    """Load trained model from file."""
    return joblib.load(filepath)
