"""
Visualization utilities for Roomify pricing dashboard.
Creates charts with explanatory text for business insights.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

class PricingVisualizer:
    """Creates visualizations with explanatory text for pricing insights."""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8'
        }
    
    def occupancy_trend_chart(self, df, title="Occupancy Trend Over Time"):
        """Create occupancy trend chart with seasonal patterns."""
        fig = go.Figure()
        
        # Add occupancy line
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Occupancy_Percentage'],
            mode='lines',
            name='Occupancy %',
            line=dict(color=self.color_palette['primary'], width=2),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'Occupancy: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ))
        
        # Add seasonal background colors
        seasons = df['Season'].unique()
        season_colors = {'Low': 'rgba(255,255,255,0.1)', 'Medium': 'rgba(255,165,0,0.1)', 'High': 'rgba(255,0,0,0.1)'}
        
        for season in seasons:
            season_data = df[df['Season'] == season]
            if not season_data.empty:
                fig.add_vrect(
                    x0=season_data['Date'].min(),
                    x1=season_data['Date'].max(),
                    fillcolor=season_colors.get(season, 'rgba(128,128,128,0.1)'),
                    layer="below",
                    line_width=0,
                    annotation_text=season,
                    annotation_position="top left"
                )
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Occupancy Percentage (%)",
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        explanation = """
        **Occupancy Trend Analysis**: This chart shows how occupancy fluctuates over time with clear seasonal patterns. 
        Notice the peaks during summer months (High season) and holiday periods, while winter months show lower occupancy. 
        Weekend spikes are visible throughout the year, indicating strong leisure demand patterns.
        """
        
        return fig, explanation
    
    def demand_price_curve(self, df, title="Demand vs Price Relationship"):
        """Create demand vs price scatter plot to show elasticity."""
        fig = go.Figure()
        
        # Color by season
        seasons = df['Season'].unique()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, season in enumerate(seasons):
            season_data = df[df['Season'] == season]
            fig.add_trace(go.Scatter(
                x=season_data['Roomify_Price'],
                y=season_data['Demand'],
                mode='markers',
                name=f'{season} Season',
                marker=dict(color=colors[i % len(colors)], size=8, opacity=0.7),
                hovertemplate='<b>%{customdata}</b><br>' +
                             'Price: $%{x:.0f}<br>' +
                             'Demand: %{y:.0f} rooms<br>' +
                             '<extra></extra>',
                customdata=season_data['Date'].dt.strftime('%Y-%m-%d')
            ))
        
        # Add trend line
        z = np.polyfit(df['Roomify_Price'], df['Demand'], 1)
        p = np.poly1d(z)
        trend_x = np.linspace(df['Roomify_Price'].min(), df['Roomify_Price'].max(), 100)
        trend_y = p(trend_x)
        
        fig.add_trace(go.Scatter(
            x=trend_x,
            y=trend_y,
            mode='lines',
            name='Trend Line',
            line=dict(color='red', width=3, dash='dash'),
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Roomify Price ($)",
            yaxis_title="Demand (Rooms)",
            template='plotly_white',
            height=400
        )
        
        explanation = """
        **Price Elasticity Analysis**: This scatter plot reveals the inverse relationship between price and demand. 
        Higher prices generally lead to lower demand, but the slope varies by season. In high season (red), 
        demand remains relatively stable even at higher prices, indicating lower price sensitivity. 
        The dashed trend line shows the overall negative correlation between price and demand.
        """
        
        return fig, explanation
    
    def revenue_optimization_chart(self, price_analysis_df, current_price=None, title="Revenue Optimization"):
        """Create revenue vs price chart for optimization."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Revenue vs Price', 'Occupancy vs Price'),
            vertical_spacing=0.1
        )
        
        # Revenue chart
        fig.add_trace(go.Scatter(
            x=price_analysis_df['price'],
            y=price_analysis_df['revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color=self.color_palette['success'], width=3),
            marker=dict(size=6),
            hovertemplate='<b>Price: $%{x:.0f}</b><br>' +
                         'Revenue: $%{y:,.0f}<br>' +
                         '<extra></extra>'
        ), row=1, col=1)
        
        # Occupancy chart
        fig.add_trace(go.Scatter(
            x=price_analysis_df['price'],
            y=price_analysis_df['occupancy'],
            mode='lines+markers',
            name='Occupancy',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=6),
            hovertemplate='<b>Price: $%{x:.0f}</b><br>' +
                         'Occupancy: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ), row=2, col=1)
        
        # Add current price line if provided
        if current_price:
            fig.add_vline(x=current_price, line_dash="dash", line_color="red", 
                         annotation_text=f"Current: ${current_price:.0f}", row=1, col=1)
            fig.add_vline(x=current_price, line_dash="dash", line_color="red", row=2, col=1)
        
        # Find and highlight optimal price
        optimal_idx = price_analysis_df['revenue'].idxmax()
        optimal_price = price_analysis_df.loc[optimal_idx, 'price']
        optimal_revenue = price_analysis_df.loc[optimal_idx, 'revenue']
        
        fig.add_vline(x=optimal_price, line_dash="dot", line_color="green",
                     annotation_text=f"Optimal: ${optimal_price:.0f}", row=1, col=1)
        fig.add_vline(x=optimal_price, line_dash="dot", line_color="green", row=2, col=1)
        
        fig.update_xaxes(title_text="Price ($)", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Occupancy (%)", row=2, col=1)
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=600,
            showlegend=False
        )
        
        explanation = f"""
        **Revenue Optimization Analysis**: This chart shows how revenue and occupancy change with different price points. 
        The optimal price of ${optimal_price:.0f} maximizes revenue at ${optimal_revenue:,.0f}. 
        Notice that the highest revenue doesn't always coincide with the highest occupancy - 
        this demonstrates the trade-off between occupancy and average daily rate (ADR).
        """
        
        return fig, explanation
    
    def price_elasticity_chart(self, elasticity_df, title="Price Elasticity Analysis"):
        """Create price elasticity sensitivity chart."""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Revenue Impact', 'Booking Impact'),
            horizontal_spacing=0.1
        )
        
        # Revenue change
        fig.add_trace(go.Bar(
            x=elasticity_df['price_change_pct'],
            y=elasticity_df['revenue_change_pct'],
            name='Revenue Change %',
            marker_color=['green' if x > 0 else 'red' for x in elasticity_df['revenue_change_pct']],
            hovertemplate='<b>Price Change: %{x}%</b><br>' +
                         'Revenue Change: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ), row=1, col=1)
        
        # Booking change
        fig.add_trace(go.Bar(
            x=elasticity_df['price_change_pct'],
            y=elasticity_df['booking_change_pct'],
            name='Booking Change %',
            marker_color=['blue' if x > 0 else 'orange' for x in elasticity_df['booking_change_pct']],
            hovertemplate='<b>Price Change: %{x}%</b><br>' +
                         'Booking Change: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ), row=1, col=2)
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=2)
        
        fig.update_xaxes(title_text="Price Change (%)", row=1, col=1)
        fig.update_xaxes(title_text="Price Change (%)", row=1, col=2)
        fig.update_yaxes(title_text="Revenue Change (%)", row=1, col=1)
        fig.update_yaxes(title_text="Booking Change (%)", row=1, col=2)
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        explanation = """
        **Price Sensitivity Analysis**: This chart shows how revenue and bookings respond to price changes. 
        Positive bars indicate increases, negative bars indicate decreases. 
        The relationship between price changes and booking changes shows demand elasticity - 
        larger negative booking changes indicate higher price sensitivity.
        """
        
        return fig, explanation
    
    def competitive_analysis_chart(self, df, title="Competitive Pricing Analysis"):
        """Create competitive pricing comparison chart."""
        fig = go.Figure()
        
        # Add competitor price
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Competitor_Price'],
            mode='lines',
            name='Competitor Price',
            line=dict(color=self.color_palette['danger'], width=2),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'Competitor: $%{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add Roomify price
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Roomify_Price'],
            mode='lines',
            name='Roomify Price',
            line=dict(color=self.color_palette['primary'], width=2),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'Roomify: $%{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add price difference area
        price_diff = df['Roomify_Price'] - df['Competitor_Price']
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=price_diff,
            mode='lines',
            name='Price Difference',
            line=dict(color=self.color_palette['warning'], width=2),
            fill='tonexty',
            fillcolor='rgba(255,165,0,0.2)',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         'Difference: $%{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template='plotly_white',
            height=400
        )
        
        explanation = """
        **Competitive Positioning**: This chart tracks Roomify's pricing relative to competitors over time. 
        The orange area shows the price premium (positive) or discount (negative) compared to competitors. 
        Maintaining a reasonable premium while staying competitive is key to maximizing revenue without losing market share.
        """
        
        return fig, explanation
    
    def kpi_dashboard(self, df):
        """Create KPI summary cards."""
        # Calculate key metrics
        avg_occupancy = df['Occupancy_Percentage'].mean()
        avg_daily_rate = df['Roomify_Price'].mean()
        total_revenue = df['Revenue'].sum()
        avg_revenue = df['Revenue'].mean()
        revpar = df['RevPAR'].mean()
        
        # Calculate growth rates (comparing first half vs second half)
        mid_point = len(df) // 2
        first_half_revenue = df.iloc[:mid_point]['Revenue'].mean()
        second_half_revenue = df.iloc[mid_point:]['Revenue'].mean()
        revenue_growth = ((second_half_revenue - first_half_revenue) / first_half_revenue) * 100
        
        kpis = {
            'Average Occupancy': f"{avg_occupancy:.1f}%",
            'Average Daily Rate': f"${avg_daily_rate:.0f}",
            'Total Revenue': f"${total_revenue:,.0f}",
            'Average Daily Revenue': f"${avg_revenue:,.0f}",
            'RevPAR': f"${revpar:.0f}",
            'Revenue Growth': f"{revenue_growth:+.1f}%"
        }
        
        return kpis

def create_insight_text(chart_type, data_summary=None):
    """Generate contextual insight text for different chart types."""
    insights = {
        'occupancy_trend': """
        **Seasonal Occupancy Patterns**: The occupancy trend reveals clear seasonal cycles with summer peaks and winter valleys. 
        Holiday periods show significant spikes, indicating strong leisure demand. Weekend occupancy consistently outperforms weekdays, 
        suggesting a leisure-focused customer base. These patterns are crucial for pricing strategy - higher prices can be sustained 
        during peak periods while competitive pricing may be needed during low seasons.
        """,
        
        'demand_price': """
        **Price Elasticity Insights**: The demand-price relationship shows classic economic behavior with higher prices reducing demand. 
        However, the elasticity varies significantly by season - high season shows relatively inelastic demand (customers still book at higher prices), 
        while low season shows elastic demand (price changes have larger impact on bookings). This suggests different pricing strategies 
        for different seasons: premium pricing in high season, competitive pricing in low season.
        """,
        
        'revenue_optimization': """
        **Revenue Maximization Strategy**: The revenue optimization curve shows the classic trade-off between occupancy and average daily rate. 
        The optimal price point balances these factors to maximize total revenue. Beyond the optimal point, higher prices reduce revenue due to 
        decreased occupancy. This analysis helps identify the sweet spot where price increases still generate positive revenue impact.
        """,
        
        'competitive': """
        **Competitive Positioning Strategy**: Maintaining competitive pricing while maximizing revenue requires careful balance. 
        The analysis shows periods where Roomify can command premium pricing and periods where competitive pricing is necessary. 
        The key is understanding when customers are price-sensitive versus when they value other factors like location or amenities.
        """
    }
    
    return insights.get(chart_type, "Analysis provides insights into pricing strategy optimization.")
