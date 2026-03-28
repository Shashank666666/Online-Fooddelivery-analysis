import pandas as pd
import numpy as np

# Load the enhanced dataset
enhanced_data = pd.read_csv('enhanced_delivery_data.csv')

# Create distance categories
distance_bins = [0, 2, 4, 6, 8, 10, float('inf')]
distance_labels = ['0-2km', '2-4km', '4-6km', '6-8km', '8-10km', '10km+']
enhanced_data['distance_category'] = pd.cut(
    enhanced_data['total_distance'], 
    bins=distance_bins, 
    labels=distance_labels
)

# Generate key business insights
def generate_key_insights(data):
    insights = []
    
    # 1. Top Cities by Order Volume
    city_orders = data.groupby('City')['order_id'].count().sort_values(ascending=False)
    top_cities = city_orders.head(3)
    
    insights.append("🏆 TOP CITIES BY ORDERS:")
    for city, orders in top_cities.items():
        insights.append(f"• {city}: {orders:,} orders")
    
    # 2. Peak Order Hours
    hourly_orders = data.groupby('hour')['order_id'].count()
    peak_hours = hourly_orders.nlargest(3)
    
    insights.append("\n⏰ PEAK ORDER HOURS:")
    for hour, orders in peak_hours.items():
        insights.append(f"• {hour}:00-{hour+1}:00: {orders:,} orders")
    
    # 3. Delivery Performance by City
    city_performance = data.groupby('City').agg({
        'delivery_time_minutes': 'mean',
        'on_time_delivery': 'mean'
    }).round(2)
    
    best_cities = city_performance.nsmallest(3, 'delivery_time_minutes')
    insights.append("\n🚀 FASTEST DELIVERY CITIES:")
    for city, row in best_cities.iterrows():
        insights.append(f"• {city}: {row['delivery_time_minutes']}min avg, {row['on_time_delivery']*100:.0f}% on-time")
    
    # 4. Distance Impact
    distance_performance = data.groupby('distance_category').agg({
        'delivery_time_minutes': 'mean',
        'order_id': 'count'
    }).round(2)
    
    insights.append("\n📍 DELIVERY TIME BY DISTANCE:")
    for dist_cat, row in distance_performance.iterrows():
        insights.append(f"• {dist_cat}: {row['delivery_time_minutes']}min avg ({row['order_id']:,} orders)")
    
    # 5. Weekend vs Weekday Performance (only show if weekend data exists)
    weekend_data = data[data['is_weekend'] == True]
    weekday_data = data[data['is_weekend'] == False]

    if len(weekend_data) > 0:
        insights.append("\n📅 WEEKEND VS WEEKDAY:")
        insights.append(f"• Weekend: {len(weekend_data):,} orders, {weekend_data['delivery_time_minutes'].mean():.1f}min avg")
        insights.append(f"• Weekday: {len(weekday_data):,} orders, {weekday_data['delivery_time_minutes'].mean():.1f}min avg")
    
    return insights

# Generate and save insights
key_insights = generate_key_insights(enhanced_data)

with open('key_business_insights.txt', 'w', encoding='utf-8') as f:
    f.write("KEY BUSINESS INSIGHTS\n")
    f.write("=" * 30 + "\n\n")
    for insight in key_insights:
        f.write(insight + "\n")

print("Key business insights saved to 'key_business_insights.txt'")
print("\n📊 KEY INSIGHTS SUMMARY:")
for insight in key_insights:
    print(f"• {insight}")
