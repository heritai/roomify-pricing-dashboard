"""
Roomify Dynamic Pricing Dashboard
A comprehensive tool for hotel revenue optimization through intelligent pricing strategies.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our custom modules
from utils.data_prep import load_dataset
from utils.pricing_model import train_pricing_model, DemandPredictor, RevenueOptimizer, PricingInsights
from utils.visualization import PricingVisualizer

# Page configuration
st.set_page_config(
    page_title="Roomify - Dynamic Pricing Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling (dark mode compatible)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--text-color);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color);
        margin: 0.5rem 0;
        color: var(--text-color);
    }
    .insight-box {
        background-color: rgba(23, 162, 184, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        color: var(--text-color);
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        color: var(--text-color);
    }
    .success-box {
        background-color: rgba(40, 167, 69, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    /* Dark mode specific adjustments */
    @media (prefers-color-scheme: dark) {
        .kpi-card {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .insight-box {
            background-color: rgba(23, 162, 184, 0.2);
            border: 1px solid rgba(23, 162, 184, 0.3);
        }
        .warning-box {
            background-color: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.3);
        }
        .success-box {
            background-color: rgba(40, 167, 69, 0.2);
            border: 1px solid rgba(40, 167, 69, 0.3);
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the pricing dataset."""
    try:
        df = load_dataset()
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure sample_data/pricing_data.csv exists.")
        return None

@st.cache_resource
def load_models():
    """Load and cache the pricing models."""
    try:
        df = load_data()
        if df is not None:
            predictor, optimizer, insights, metrics = train_pricing_model(df)
            return predictor, optimizer, insights, metrics
        return None, None, None, None
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None, None

def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">🏨 Roomify Dynamic Pricing Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Maximize revenue and occupancy through AI-driven dynamic pricing strategies**")
    
    # Load data and models
    df = load_data()
    predictor, optimizer, insights, metrics = load_models()
    
    if df is None or predictor is None:
        st.error("Unable to load data or models. Please check your setup.")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Global Insights", "🎯 Pricing Simulator", "🔍 Scenario Explorer", "📈 Model Performance"]
    )
    
    # Initialize visualizer
    visualizer = PricingVisualizer()
    
    if page == "📊 Global Insights":
        show_global_insights(df, visualizer)
    elif page == "🎯 Pricing Simulator":
        show_pricing_simulator(predictor, optimizer, insights, visualizer)
    elif page == "🔍 Scenario Explorer":
        show_scenario_explorer(predictor, optimizer, insights, visualizer)
    elif page == "📈 Model Performance":
        show_model_performance(metrics, df)

