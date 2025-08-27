"""
E-commerce Business Dashboard
Professional Streamlit dashboard for e-commerce business performance analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from data_loader import (
    load_raw_data, clean_and_prepare_orders, create_sales_dataset,
    filter_delivered_orders, filter_by_date_range, add_delivery_metrics,
    create_product_sales_data, create_geographic_sales_data, 
    create_review_analysis_data
)
from business_metrics import (
    calculate_revenue_metrics, calculate_monthly_trends, 
    calculate_product_performance, calculate_geographic_performance,
    calculate_customer_satisfaction_metrics
)

# Page configuration
st.set_page_config(
    page_title="E-commerce Business Dashboard", 
    page_icon="👟", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .main .block-container {
        background-color: #1e1e1e;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
        background-color: #1e1e1e;
    }
    
    /* Dark theme styling */
    .stApp, .main, .block-container {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #404040;
        box-shadow: 0 2px 4px rgba(255,255,255,0.1);
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        color: #00d4ff;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #cccccc;
        margin-bottom: 0.5rem;
    }
    
    /* Trend indicators */
    .trend-positive {
        color: #00ff88;
    }
    .trend-negative {
        color: #ff4444;
    }
    .trend-neutral {
        color: #cccccc;
    }
    
    /* Selectbox styling for dark theme - fix dropdown cutoff */
    .stSelectbox {
        background-color: #2d2d2d;
        position: relative;
        z-index: 999;
    }
    
    .stSelectbox > div {
        overflow: visible !important;
        position: relative;
        z-index: 999;
    }
    
    /* Ensure column containers don't clip dropdowns */
    .element-container {
        overflow: visible !important;
    }
    
    .stColumn > div {
        overflow: visible !important;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        min-height: 50px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
        overflow: visible !important;
    }
    
    .stSelectbox label {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 10px !important;
        display: block !important;
    }
    
    /* Force selectbox text to be visible and dropdown to appear properly */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2d2d2d !important;
        border: 1px solid #404040 !important;
        position: relative;
        z-index: 999;
        overflow: visible !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Dropdown menu styling */
    .stSelectbox div[data-baseweb="popover"] {
        z-index: 9999 !important;
        position: fixed !important;
        background-color: #2d2d2d !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1) !important;
        max-height: 200px !important;
        overflow-y: auto !important;
        transform: translateY(0) !important;
    }
    
    .stSelectbox div[role="listbox"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        max-height: 200px !important;
        overflow-y: auto !important;
    }
    
    .stSelectbox div[role="option"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
    }
    
    .stSelectbox div[role="option"]:hover {
        background-color: #404040 !important;
        color: #00d4ff !important;
    }
    
    /* Text and labels */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }
    
    /* Sidebar and other components */
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    
    /* Streamlit metrics styling for dark theme */
    div[data-testid="metric-container"] {
        background-color: #2d2d2d !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 212, 255, 0.1) !important;
    }
    
    div[data-testid="metric-container"] > div {
        color: #ffffff !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #cccccc !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        color: #00d4ff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="metric-delta"] {
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Plotly charts background and text clarity for dark theme */
    .js-plotly-plot, .plotly {
        background-color: #2d2d2d !important;
    }
    
    /* Fix chart text for dark theme */
    .plotly .gtitle, .plotly .xtitle, .plotly .ytitle {
        font-family: "Arial", sans-serif !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .plotly .tick text {
        font-family: "Arial", sans-serif !important;
        color: #ffffff !important;
        font-size: 12px !important;
    }
    
    /* Metric values should be large and clear */
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #00d4ff !important;
        line-height: 1.1 !important;
    }
    
    .metric-delta {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Debug checkbox styling */
    .stCheckbox {
        color: #ffffff !important;
    }
    
    .stCheckbox > label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_prepare_data():
    """Load and prepare all data for dashboard"""
    # Load raw data
    orders, order_items, products, customers, reviews = load_raw_data('ecommerce_data')
    
    # Clean and prepare data
    orders_clean = clean_and_prepare_orders(orders)
    sales_data = create_sales_dataset(orders_clean, order_items)
    sales_delivered = filter_delivered_orders(sales_data)
    sales_with_delivery = add_delivery_metrics(sales_delivered)
    
    return sales_with_delivery, orders_clean, products, customers, reviews

def format_currency(value):
    """Format currency values for display"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage values for display"""
    return f"{value:+.2f}%"

