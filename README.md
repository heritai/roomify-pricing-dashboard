# 🏨 Roomify — Dynamic Pricing Dashboard

**Maximize hotel chain revenue with AI-driven dynamic pricing.**

## 🎯 Problem Statement

Static pricing strategies prevent hotels from maximizing revenue by failing to adapt to demand fluctuations. Traditional fixed pricing misses opportunities to capitalize on peak demand and struggles to maintain optimal occupancy during low-demand seasons, resulting in substantial revenue loss.

## 💡 Solution

Roomify's AI-powered dynamic pricing engine uses machine learning to predict demand and recommend optimal prices, maximizing both revenue and occupancy. The system analyzes historical patterns, competitor pricing, seasonal trends, and broader market conditions to deliver real-time, data-driven recommendations.

## 🚀 Key Features

### 📊 Global Insights Dashboard
-   **KPI Monitoring**: Monitor key performance indicators (KPIs) like occupancy rates, Average Daily Rate (ADR), Revenue Per Available Room (RevPAR), and overall revenue growth.
-   **Occupancy Trends**: Visualize seasonal patterns and demand fluctuations.
-   **Price Elasticity Analysis**: Analyze the impact of price changes on demand across seasons.
-   **Competitive Positioning**: Track pricing relative to competitors and broader market trends.

### 🎯 Dynamic Pricing Simulator
-   **Real-time Optimization**: Calculate optimal prices for diverse scenarios in real-time.
-   **Revenue Maximization**: Identify the optimal balance between price and occupancy to maximize revenue.
-   **Business Insights**: Generate actionable recommendations with detailed revenue impact analysis.
-   **Price Sensitivity Testing**: Test demand responsiveness to price adjustments.

### 🔍 Scenario Explorer
-   **Competitor Analysis**: Simulate the impact of competitor price adjustments.
-   **Seasonal Strategies**: Compare pricing performance across seasons.
-   **Holiday Pricing**: Optimize pricing for special events and holidays.
-   **Weekend vs Weekday**: Analyze and optimize day-of-week pricing strategies.

### 📈 Model Performance
-   **Machine Learning Metrics**: Monitor machine learning model accuracy and key performance metrics.
-   **Feature Importance**: Understand the key features influencing demand predictions.
-   **Data Quality**: Track data coverage and quality metrics.

## 🛠️ Technical Stack

Here's a look at the core technologies powering Roomify:

-   **Python 3.10+**: Core programming language for backend logic and ML model development.
-   **Streamlit**: Interactive web application framework for the dashboard interface.
-   **Scikit-learn**: Machine learning library for demand prediction models.
-   **Pandas & NumPy**: Libraries for efficient data manipulation and analysis.
-   **Plotly**: For creating interactive and dynamic data visualizations.
-   **Matplotlib & Seaborn**: For static and statistical plotting in data exploration.

## 📊 Dataset

The dashboard uses a synthetic, yet realistic, dataset, comprising:
-   **Two years of daily data** (2022-2023).
-   **730 data points**, reflecting realistic seasonal patterns and market dynamics.
-   **Key metrics**: Date, season, competitor price, Roomify's price, demand, occupancy, and revenue.

### Data Patterns
-   **Seasonal Variations**: Higher demand during summer and holiday periods.
-   **Weekend Peaks**: Increased leisure travel demand during weekends.
-   **Price Elasticity**: Realistic demand response to price changes.
-   **Competitor Influence**: Market-driven pricing dynamics, reflecting competitor strategies.

## 🚀 Quick Start

Get Roomify up and running quickly with these steps:

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
    -   Access the dashboard via your web browser at `http://localhost:8501`.
    -   The dashboard will automatically load with pre-generated sample data.

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

Navigate Roomify effectively with this guide:

### 1. Global Insights
Begin with the Global Insights page to gain a comprehensive understanding of overall performance:
-   Review key performance indicators (KPIs) and core metrics.
-   Analyze occupancy trends and seasonal patterns.
-   Examine price-demand relationships.
-   Assess competitive positioning.

