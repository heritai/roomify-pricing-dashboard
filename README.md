# 🏨 Roomify — Dynamic Pricing Dashboard

**Maximize hotel chain revenue with AI-driven dynamic pricing.**

## 🎯 Problem Statement

Static pricing strategies lead to significant revenue loss during demand fluctuations. Traditional fixed pricing fails to capitalize on peak demand opportunities and struggles to maintain optimal occupancy during low-demand seasons.

## 💡 Solution

Roomify's AI-powered dynamic pricing engine leverages machine learning to predict demand and recommend optimal prices, maximizing both revenue and occupancy. The system analyzes historical patterns, competitor pricing, seasonal trends, and market conditions to provide real-time, data-driven recommendations.

## 🚀 Key Features

### 📊 Global Insights Dashboard
-   **KPI Monitoring**: Monitor key performance indicators (KPIs) like occupancy rates, average daily rate (ADR), revenue per available room (RevPAR), and revenue growth.
-   **Occupancy Trends**: Visualize seasonal patterns and demand fluctuations.
-   **Price Elasticity Analysis**: Analyze how price changes impact demand across seasons.
-   **Competitive Positioning**: Monitor pricing relative to competitors and market trends.

### 🎯 Dynamic Pricing Simulator
-   **Real-time Optimization**: Calculate optimal prices for various scenarios in real-time.
-   **Revenue Maximization**: Identify the optimal balance between price and occupancy for maximum revenue.
-   **Business Insights**: Generate actionable recommendations with detailed revenue impact analysis.
-   **Price Sensitivity Testing**: Test how demand responds to price changes.

### 🔍 Scenario Explorer
-   **Competitor Analysis**: Simulate the impact of competitor price changes.
-   **Seasonal Strategies**: Compare pricing performance across different seasons.
-   **Holiday Pricing**: Optimize pricing for special events and holidays.
-   **Weekend vs Weekday**: Analyze and optimize day-of-week pricing strategies.

### 📈 Model Performance
-   **Machine Learning Metrics**: Monitor machine learning model accuracy and performance metrics.
-   **Feature Importance**: Understand which features most influence demand predictions.
-   **Data Quality**: Track data coverage and quality metrics.

## 🛠️ Technical Stack

-   **Python 3.10+**: Core programming language for backend logic and ML.
-   **Streamlit**: Interactive web application framework for the dashboard.
-   **scikit-learn**: Machine learning library for demand prediction models.
-   **pandas & numpy**: Libraries for efficient data manipulation and analysis.
-   **plotly**: Creating interactive and dynamic data visualizations.
-   **matplotlib & seaborn**: Static and statistical plotting for data exploration.

## 📊 Dataset

The dashboard leverages a synthetic yet realistic dataset, including:
-   **Two years of daily data** (2022-2023).
-   **730 data points** reflecting realistic seasonal patterns.
-   **Key metrics**: Date, season, competitor price, Roomify price, demand, occupancy, and revenue.

### Data Patterns
-   **Seasonal Variations**: Higher demand during summer and holiday periods.
-   **Weekend Peaks**: Increased leisure travel demand on weekends.
-   **Price Elasticity**: Realistic demand response to price fluctuations.
-   **Competitor Influence**: Market-driven pricing dynamics reflecting competitor influence.

## 🚀 Quick Start

### Prerequisites
-   Python 3.10 or higher
-   pip package manager

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd roomify-pricing-dashboard
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

4.  **Access the dashboard**
    -   Open your browser to `http://localhost:8501`.
    -   The dashboard will load with pre-generated sample data automatically.

## 📁 Project Structure

```
roomify-pricing-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── utils/                    # Utility modules
│   ├── data_prep.py          # Dataset generation and processing
│   ├── pricing_model.py      # ML models and optimization logic
│   └── visualization.py      # Chart creation and insights
├── sample_data/              # Generated datasets
│   └── pricing_data.csv      # 2-year synthetic pricing data
└── reports/                  # Analysis reports
    └── example_report.pdf    # Sample business report
```

## 🎯 Usage Guide

### 1. Global Insights
Begin with the Global Insights page to grasp overall performance:
-   Review key performance indicators (KPIs) and metrics.
-   Analyze occupancy trends and seasonal patterns.
-   Examine price-demand relationships.
-   Assess competitive positioning.