def get_trend_indicator(current, previous):
    """Get trend indicator with color and arrow"""
    if previous == 0:
        return "0.00%", "neutral"
    
    change = ((current - previous) / previous) * 100
    if change > 0:
        return f"↗ {change:.2f}%", "positive"
    elif change < 0:
        return f"↘ {abs(change):.2f}%", "negative"
    else:
        return "→ 0.00%", "neutral"

def create_revenue_trend_chart(current_monthly, previous_monthly, current_year, previous_year):
    """Create revenue trend line chart"""
    fig = go.Figure()
    
    # Current period line (solid)
    fig.add_trace(go.Scatter(
        x=current_monthly['month'],
        y=current_monthly['revenue'],
        mode='lines+markers',
        name=f'{current_year}',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    # Previous period line (dashed)
    if not previous_monthly.empty:
        fig.add_trace(go.Scatter(
            x=previous_monthly['month'],
            y=previous_monthly['revenue'],
            mode='lines+markers',
            name=f'{previous_year}',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            marker=dict(size=6),
            hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text="Monthly Revenue Trend",
            font=dict(size=16, color='#ffffff', family='Arial, sans-serif')
        ),
        xaxis_title="Month",
        yaxis_title="Revenue",
        showlegend=True,
        height=350,
        plot_bgcolor='#2d2d2d',
        paper_bgcolor='#2d2d2d',
        font=dict(size=13, color='#ffffff', family='Arial, sans-serif'),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#404040',
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#404040', 
            tickformat='$,.0f',
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff')
        )
    )
    
    return fig

def create_category_bar_chart(category_data):
    """Create top 10 categories bar chart"""
    top_10 = category_data.head(10)
    
    fig = px.bar(
        top_10, 
        x='total_revenue', 
        y='product_category_name',
        orientation='h',
        title="Top 10 Product Categories by Revenue",
        color='total_revenue',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='#2d2d2d',
        paper_bgcolor='#2d2d2d',
        font=dict(size=11, color='#ffffff'),
        title=dict(
            font=dict(size=16, color='#ffffff', family='Arial, sans-serif')
        ),
        xaxis=dict(
            title="Revenue", 
            tickformat='$,.0f',
            title_font=dict(color='#ffffff'),
            tickfont=dict(color='#ffffff'),
            showgrid=True,
            gridcolor='#404040'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color='#ffffff')
        ),
        showlegend=False,
        coloraxis_showscale=False
    )
    
    fig.update_yaxes(categoryorder="total ascending")
    
    return fig

def create_state_choropleth(state_data):
    """Create US state choropleth map"""
    fig = px.choropleth(
        state_data,
        locations='state',
        color='total_revenue',
        locationmode='USA-states',
        scope='usa',
        title='Revenue by State',
        color_continuous_scale='Viridis',
        hover_data={
            'state': True,
            'total_revenue': ':$,.0f',
            'total_orders': ':,',
            'avg_order_value': ':$.0f'
        }
    )
    
    fig.update_layout(
        height=350,
        paper_bgcolor='#2d2d2d',
        plot_bgcolor='#2d2d2d',
        font=dict(color='#ffffff'),
        title=dict(
            font=dict(size=16, color='#ffffff', family='Arial, sans-serif')
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            bgcolor='#2d2d2d'
        ),
        coloraxis_colorbar=dict(
            title="Revenue",
            tickformat="$,.0s",
            title_font=dict(color='#ffffff'),
            tickfont=dict(color='#ffffff')
        )
    )
    
    return fig

