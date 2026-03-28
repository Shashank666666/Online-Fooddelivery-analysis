# 🍔 Interactive Food Delivery Dashboard

A comprehensive web-based analytics dashboard for food delivery business intelligence, built with Python, Dash, and Plotly.

## 📊 Features

### 🎯 Core Dashboard
- **6 Interactive Charts** - Cuisine distribution, price analysis, delivery metrics, ratings, city performance, top restaurants
- **Real-time Filtering** - Filter by cuisine type, city, and price range
- **Click Interactions** - Click any chart element to see detailed restaurant information
- **Dynamic Insights** - Real-time business intelligence and recommendations
- **Dark Theme UI** - Professional, modern interface with consistent styling

### 📈 Analytics & Insights
- **Business Metrics** - Order counts, delivery times, ratings, pricing analysis
- **Performance Analytics** - City-wise, hourly, distance, and rider performance
- **Smart Recommendations** - AI-powered business insights and action items
- **Data Merging** - Enhanced delivery data with restaurant information

### 🎨 User Experience
- **Responsive Design** - Works on all screen sizes
- **Repeated Click Support** - Click same chart multiple times
- **Chart Switching** - Seamless navigation between different visualizations
- **Detailed Information** - Restaurant names, ratings, and performance metrics

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements_dashboard.txt
```

### Run Dashboard
```bash
python interactive_dashboard.py
```

Access the dashboard at: `http://127.0.0.1:8050`

## 📁 Project Structure

```
├── interactive_dashboard.py          # Main dashboard application
├── enhanced_delivery_data.csv       # Delivery data with city information
├── zomato_restaurant_data.csv      # Restaurant information
├── key_business_insights.txt       # Business insights summary
├── generate_key_insights.py       # Insights generation script
├── merge_and_insights.py          # Data processing and analytics
└── requirements_dashboard.txt        # Python dependencies
```

## 📊 Data Sources

### Delivery Data (`enhanced_delivery_data.csv`)
- Order information with timestamps
- Delivery times and distances
- Restaurant and city details
- Rider performance metrics
- Customer ratings and feedback

### Restaurant Data (`zomato_restaurant_data.csv`)
- Restaurant names and cuisines
- Pricing information
- Location details
- Rating and review data

## 🎯 How to Use

### 1. **Filter Data**
- Use dropdowns to filter by cuisine type
- Select specific cities for regional analysis
- Adjust price range slider for cost analysis

### 2. **Explore Charts**
- **Cuisine Distribution** - Click bars to see top restaurants
- **Price Analysis** - Click histogram for price range details
- **Delivery Metrics** - Click for time and distance insights
- **Rating Comparison** - Click for quality analysis
- **City Performance** - Click for geographic insights
- **Top Restaurants** - Click for detailed rankings

### 3. **View Insights**
- **Selected Details** - Shows restaurant information for clicked elements
- **Business Insights** - Real-time recommendations and metrics
- **Performance Metrics** - KPIs and trend analysis

## 🔧 Technical Stack

- **Backend**: Python 3.x
- **Framework**: Dash by Plotly
- **Visualization**: Plotly Express & Graph Objects
- **Styling**: Dash Bootstrap Components
- **Data Processing**: Pandas & NumPy
- **Deployment**: Flask development server

## 📈 Key Features Explained

### Interactive Click System
- Click any chart element (bars, pie slices, data points)
- View detailed restaurant information including names and ratings
- Repeated clicks supported - click same element multiple times
- Smart chart switching - maintains context between views

### Business Intelligence
- **Dynamic Filtering** - Real-time data exploration
- **Performance Analytics** - Multi-dimensional insights
- **Smart Recommendations** - Contextual business advice
- **Trend Analysis** - Time-based performance metrics

### Enhanced Data Processing
- **Data Merging** - Combines delivery and restaurant information
- **City Enrichment** - Adds location context to delivery data
- **Analytics Generation** - Creates detailed performance reports
- **Insight Extraction** - Identifies key business opportunities

## 🎯 Business Insights Generated

### Operational Metrics
- Order volume and patterns
- Delivery time analysis
- Customer satisfaction ratings
- Geographic performance

### Performance Analytics
- City-wise delivery performance
- Hourly order patterns
- Distance impact analysis
- Rider productivity metrics

### Strategic Recommendations
- Peak hour optimization
- Geographic expansion opportunities
- Pricing strategy insights
- Service improvement areas

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements_dashboard.txt

# Run dashboard
python interactive_dashboard.py

# Access at
http://127.0.0.1:8050
```

### Production Considerations
- **Security**: Add authentication for production use
- **Scaling**: Consider Redis for session management
- **Database**: Migrate to PostgreSQL/MySQL for large datasets
- **Monitoring**: Add logging and error tracking

## 📊 Sample Insights Generated

- **"🏆 Top performing cities: Bangalore, Mumbai, Delhi with 15,234, 12,456, 10,789 orders"**
- **"⏰ Peak delivery hours: 7-9 PM with 25% higher order volume"**
- **"📈 Average delivery time: 18.5 minutes with 92% on-time rate"**
- **"💰 Optimal price range: ₹200-400 with highest customer satisfaction"**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or support:
- Create an issue in the GitHub repository
- Check the existing documentation and code comments
- Review the sample insights and analytics outputs

---

**Built with ❤️ for data-driven food delivery businesses**
