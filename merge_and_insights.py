import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the datasets
print("Loading datasets...")
restaurant_data = pd.read_csv('zomato_restaurant_data.csv')
delivery_data = pd.read_csv('swiggyzomato_data.csv')

print(f"Restaurant data shape: {restaurant_data.shape}")
print(f"Delivery data shape: {delivery_data.shape}")

# Extract city from restaurant data (City column)
cities = restaurant_data['City'].values

# Add city to delivery data
delivery_data_enhanced = delivery_data.copy()
delivery_data_enhanced['City'] = cities

# Create enhanced delivery time analysis
delivery_data_enhanced['order_time'] = pd.to_datetime(delivery_data_enhanced['order_time'])
delivery_data_enhanced['accept_time'] = pd.to_datetime(delivery_data_enhanced['accept_time'])
delivery_data_enhanced['pickup_time'] = pd.to_datetime(delivery_data_enhanced['pickup_time'])
delivery_data_enhanced['delivered_time'] = pd.to_datetime(delivery_data_enhanced['delivered_time'])

# Calculate delivery metrics
delivery_data_enhanced['delivery_time_minutes'] = (
    delivery_data_enhanced['delivered_time'] - delivery_data_enhanced['pickup_time']
).dt.total_seconds() / 60

delivery_data_enhanced['response_time_minutes'] = (
    delivery_data_enhanced['accept_time'] - delivery_data_enhanced['order_time']
).dt.total_seconds() / 60

delivery_data_enhanced['pickup_delay_minutes'] = (
    delivery_data_enhanced['pickup_time'] - delivery_data_enhanced['accept_time']
).dt.total_seconds() / 60

# Extract time features
delivery_data_enhanced['hour'] = delivery_data_enhanced['order_time'].dt.hour
delivery_data_enhanced['day_of_week'] = delivery_data_enhanced['order_time'].dt.day_name()
delivery_data_enhanced['is_weekend'] = delivery_data_enhanced['day_of_week'].isin(['Saturday', 'Sunday'])

# Calculate distance metrics
delivery_data_enhanced['total_distance'] = (
    delivery_data_enhanced['first_mile_distance'] + delivery_data_enhanced['last_mile_distance']
)

# Create performance metrics
delivery_data_enhanced['on_time_delivery'] = delivery_data_enhanced['delivery_time_minutes'] <= 30
delivery_data_enhanced['fast_response'] = delivery_data_enhanced['response_time_minutes'] <= 5

# Save the enhanced dataset
delivery_data_enhanced.to_csv('enhanced_delivery_data.csv', index=False)
print("Enhanced delivery data saved to 'enhanced_delivery_data.csv'")

# Create comprehensive business insights
print("\nGenerating comprehensive business insights...")

# 1. City Performance Analysis
city_insights = delivery_data_enhanced.groupby('City').agg({
    'delivery_time_minutes': ['mean', 'std', 'count'],
    'response_time_minutes': 'mean',
    'total_distance': 'mean',
    'on_time_delivery': 'mean',
    'fast_response': 'mean',
    'rider_id': 'nunique'
}).round(2)

city_insights.columns = ['Avg_Delivery_Time', 'Std_Delivery_Time', 'Order_Count', 
                        'Avg_Response_Time', 'Avg_Distance', 'On_Time_Rate', 
                        'Fast_Response_Rate', 'Active_Riders']
city_insights = city_insights.sort_values('Order_Count', ascending=False)

# 2. Peak Hour Analysis
hourly_insights = delivery_data_enhanced.groupby('hour').agg({
    'delivery_time_minutes': 'mean',
    'response_time_minutes': 'mean',
    'order_id': 'count'
}).round(2)
hourly_insights.columns = ['Avg_Delivery_Time', 'Avg_Response_Time', 'Order_Count']
hourly_insights['Peak_Hour'] = hourly_insights['Order_Count'] > hourly_insights['Order_Count'].quantile(0.75)

# 3. Distance vs Delivery Time Analysis
distance_bins = [0, 2, 4, 6, 8, 10, float('inf')]
distance_labels = ['0-2km', '2-4km', '4-6km', '6-8km', '8-10km', '10km+']
delivery_data_enhanced['distance_category'] = pd.cut(
    delivery_data_enhanced['total_distance'], 
    bins=distance_bins, 
    labels=distance_labels
)

distance_insights = delivery_data_enhanced.groupby('distance_category').agg({
    'delivery_time_minutes': ['mean', 'std'],
    'order_id': 'count',
    'on_time_delivery': 'mean'
}).round(2)
distance_insights.columns = ['Avg_Delivery_Time', 'Std_Delivery_Time', 'Order_Count', 'On_Time_Rate']

# 4. Rider Performance Analysis
rider_insights = delivery_data_enhanced.groupby('rider_id').agg({
    'delivery_time_minutes': ['mean', 'count'],
    'response_time_minutes': 'mean',
    'on_time_delivery': 'mean',
    'total_distance': 'mean'
}).round(2)

rider_insights.columns = ['Avg_Delivery_Time', 'Order_Count', 'Avg_Response_Time', 
                         'On_Time_Rate', 'Avg_Distance']
rider_insights = rider_insights[rider_insights['Order_Count'] >= 10]  # Active riders
rider_insights = rider_insights.sort_values('On_Time_Rate', ascending=False)