def create_satisfaction_delivery_chart(review_analysis):
    """Create satisfaction vs delivery time bar chart"""
    # Group by delivery category
    satisfaction_by_delivery = review_analysis.groupby('delivery_category')['review_score'].mean().reset_index()
    satisfaction_by_delivery = satisfaction_by_delivery.sort_values('delivery_category')
    
    fig = px.bar(
        satisfaction_by_delivery,
        x='delivery_category',
        y='review_score',
        title="Customer Satisfaction by Delivery Speed",
        color='review_score',
        color_continuous_scale='Plasma'
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='#2d2d2d',
        paper_bgcolor='#2d2d2d',
        font=dict(color='#ffffff'),
        title=dict(
            font=dict(size=16, color='#ffffff', family='Arial, sans-serif')
        ),
        xaxis=dict(
            title="Delivery Time",
            title_font=dict(color='#ffffff'),
            tickfont=dict(color='#ffffff'),
            showgrid=True,
            gridcolor='#404040'
        ),
        yaxis=dict(
            title="Average Review Score",
            range=[3.5, 5],
            title_font=dict(color='#ffffff'),
            tickfont=dict(color='#ffffff'),
            showgrid=True,
            gridcolor='#404040'
        ),
        showlegend=False,
        coloraxis_showscale=False
    )
    
    return fig

