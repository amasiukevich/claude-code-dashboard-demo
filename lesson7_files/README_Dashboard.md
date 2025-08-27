# E-commerce Business Intelligence Dashboard

A professional Streamlit dashboard for interactive e-commerce business performance analysis with real-time KPIs, trend analysis, and geographic insights.

## Dashboard Overview

This dashboard converts the comprehensive EDA analysis into an interactive business intelligence tool designed for stakeholders, analysts, and business leaders.

### Dashboard Features

🎯 **Key Performance Indicators**
- Total Revenue with year-over-year comparison
- Monthly Growth Rate tracking
- Average Order Value with trend indicators  
- Total Orders with growth metrics

📊 **Interactive Analytics**
- Revenue trend analysis with current vs previous period comparison
- Top 10 product categories by revenue (horizontal bar chart)
- Geographic performance via interactive US state map
- Customer satisfaction analysis by delivery speed

⚡ **Real-time Filtering**
- Year selection with automatic comparison to previous year
- Dynamic chart updates based on selected time period
- Consistent data filtering across all visualizations

🎨 **Professional Design**
- Clean, business-oriented layout
- Consistent color schemes and formatting
- Mobile-responsive design
- Trend indicators with color coding (green/red)

## Quick Start

### 1. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Launch Dashboard

```bash
# Start the Streamlit dashboard
streamlit run dashboard.py
```

### 3. Access Dashboard

Open your browser and navigate to:
```
http://localhost:8501
```

## Dashboard Layout

### Header Section
- **Left**: Dashboard title with business intelligence branding
- **Right**: Year selection dropdown for filtering data

### KPI Cards Row
Four key performance indicators displayed as cards:

1. **Total Revenue**
   - Current year total revenue
   - Trend indicator vs previous year
   - Color-coded arrows (↗ green, ↘ red)

2. **Monthly Growth**
   - Average month-over-month growth rate
   - Calculated from monthly revenue changes

3. **Average Order Value**
   - Mean order value for selected period
   - Trend comparison with previous year

4. **Total Orders**
   - Total number of orders processed
   - Growth indicator vs previous period

### Analytics Grid (2x2)

**Top Row:**
- **Revenue Trend Chart**: Line chart comparing current vs previous year monthly revenue
  - Solid line: Current year
  - Dashed line: Previous year
  - Grid lines for easy reading
  - Currency formatting ($300K style)

- **Top Categories Chart**: Horizontal bar chart of top 10 product categories
  - Blue gradient coloring
  - Revenue values formatted as $300K, $2M
  - Sorted descending by revenue

**Bottom Row:**
- **Geographic Map**: Interactive US choropleth map
  - Color-coded by state revenue
  - Hover details with revenue, orders, AOV
  - Blue gradient color scheme

- **Satisfaction Analysis**: Bar chart of customer satisfaction by delivery speed
  - X-axis: Delivery time buckets (1-3 days, 4-7 days, 8+ days)
  - Y-axis: Average review score
  - Color-coded bars

### Bottom Metrics Row
Two additional key metrics:

1. **Average Delivery Time**
   - Days from order to delivery
   - Trend indicator vs previous period

2. **Review Score Display**
   - Large numeric rating with star visualization
   - "Average Review Score" subtitle

## Configuration Options

### Data Filtering
The dashboard automatically filters data based on year selection:
```python
# Year selection affects all charts and metrics
selected_year = st.selectbox("Select Year", available_years)
```

### Chart Customization
Charts use consistent styling defined in `dashboard_utils.py`:
```python
COLORS = {
    'primary': '#1f77b4',    # Blue for primary elements
    'secondary': '#ff7f0e',  # Orange for comparisons
    'success': '#28a745',    # Green for positive trends
    'danger': '#dc3545'      # Red for negative trends
}
```

### Performance Optimization
The dashboard uses Streamlit caching for data loading:
```python
@st.cache_data
def load_and_prepare_data():
    # Cached data loading for better performance
```