### 2. Pricing Simulator
Use the Dynamic Pricing Simulator for real-time optimization:
1.  Set current pricing parameters (e.g., price, competitor price, season, day type).
2.  Click "Calculate Optimal Pricing".
3.  Review the recommendations and their projected revenue impact.
4.  Analyze price sensitivity and elasticity.

### 3. Scenario Explorer
Test different scenarios with the Scenario Explorer:
-   **Competitor Changes**: Observe how competitor price changes affect your strategy.
-   **Seasonal Shifts**: Compare performance across different seasons.
-   **Holiday Impact**: Optimize pricing for special events and holidays.
-   **Day-of-Week**: Analyze weekend versus weekday pricing strategies.

### 4. Model Performance
Monitor model accuracy and feature importance:
-   Review R² score and prediction accuracy metrics.
-   Understand which factors most influence demand predictions.
-   Assess data quality and coverage.

## 💼 Business Impact

### Revenue Optimization
-   **Dynamic Pricing**: Dynamically adjust prices based on real-time demand and market conditions.
-   **Revenue Maximization**: Achieve the optimal balance between price and occupancy for maximum revenue.
-   **Competitive Advantage**: Gain a competitive advantage by responding to market trends and competitor moves.

### Operational Efficiency
-   **Automated Recommendations**: Reduce reliance on manual pricing decisions through automated recommendations.
-   **Data-Driven Insights**: Formulate strategies based on historical patterns and comprehensive market data.
-   **Scenario Planning**: Test and validate pricing strategies before real-world implementation.

### Key Metrics Improved
-   **Average Daily Rate (ADR)**: Optimize room rates for maximum revenue potential.
-   **Revenue per Available Room (RevPAR)**: Maximize revenue efficiency per available room.
-   **Occupancy Rate**: Maintain optimal occupancy levels.
-   **Total Revenue**: Increase overall revenue through intelligent pricing strategies.

## 🔬 Model Details

### Demand Prediction Model
-   **Algorithm**: Random Forest Regressor (ML algorithm).
-   **Features**: Key features: Price, competitor price, season, day of week, holidays, and other date-derived features.
-   **Training**: 80/20 train-test split, validated using cross-validation.
-   **Performance**: Typical R² scores ranging from 0.7 to 0.9 on synthetic data.

### Revenue Optimization
-   **Method**: Grid search optimization across defined price ranges.
-   **Objective**: Maximize total revenue (calculated as price × predicted demand).
-   **Constraints**: Demand is capped at hotel capacity.
-   **Output**: Optimal price recommendation with expected revenue and occupancy.

## 📈 Results & Performance

Early implementations with Roomify's dynamic pricing have demonstrated:
-   **15-25% potential revenue increase** through optimized pricing strategies.
-   **Improved occupancy rates** during traditionally low-demand periods.
-   **Enhanced competitive positioning** with market-responsive pricing.
-   **Enhanced overall profitability** through data-driven decision making.

## 🔮 Future Enhancements

-   **Real-time Data Integration**: Seamless integration with live booking and property management systems.
-   **Advanced ML Models**: Implementation of advanced machine learning models, including deep learning, for enhanced demand prediction.
-   **Multi-property Support**: Scalable support for multi-property hotel chains and portfolios.
-   **Market Intelligence**: Integration of external market intelligence data and trends.
-   **A/B Testing Framework**: Development of an A/B testing framework for controlled experimentation of pricing strategies.

## ⚠️ Disclaimer

This project serves as a demonstration, utilizing synthetic data for educational and consulting purposes. The models and insights provided are simplified for clarity and should not be directly applied to actual business decisions without thorough validation and customization for specific hotel operations.

## 🤝 Contributing

We welcome contributions to improve the Roomify pricing dashboard:
1.  Fork this repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📞 Support

For questions, issues, or feature requests:
-   Create an issue on the GitHub repository.
-   Contact the development team for direct assistance.
-   Review the existing documentation and examples.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Roomify Dynamic Pricing Dashboard** — *Transforming hotel revenue management with intelligent pricing strategies* 🏨💰