def main():
    # Load data
    sales_data, orders_clean, products, customers, reviews = load_and_prepare_data()
    
    # Header with title - ensure proper spacing
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    st.title("👟 Shoe Company Sales Dashboard")
    
    # Date filters below the title
    st.markdown("### Filters")
    col2, col3 = st.columns(2)
    
    with col2:
        # Year selection with improved visibility
        available_years = sorted(sales_data['order_year'].unique())
        # Set default to 2023 if available, otherwise latest year
        default_year = 2023 if 2023 in available_years else available_years[-1]
        default_index = available_years.index(default_year)
        
        # Add container div for proper dropdown display
        st.markdown("<div style='margin-bottom: 10px;'><strong>📅 Select Year:</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='position: relative; z-index: 999; margin-bottom: 20px;'>", unsafe_allow_html=True)
        selected_year = st.selectbox(
            "Year",
            options=available_years,
            index=default_index,
            key="year_selector",
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        # Month selection with improved visibility
        months = ['All Months'] + [f'{i:02d} - {pd.to_datetime(f"2023-{i:02d}-01").strftime("%B")}' for i in range(1, 13)]
        
        # Add container div for proper dropdown display
        st.markdown("<div style='margin-bottom: 10px;'><strong>📊 Select Month:</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='position: relative; z-index: 999; margin-bottom: 20px;'>", unsafe_allow_html=True)
        selected_month = st.selectbox(
            "Month",
            options=months,
            index=0,
            key="month_selector",
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Extract month number or None for all months
        if selected_month == 'All Months':
            month_filter = None
        else:
            month_filter = int(selected_month.split(' - ')[0])
    
    comparison_year = selected_year - 1 if selected_year > min(available_years) else selected_year
    
    # Filter data based on selection
    current_data = filter_by_date_range(sales_data, year=selected_year, month=month_filter)
    previous_data = filter_by_date_range(sales_data, year=comparison_year, month=month_filter)
    
    # Calculate metrics
    current_metrics = calculate_revenue_metrics(current_data, previous_data, str(selected_year))
    
    # Debug: Show what metrics we have (temporary)
    if st.checkbox("Debug: Show raw metrics", value=False):
        st.write("Current metrics:", current_metrics)
        st.write("Current data shape:", current_data.shape if not current_data.empty else "Empty")
        st.write("Previous data shape:", previous_data.shape if not previous_data.empty else "Empty")
    
    # KPI Row - 4 cards
    st.markdown("### Key Performance Indicators")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        # Revenue metric with clear formatting
        revenue_value = format_currency(current_metrics.get('total_revenue', 0))
        if 'revenue_growth_rate' in current_metrics and current_metrics['revenue_growth_rate'] is not None:
            revenue_change = current_metrics['revenue_growth_rate']
            revenue_delta = f"{revenue_change:+.2f}%" if revenue_change != 0 else "0.00%"
        else:
            revenue_delta = None
        
        st.metric(
            label="💰 Total Revenue",
            value=revenue_value,
            delta=revenue_delta
        )
    
    with kpi_col2:
        # Growth rate display
        growth_rate = current_metrics.get('revenue_growth_rate', 0)
        if growth_rate is not None and growth_rate != 0:
            growth_value = f"{growth_rate:+.2f}%"
            growth_label = "📈 YoY Growth"
        else:
            growth_value = "0.00%"
            growth_label = "📈 YoY Growth"
        
        st.metric(
            label=growth_label,
            value=growth_value,
            delta=None
        )
    
    with kpi_col3:
        # Average Order Value
        aov = current_metrics.get('average_order_value', 0)
        aov_value = f"${aov:.0f}"
        if 'aov_growth_rate' in current_metrics and current_metrics['aov_growth_rate'] is not None:
            aov_change = current_metrics['aov_growth_rate']
            aov_delta = f"{aov_change:+.2f}%" if aov_change != 0 else "0.00%"
        else:
            aov_delta = None
            
        st.metric(
            label="🛒 Average Order Value",
            value=aov_value,
            delta=aov_delta
        )
    
    with kpi_col4:
        # Total Orders
        orders = current_metrics.get('total_orders', 0)
        orders_value = f"{orders:,}"
        if 'order_growth_rate' in current_metrics and current_metrics['order_growth_rate'] is not None:
            orders_change = current_metrics['order_growth_rate']
            orders_delta = f"{orders_change:+.2f}%" if orders_change != 0 else "0.00%"
        else:
            orders_delta = None
            
        st.metric(
            label="📦 Total Orders",
            value=orders_value,
            delta=orders_delta
        )
    
    st.markdown("---")
    
    # Charts Grid - 2x2 layout
    st.markdown("### Analytics Dashboard")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Revenue trend chart
        current_monthly = calculate_monthly_trends(sales_data, selected_year)
        previous_monthly = calculate_monthly_trends(sales_data, comparison_year) if comparison_year != selected_year else pd.DataFrame()
        
        revenue_chart = create_revenue_trend_chart(current_monthly, previous_monthly, selected_year, comparison_year)
        st.plotly_chart(revenue_chart, use_container_width=True)
    
    with chart_col2:
        # Top 10 categories chart
        product_sales = create_product_sales_data(current_data, products)
        category_performance = calculate_product_performance(product_sales)
        
        category_chart = create_category_bar_chart(category_performance)
        st.plotly_chart(category_chart, use_container_width=True)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        # Geographic performance map
        geographic_sales = create_geographic_sales_data(current_data, orders_clean, customers)
        state_performance = calculate_geographic_performance(geographic_sales)
        
        state_chart = create_state_choropleth(state_performance)
        st.plotly_chart(state_chart, use_container_width=True)
    
    with chart_col4:
        # Satisfaction vs delivery time
        review_analysis = create_review_analysis_data(current_data, reviews)
        
        satisfaction_chart = create_satisfaction_delivery_chart(review_analysis)
        st.plotly_chart(satisfaction_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Bottom Row - 2 cards
    st.markdown("### Customer Experience Metrics")
    
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        # Average delivery time
        avg_delivery = review_analysis['delivery_days'].mean()
        previous_review = create_review_analysis_data(previous_data, reviews) if not previous_data.empty else pd.DataFrame()
        prev_delivery = previous_review['delivery_days'].mean() if not previous_review.empty else avg_delivery
        
        delivery_trend, delivery_color = get_trend_indicator(avg_delivery, prev_delivery)
        st.metric(
            label="Average Delivery Time",
            value=f"{avg_delivery:.1f} days",
            delta=delivery_trend
        )
    
    with bottom_col2:
        # Review score with stars
        satisfaction_metrics = calculate_customer_satisfaction_metrics(review_analysis)
        avg_score = satisfaction_metrics['average_review_score']
        
        # Create star display
        stars = "⭐" * int(round(avg_score))
        
        col_score1, col_score2 = st.columns([1, 2])
        with col_score1:
            st.markdown(f"<h1 style='margin: 0; color: #00d4ff; font-weight: 700;'>{avg_score:.2f}</h1>", unsafe_allow_html=True)
        with col_score2:
            st.markdown(f"<h2 style='margin: 0; color: #ffaa00;'>{stars}</h2>", unsafe_allow_html=True)
        
        st.markdown("<p style='margin: 0; color: #cccccc; font-weight: 600;'>Average Review Score</p>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"*Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data for {selected_year}*")

if __name__ == "__main__":
    main()