## Technical Architecture

### File Structure
```
lesson7_files/
├── dashboard.py              # Main Streamlit application
├── dashboard_utils.py        # Chart generation utilities
├── data_loader.py           # Data processing functions
├── business_metrics.py      # Business logic and calculations
├── requirements.txt         # Python dependencies
├── README_Dashboard.md      # This file
└── ecommerce_data/         # CSV data files
```

### Key Dependencies
- **Streamlit**: Web dashboard framework
- **Plotly**: Interactive chart generation
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Data Processing Flow
1. **Data Loading**: Raw CSV files loaded and cached
2. **Data Cleaning**: Timestamp parsing, filtering, joins
3. **Metric Calculation**: Business KPIs computed
4. **Chart Generation**: Interactive visualizations created
5. **Dashboard Rendering**: Streamlit layout with real-time updates

## Deployment Options

### Local Development
```bash
streamlit run dashboard.py
```

### Cloud Deployment

**Streamlit Cloud:**
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy directly from repository

**Docker Deployment:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]
```

**Heroku Deployment:**
1. Add `Procfile`: `web: streamlit run dashboard.py --server.port=$PORT`
2. Include `setup.sh` for Streamlit configuration
3. Deploy via Git or GitHub integration

## Customization Guide

### Adding New KPIs
1. Update `calculate_revenue_metrics()` in `business_metrics.py`
2. Add new metric card in dashboard KPI row
3. Include trend calculation logic

### Creating New Charts
1. Add chart function to `dashboard_utils.py`
2. Import and use in `dashboard.py`
3. Follow existing color and styling conventions

### Modifying Layout
The dashboard uses Streamlit columns for layout:
```python
col1, col2 = st.columns([3, 1])  # 3:1 ratio
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)  # Equal width
```

## Data Requirements

### Expected Data Structure
The dashboard expects CSV files in `ecommerce_data/` directory:

- `orders_dataset.csv`: Order information with timestamps
- `order_items_dataset.csv`: Item-level pricing data
- `products_dataset.csv`: Product catalog with categories
- `customers_dataset.csv`: Customer geographic data
- `order_reviews_dataset.csv`: Customer satisfaction scores

### Data Quality Assumptions
- Orders have valid timestamps for date filtering
- Revenue calculations based on delivered orders only
- Geographic analysis requires valid state codes
- Review scores range from 1-5

## Troubleshooting

### Common Issues

**Dashboard won't start:**
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify data files exist in `ecommerce_data/` directory
- Ensure Python 3.8+ is being used

**Charts not displaying:**
- Confirm Plotly is installed and updated
- Check browser console for JavaScript errors
- Try refreshing the page

**Data not filtering correctly:**
- Verify year column exists in datasets
- Check date parsing in `data_loader.py`
- Ensure consistent date formats

**Performance issues:**
- Clear Streamlit cache: Add `?clear_cache=true` to URL
- Reduce data size for testing
- Check memory usage with large datasets

### Development Tips

1. **Use Streamlit's built-in debugging:**
   ```bash
   streamlit run dashboard.py --logger.level=debug
   ```

2. **Enable auto-reload during development:**
   ```python
   # Streamlit watches files and auto-reloads
   # No additional configuration needed
   ```

3. **Test with different data sizes:**
   ```python
   # Add sample data filtering for testing
   if st.checkbox("Use sample data"):
       sales_data = sales_data.sample(1000)
   ```

## Support & Maintenance

### Regular Updates
- Monitor dashboard performance with user feedback
- Update dependencies quarterly for security patches
- Review and optimize data loading performance
- Add new KPIs based on business requirements

### Data Refresh
- Dashboard automatically uses latest data when restarted
- Consider implementing automatic data refresh for production
- Monitor data quality and implement validation checks

This dashboard provides a comprehensive, interactive view of e-commerce business performance with professional styling and real-time analytics capabilities.