# 5. Weekend vs Weekday Analysis
weekend_insights = delivery_data_enhanced.groupby('is_weekend').agg({
    'delivery_time_minutes': 'mean',
    'response_time_minutes': 'mean',
    'order_id': 'count',
    'on_time_delivery': 'mean'
}).round(2)
weekend_insights.columns = ['Avg_Delivery_Time', 'Avg_Response_Time', 'Order_Count', 'On_Time_Rate']

# Generate comprehensive insights summary
insights_summary = []

# Top performing cities
top_cities = city_insights.head(5)
insights_summary.append("🏆 TOP PERFORMING CITIES:")
for city, row in top_cities.iterrows():
    insights_summary.append(f"• {city}: {row['Order_Count']} orders, {row['Avg_Delivery_Time']}min avg delivery, {row['On_Time_Rate']*100:.1f}% on-time")

# Peak hours
peak_hours = hourly_insights[hourly_insights['Peak_Hour']].sort_values('Order_Count', ascending=False)
insights_summary.append(f"\n⏰ PEAK ORDER HOURS:")
for hour, row in peak_hours.head(3).iterrows():
    insights_summary.append(f"• {hour}:00-{hour+1}:00: {row['Order_Count']} orders, {row['Avg_Delivery_Time']}min avg delivery")

# Distance insights
insights_summary.append(f"\n📍 DISTANCE INSIGHTS:")
for dist_cat, row in distance_insights.iterrows():
    insights_summary.append(f"• {dist_cat}: {row['Avg_Delivery_Time']}min avg, {row['On_Time_Rate']*100:.1f}% on-time")

# Weekend impact
insights_summary.append(f"\n📅 WEEKEND VS WEEKDAY:")
for is_weekend, row in weekend_insights.iterrows():
    day_type = "Weekend" if is_weekend else "Weekday"
    insights_summary.append(f"• {day_type}: {row['Order_Count']} orders, {row['Avg_Delivery_Time']}min avg, {row['On_Time_Rate']*100:.1f}% on-time")

# Top riders
top_riders = rider_insights.head(5)
insights_summary.append(f"\n🚴 TOP PERFORMING RIDERS:")
for rider_id, row in top_riders.iterrows():
    insights_summary.append(f"• Rider {int(rider_id)}: {row['Order_Count']} orders, {row['On_Time_Rate']*100:.1f}% on-time, {row['Avg_Delivery_Time']}min avg")

# Key business recommendations
recommendations = [
    "🎯 STRATEGIC RECOMMENDATIONS:",
    "• Increase rider capacity during peak hours (7-10 PM) to reduce delivery times",
    "• Implement dynamic pricing for longer distances (>8km) to maintain profitability",
    "• Focus on improving response times during weekday lunch hours (12-2 PM)",
    "• Provide incentives for riders with >90% on-time delivery rate",
    "• Optimize restaurant partnerships in high-performing cities",
    "• Implement predictive routing for distances >6km to improve efficiency",
    "• Create weekend-specific delivery strategies to handle increased demand",
    "• Monitor and reward top-performing riders to reduce churn"
]

# Combine all insights
all_insights = insights_summary + recommendations

# Save insights to file
with open('business_insights.txt', 'w', encoding='utf-8') as f:
    f.write("COMPREHENSIVE BUSINESS INSIGHTS\n")
    f.write("=" * 50 + "\n\n")
    for insight in all_insights:
        f.write(insight + "\n")

# Save detailed analytics to CSV
city_insights.to_csv('city_performance_analytics.csv')
hourly_insights.to_csv('hourly_performance_analytics.csv')
distance_insights.to_csv('distance_performance_analytics.csv')
rider_insights.to_csv('rider_performance_analytics.csv')
weekend_insights.to_csv('weekend_performance_analytics.csv')

print("\n✅ Files created successfully:")
print("• enhanced_delivery_data.csv - Merged dataset with city information")
print("• business_insights.txt - Comprehensive business insights")
print("• city_performance_analytics.csv - City-wise performance metrics")
print("• hourly_performance_analytics.csv - Hour-wise performance metrics")
print("• distance_performance_analytics.csv - Distance-wise performance metrics")
print("• rider_performance_analytics.csv - Rider performance metrics")
print("• weekend_performance_analytics.csv - Weekend vs Weekday comparison")

# Display summary statistics
print(f"\n📊 SUMMARY STATISTICS:")
print(f"• Total Orders: {len(delivery_data_enhanced):,}")
print(f"• Total Cities: {delivery_data_enhanced['City'].nunique()}")
print(f"• Total Riders: {delivery_data_enhanced['rider_id'].nunique()}")
print(f"• Avg Delivery Time: {delivery_data_enhanced['delivery_time_minutes'].mean():.1f} minutes")
print(f"• On-Time Delivery Rate: {delivery_data_enhanced['on_time_delivery'].mean()*100:.1f}%")
print(f"• Fast Response Rate: {delivery_data_enhanced['fast_response'].mean()*100:.1f}%")
print(f"• Avg Distance: {delivery_data_enhanced['total_distance'].mean():.1f} km")

print(f"\n🎯 Key Insights:")
for insight in all_insights[:5]:  # Show first 5 key insights
    print(f"• {insight}")