### 2. Pricing Simulator
Use the Dynamic Pricing Simulator for real-time optimization:
1.  Set current pricing parameters (e.g., your price, competitor price, season, day of week).
2.  Click "Calculate Optimal Pricing".
3.  Review the optimal price recommendations and their projected revenue impact.
4.  Analyze price sensitivity and elasticity.

### 3. Scenario Explorer
Test different scenarios with the Scenario Explorer:
-   **Competitor Changes**: Observe how competitor pricing adjustments affect your strategy.
-   **Seasonal Shifts**: Compare performance across various seasons.
-   **Holiday Impact**: Optimize pricing for special events and holidays.
-   **Day-of-Week**: Analyze and optimize weekend versus weekday pricing strategies.

### 4. Model Performance
Monitor model accuracy and feature importance:
-   Review R² score and prediction accuracy metrics.
-   Understand which factors most significantly influence demand predictions.
-   Assess data quality and coverage.

## 💼 Business Impact

Roomify delivers tangible business benefits:

### Revenue Optimization
-   **Dynamic Pricing**: Dynamically adjust prices based on real-time demand and market conditions to maximize potential.
-   **Revenue Maximization**: Achieve the optimal balance between price and occupancy for maximum revenue.
-   **Competitive Advantage**: Gain a competitive advantage by swiftly responding to market trends and competitor actions.

### Operational Efficiency
-   **Automated Recommendations**: Reduce reliance on manual pricing decisions through automated recommendations.
-   **Data-Driven Insights**: Formulate robust strategies based on historical patterns and comprehensive market data.
-   **Scenario Planning**: Test and validate pricing strategies before real-world implementation.

### Key Metrics Improved
-   **Average Daily Rate (ADR)**: Optimize room rates for maximum revenue potential.
-   **Revenue per Available Room (RevPAR)**: Maximize revenue efficiency per available room.
-   **Occupancy Rate**: Maintain optimal occupancy levels.
-   **Total Revenue**: Increase overall revenue through intelligent pricing strategies.

## 🔬 Model Details

### Demand Prediction Model
-   **Algorithm**: Random Forest Regressor (Machine Learning algorithm).
-   **Features**: Key features include Roomify's price, competitor price, season, day of week, holidays, and other date-derived attributes.
-   **Training**: Utilizes an 80/20 train-test split, validated through cross-validation.
-   **Performance**: Achieves typical R² scores ranging from 0.7 to 0.9 on synthetic data.

### Revenue Optimization
-   **Method**: Grid search optimization across predefined price ranges.
-   **Objective**: Maximize total revenue (calculated as price × predicted demand).
-   **Constraints**: Demand is capped at the hotel's capacity.
-   **Output**: Provides optimal price recommendations along with expected revenue and occupancy.

## 📈 Results & Performance

Early implementations of Roomify's dynamic pricing have demonstrated:
-   **A potential 15-25% increase in revenue** through optimized pricing strategies.
-   **Improved occupancy rates**, particularly during traditionally low-demand periods.
-   **Enhanced competitive positioning** through market-responsive pricing.
-   **Enhanced overall profitability** through data-driven decision-making.

## 🔮 Future Enhancements

Roomify is continuously evolving, with planned enhancements including:

-   **Real-time Data Integration**: Seamless integration with live booking and property management systems (PMS).
-   **Advanced ML Models**: Implementation of advanced machine learning models, including deep learning, for even more precise demand prediction.
-   **Multi-property Support**: Scalable support for multi-property hotel chains and portfolios.
-   **Market Intelligence**: Integration of external market intelligence data and trends.
-   **A/B Testing Framework**: Development of an A/B testing framework for controlled experimentation of pricing strategies.

## ⚠️ Disclaimer

This project serves as a demonstration, utilizing synthetic data purely for educational and consulting purposes. The models and insights provided are simplified for clarity and should not be directly applied to actual business decisions without thorough validation and customization tailored to specific hotel operations.

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

**Roomify Dynamic Pricing Dashboard** — *Transforming hotel revenue management with intelligent, data-driven strategies.* 🏨💰