def show_global_insights(df, visualizer):
    """Display global insights and KPIs."""
    st.markdown('<h2 class="sub-header">📊 Global Insights & Performance Metrics</h2>', unsafe_allow_html=True)
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    kpis = visualizer.kpi_dashboard(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Average Occupancy</h4>
            <h2>{kpis['Average Occupancy']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Average Daily Rate</h4>
            <h2>{kpis['Average Daily Rate']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Total Revenue</h4>
            <h2>{kpis['Total Revenue']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-card">
            <h4>RevPAR</h4>
            <h2>{kpis['RevPAR']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Average Daily Revenue</h4>
            <h2>{kpis['Average Daily Revenue']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Revenue Growth</h4>
            <h2>{kpis['Revenue Growth']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    st.subheader("Occupancy Trend Analysis")
    fig1, explanation1 = visualizer.occupancy_trend_chart(df)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(f'<div class="insight-box">{explanation1}</div>', unsafe_allow_html=True)
    
    st.subheader("Demand vs Price Relationship")
    fig2, explanation2 = visualizer.demand_price_curve(df)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(f'<div class="insight-box">{explanation2}</div>', unsafe_allow_html=True)
    
    st.subheader("Competitive Pricing Analysis")
    fig3, explanation3 = visualizer.competitive_analysis_chart(df)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(f'<div class="insight-box">{explanation3}</div>', unsafe_allow_html=True)

def show_pricing_simulator(predictor, optimizer, insights, visualizer):
    """Display the dynamic pricing simulator."""
    st.markdown('<h2 class="sub-header">🎯 Dynamic Pricing Simulator</h2>', unsafe_allow_html=True)
    st.markdown("Test different pricing scenarios and find the optimal price for maximum revenue.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Parameters")
        
        # User inputs
        base_price = st.number_input(
            "Current Roomify Price ($)",
            min_value=50.0,
            max_value=500.0,
            value=160.0,
            step=5.0
        )
        
        competitor_price = st.number_input(
            "Competitor Price ($)",
            min_value=50.0,
            max_value=500.0,
            value=150.0,
            step=5.0
        )
        
        day_of_week = st.selectbox(
            "Day of Week",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        
        season = st.selectbox(
            "Season",
            ["Low", "Medium", "High"]
        )
        
        is_holiday = st.checkbox("Is Holiday")
        
        # Calculate button
        if st.button("🚀 Calculate Optimal Pricing", type="primary"):
            with st.spinner("Analyzing pricing scenarios..."):
                # Run optimization
                optimization_result = optimizer.find_optimal_price(
                    competitor_price, day_of_week, season, is_holiday
                )
                
                # Calculate current metrics
                current_revenue, current_bookings, current_demand = optimizer.calculate_revenue(
                    base_price, competitor_price, day_of_week, season, is_holiday
                )
                
                # Price elasticity analysis
                elasticity_result = optimizer.price_elasticity_analysis(
                    base_price, competitor_price, day_of_week, season, is_holiday
                )
                
                # Generate insights
                business_insights = insights.generate_insights(
                    optimization_result, elasticity_result, base_price
                )
                
                # Store results in session state
                st.session_state.optimization_result = optimization_result
                st.session_state.current_metrics = {
                    'revenue': current_revenue,
                    'bookings': current_bookings,
                    'demand': current_demand
                }
                st.session_state.elasticity_result = elasticity_result
                st.session_state.business_insights = business_insights
    
    with col2:
        st.subheader("Results & Analysis")
        
        if 'optimization_result' in st.session_state:
            result = st.session_state.optimization_result
            current = st.session_state.current_metrics
            elasticity = st.session_state.elasticity_result
            insights_list = st.session_state.business_insights
            
            # Results summary
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric(
                    "Optimal Price",
                    f"${result['optimal_price']:.0f}",
                    f"${result['optimal_price'] - base_price:+.0f}"
                )
            
            with col_b:
                st.metric(
                    "Max Revenue",
                    f"${result['max_revenue']:,.0f}",
                    f"${result['max_revenue'] - current['revenue']:+,.0f}"
                )
            
            with col_c:
                st.metric(
                    "Optimal Bookings",
                    f"{result['optimal_bookings']:.0f}",
                    f"{result['optimal_bookings'] - current['bookings']:+.0f}"
                )
            
            # Business insights
            st.subheader("💡 Business Insights & Recommendations")
            for insight in insights_list:
                if "Revenue Opportunity" in insight:
                    st.markdown(f'<div class="success-box">{insight}</div>', unsafe_allow_html=True)
                elif "Optimal Pricing" in insight:
                    st.markdown(f'<div class="success-box">{insight}</div>', unsafe_allow_html=True)
                elif "Risk" in insight:
                    st.markdown(f'<div class="warning-box">{insight}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            
            # Revenue optimization chart
            st.subheader("Revenue Optimization Analysis")
            fig1, explanation1 = visualizer.revenue_optimization_chart(
                result['price_analysis'], base_price
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(f'<div class="insight-box">{explanation1}</div>', unsafe_allow_html=True)
            
            # Price elasticity chart
            st.subheader("Price Sensitivity Analysis")
            fig2, explanation2 = visualizer.price_elasticity_chart(elasticity)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(f'<div class="insight-box">{explanation2}</div>', unsafe_allow_html=True)
        
        else:
            st.info("👆 Adjust the parameters on the left and click 'Calculate Optimal Pricing' to see results.")

def show_scenario_explorer(predictor, optimizer, insights, visualizer):
    """Display the scenario explorer for what-if analysis."""
    st.markdown('<h2 class="sub-header">🔍 Scenario Explorer</h2>', unsafe_allow_html=True)
    st.markdown("Explore 'what-if' scenarios to understand how different factors impact pricing and revenue.")
    
    # Scenario selection
    scenario_type = st.selectbox(
        "Choose scenario type:",
        ["Competitor Price Change", "Seasonal Demand Shift", "Holiday Impact", "Weekend vs Weekday"]
    )
    
    if scenario_type == "Competitor Price Change":
        show_competitor_scenario(predictor, optimizer, insights, visualizer)
    elif scenario_type == "Seasonal Demand Shift":
        show_seasonal_scenario(predictor, optimizer, insights, visualizer)
    elif scenario_type == "Holiday Impact":
        show_holiday_scenario(predictor, optimizer, insights, visualizer)
    elif scenario_type == "Weekend vs Weekday":
        show_weekend_scenario(predictor, optimizer, insights, visualizer)

def show_competitor_scenario(predictor, optimizer, insights, visualizer):
    """Show competitor price change scenarios."""
    st.subheader("Competitor Price Impact Analysis")
    
    base_competitor_price = st.slider(
        "Base Competitor Price ($)",
        min_value=100,
        max_value=300,
        value=150,
        step=10
    )
    
    price_changes = st.multiselect(
        "Competitor Price Changes to Test:",
        [-20, -10, -5, 0, 5, 10, 20],
        default=[-10, 0, 10]
    )
    
    # Fixed parameters
    base_roomify_price = 160
    day_of_week = "Friday"
    season = "Medium"
    is_holiday = False
    
    if st.button("Run Scenario Analysis"):
        results = []
        
        for change in price_changes:
            new_competitor_price = base_competitor_price * (1 + change / 100)
            
            # Find optimal price for this scenario
            optimization_result = optimizer.find_optimal_price(
                new_competitor_price, day_of_week, season, is_holiday
            )
            
            results.append({
                'competitor_change': change,
                'competitor_price': new_competitor_price,
                'optimal_roomify_price': optimization_result['optimal_price'],
                'max_revenue': optimization_result['max_revenue'],
                'optimal_bookings': optimization_result['optimal_bookings']
            })
        
        results_df = pd.DataFrame(results)
        
        # Display results
        st.subheader("Scenario Results")
        st.dataframe(results_df.style.format({
            'competitor_price': '${:.0f}',
            'optimal_roomify_price': '${:.0f}',
            'max_revenue': '${:,.0f}',
            'optimal_bookings': '{:.0f}'
        }))
        
        # Visualization
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Optimal Price vs Competitor Price', 'Revenue Impact'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(go.Scatter(
            x=results_df['competitor_price'],
            y=results_df['optimal_roomify_price'],
            mode='lines+markers',
            name='Optimal Roomify Price',
            line=dict(color='blue', width=3)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=results_df['competitor_price'],
            y=results_df['max_revenue'],
            mode='lines+markers',
            name='Max Revenue',
            line=dict(color='green', width=3)
        ), row=2, col=1)
        
        fig.update_xaxes(title_text="Competitor Price ($)", row=2, col=1)
        fig.update_yaxes(title_text="Optimal Roomify Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        
        fig.update_layout(
            title="Competitor Price Impact Analysis",
            template='plotly_white',
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown("""
        <div class="insight-box">
        **Competitor Price Impact**: This analysis shows how competitor price changes affect our optimal pricing strategy. 
        Generally, when competitors increase prices, we can also increase our prices to maintain our competitive position 
        while maximizing revenue. The key is finding the sweet spot where we remain competitive but don't lose market share.
        </div>
        """, unsafe_allow_html=True)

def show_seasonal_scenario(predictor, optimizer, insights, visualizer):
    """Show seasonal demand shift scenarios."""
    st.subheader("Seasonal Demand Impact Analysis")
    
    seasons = ["Low", "Medium", "High"]
    competitor_price = 150
    
    results = []
    
    for season in seasons:
        optimization_result = optimizer.find_optimal_price(
            competitor_price, "Saturday", season, False
        )
        
        results.append({
            'season': season,
            'optimal_price': optimization_result['optimal_price'],
            'max_revenue': optimization_result['max_revenue'],
            'optimal_bookings': optimization_result['optimal_bookings'],
            'occupancy': (optimization_result['optimal_bookings'] / 200) * 100
        })
    
    results_df = pd.DataFrame(results)
    
    # Display results
    st.subheader("Seasonal Comparison")
    st.dataframe(results_df.style.format({
        'optimal_price': '${:.0f}',
        'max_revenue': '${:,.0f}',
        'optimal_bookings': '{:.0f}',
        'occupancy': '{:.1f}%'
    }))
    
    # Visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Optimal Price by Season', 'Revenue by Season', 
                       'Bookings by Season', 'Occupancy by Season'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    fig.add_trace(go.Bar(
        x=results_df['season'],
        y=results_df['optimal_price'],
        name='Optimal Price',
        marker_color=colors
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=results_df['season'],
        y=results_df['max_revenue'],
        name='Max Revenue',
        marker_color=colors
    ), row=1, col=2)
    
    fig.add_trace(go.Bar(
        x=results_df['season'],
        y=results_df['optimal_bookings'],
        name='Optimal Bookings',
        marker_color=colors
    ), row=2, col=1)
    
    fig.add_trace(go.Bar(
        x=results_df['season'],
        y=results_df['occupancy'],
        name='Occupancy %',
        marker_color=colors
    ), row=2, col=2)
    
    fig.update_layout(
        title="Seasonal Performance Analysis",
        template='plotly_white',
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    **Seasonal Strategy Insights**: High season allows for premium pricing with strong occupancy, 
    while low season requires more competitive pricing to maintain bookings. Medium season provides 
    a balance between price and occupancy. This analysis helps set seasonal pricing strategies.
    </div>
    """, unsafe_allow_html=True)

def show_holiday_scenario(predictor, optimizer, insights, visualizer):
    """Show holiday impact scenarios."""
    st.subheader("Holiday Impact Analysis")
    
    competitor_price = 150
    season = "Medium"
    day_of_week = "Friday"
    
    # Compare holiday vs non-holiday
    scenarios = [
        {"name": "Regular Day", "is_holiday": False},
        {"name": "Holiday", "is_holiday": True}
    ]
    
    results = []
    
    for scenario in scenarios:
        optimization_result = optimizer.find_optimal_price(
            competitor_price, day_of_week, season, scenario["is_holiday"]
        )
        
        results.append({
            'scenario': scenario["name"],
            'optimal_price': optimization_result['optimal_price'],
            'max_revenue': optimization_result['max_revenue'],
            'optimal_bookings': optimization_result['optimal_bookings'],
            'occupancy': (optimization_result['optimal_bookings'] / 200) * 100
        })
    
    results_df = pd.DataFrame(results)
    
    # Display results
    st.subheader("Holiday vs Regular Day Comparison")
    st.dataframe(results_df.style.format({
        'optimal_price': '${:.0f}',
        'max_revenue': '${:,.0f}',
        'optimal_bookings': '{:.0f}',
        'occupancy': '{:.1f}%'
    }))
    
    # Calculate impact
    holiday_impact = results_df[results_df['scenario'] == 'Holiday'].iloc[0]
    regular_impact = results_df[results_df['scenario'] == 'Regular Day'].iloc[0]
    
    price_impact = ((holiday_impact['optimal_price'] - regular_impact['optimal_price']) / regular_impact['optimal_price']) * 100
    revenue_impact = ((holiday_impact['max_revenue'] - regular_impact['max_revenue']) / regular_impact['max_revenue']) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Price Impact",
            f"{price_impact:+.1f}%",
            f"${holiday_impact['optimal_price'] - regular_impact['optimal_price']:+.0f}"
        )
    
    with col2:
        st.metric(
            "Revenue Impact",
            f"{revenue_impact:+.1f}%",
            f"${holiday_impact['max_revenue'] - regular_impact['max_revenue']:+,.0f}"
        )
    
    st.markdown("""
    <div class="insight-box">
    **Holiday Pricing Strategy**: Holidays typically allow for significant price increases due to higher demand 
    and reduced price sensitivity. Customers are often willing to pay premium prices during special occasions. 
    This analysis helps identify optimal holiday pricing strategies to maximize revenue during high-demand periods.
    </div>
    """, unsafe_allow_html=True)

def show_weekend_scenario(predictor, optimizer, insights, visualizer):
    """Show weekend vs weekday scenarios."""
    st.subheader("Weekend vs Weekday Analysis")
    
    competitor_price = 150
    season = "Medium"
    is_holiday = False
    
    # Compare different days
    days = ["Monday", "Wednesday", "Friday", "Saturday", "Sunday"]
    
    results = []
    
    for day in days:
        optimization_result = optimizer.find_optimal_price(
            competitor_price, day, season, is_holiday
        )
        
        results.append({
            'day': day,
            'optimal_price': optimization_result['optimal_price'],
            'max_revenue': optimization_result['max_revenue'],
            'optimal_bookings': optimization_result['optimal_bookings'],
            'occupancy': (optimization_result['optimal_bookings'] / 200) * 100,
            'is_weekend': day in ['Saturday', 'Sunday']
        })
    
    results_df = pd.DataFrame(results)
    
    # Display results
    st.subheader("Day-of-Week Performance")
    st.dataframe(results_df.style.format({
        'optimal_price': '${:.0f}',
        'max_revenue': '${:,.0f}',
        'optimal_bookings': '{:.0f}',
        'occupancy': '{:.1f}%'
    }))
    
    # Visualization
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Optimal Price by Day', 'Revenue by Day')
    )
    
    # Color by weekend
    colors = ['red' if x else 'blue' for x in results_df['is_weekend']]
    
    fig.add_trace(go.Bar(
        x=results_df['day'],
        y=results_df['optimal_price'],
        name='Optimal Price',
        marker_color=colors
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=results_df['day'],
        y=results_df['max_revenue'],
        name='Max Revenue',
        marker_color=colors
    ), row=1, col=2)
    
    fig.update_layout(
        title="Day-of-Week Performance Analysis (Red=Weekend, Blue=Weekday)",
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekend vs weekday summary
    weekend_data = results_df[results_df['is_weekend'] == True]
    weekday_data = results_df[results_df['is_weekend'] == False]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weekend Average")
        st.metric("Avg Price", f"${weekend_data['optimal_price'].mean():.0f}")
        st.metric("Avg Revenue", f"${weekend_data['max_revenue'].mean():,.0f}")
        st.metric("Avg Occupancy", f"{weekend_data['occupancy'].mean():.1f}%")
    
    with col2:
        st.subheader("Weekday Average")
        st.metric("Avg Price", f"${weekday_data['optimal_price'].mean():.0f}")
        st.metric("Avg Revenue", f"${weekday_data['max_revenue'].mean():,.0f}")
        st.metric("Avg Occupancy", f"{weekday_data['occupancy'].mean():.1f}%")
    
    st.markdown("""
    <div class="insight-box">
    **Weekend vs Weekday Strategy**: Weekends typically command higher prices and generate more revenue 
    due to leisure travel demand. This analysis helps optimize pricing for different day types, 
    with weekend pricing strategies focusing on maximizing revenue from leisure travelers.
    </div>
    """, unsafe_allow_html=True)

def show_model_performance(metrics, df):
    """Display model performance metrics."""
    st.markdown('<h2 class="sub-header">📈 Model Performance & Analytics</h2>', unsafe_allow_html=True)
    
    if metrics is None:
        st.error("Model metrics not available.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Accuracy")
        st.metric("R² Score", f"{metrics['r2']:.3f}")
        st.metric("Mean Squared Error", f"{metrics['mse']:.1f}")
        
        # Model performance interpretation
        r2 = metrics['r2']
        if r2 > 0.8:
            st.success("🟢 Excellent model performance - high predictive accuracy")
        elif r2 > 0.6:
            st.warning("🟡 Good model performance - moderate predictive accuracy")
        else:
            st.error("🔴 Poor model performance - low predictive accuracy")
    
    with col2:
        st.subheader("Feature Importance")
        importance_df = pd.DataFrame(
            list(metrics['feature_importance'].items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=importance_df['Importance'],
            y=importance_df['Feature'],
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Feature Importance in Demand Prediction",
            xaxis_title="Importance",
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Data quality metrics
    st.subheader("Data Quality & Coverage")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        st.metric("Date Range", f"{(df['Date'].max() - df['Date'].min()).days} days")
    
    with col3:
        st.metric("Avg Occupancy", f"{df['Occupancy_Percentage'].mean():.1f}%")
    
    with col4:
        st.metric("Price Range", f"${df['Roomify_Price'].min():.0f} - ${df['Roomify_Price'].max():.0f}")
    
    # Model insights
    st.subheader("Model Insights")
    st.markdown("""
    <div class="insight-box">
    **Model Performance Analysis**: The demand prediction model uses machine learning to analyze historical patterns 
    and predict future demand based on pricing and contextual factors. Feature importance shows which factors 
    most strongly influence demand predictions, helping prioritize pricing strategy considerations.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
