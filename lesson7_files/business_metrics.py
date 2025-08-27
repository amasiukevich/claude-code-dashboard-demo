"""
Business Metrics Calculation Module for E-commerce Analysis

This module provides functions for calculating key business metrics
from e-commerce sales data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Optional, List
import numpy as np


# Set consistent style for all plots
plt.style.use('default')
BUSINESS_COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'success': '#F18F01',
    'neutral': '#C73E1D',
    'light': '#F5F5F5'
}

def calculate_revenue_metrics(
    current_data: pd.DataFrame, 
    comparison_data: pd.DataFrame = None,
    period_name: str = "Current Period"
) -> Dict:
    """
    Calculate revenue metrics for a given period with optional comparison.
    
    Args:
        current_data: Sales data for current period
        comparison_data: Sales data for comparison period (optional)
        period_name: Name of the current period for reporting
        
    Returns:
        Dictionary with revenue metrics
    """
    metrics = {
        'period': period_name,
        'total_revenue': current_data['price'].sum(),
        'total_orders': current_data['order_id'].nunique(),
        'total_items': len(current_data),
        'average_order_value': current_data.groupby('order_id')['price'].sum().mean(),
        'average_item_price': current_data['price'].mean()
    }
    
    if comparison_data is not None:
        comparison_revenue = comparison_data['price'].sum()
        comparison_orders = comparison_data['order_id'].nunique()
        comparison_aov = comparison_data.groupby('order_id')['price'].sum().mean()
        
        metrics.update({
            'revenue_growth_rate': (metrics['total_revenue'] - comparison_revenue) / comparison_revenue * 100,
            'order_growth_rate': (metrics['total_orders'] - comparison_orders) / comparison_orders * 100,
            'aov_growth_rate': (metrics['average_order_value'] - comparison_aov) / comparison_aov * 100,
            'comparison_revenue': comparison_revenue,
            'comparison_orders': comparison_orders,
            'comparison_aov': comparison_aov
        })
    
    return metrics


def calculate_monthly_trends(data: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Calculate month-over-month growth trends for a specific year.
    
    Args:
        data: Sales data with order_month column
        year: Year to analyze
        
    Returns:
        DataFrame with monthly metrics and growth rates
    """
    yearly_data = data[data['order_year'] == year].copy()
    
    monthly_stats = yearly_data.groupby('order_month').agg({
        'price': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    monthly_stats.columns = ['month', 'revenue', 'orders']
    monthly_stats['aov'] = yearly_data.groupby('order_month').apply(
        lambda x: x.groupby('order_id')['price'].sum().mean()
    ).values
    
    # Calculate growth rates
    monthly_stats['revenue_growth'] = monthly_stats['revenue'].pct_change() * 100
    monthly_stats['order_growth'] = monthly_stats['orders'].pct_change() * 100
    monthly_stats['aov_growth'] = monthly_stats['aov'].pct_change() * 100
    
    return monthly_stats


def calculate_product_performance(product_sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate product category performance metrics.
    
    Args:
        product_sales_data: Sales data with product category information
        
    Returns:
        DataFrame with category performance metrics
    """
    category_metrics = product_sales_data.groupby('product_category_name').agg({
        'price': ['sum', 'mean', 'count'],
    }).round(2)
    
    # Flatten column names
    category_metrics.columns = ['total_revenue', 'avg_price', 'total_items']
    category_metrics = category_metrics.reset_index()
    
    # Calculate percentages
    total_revenue = category_metrics['total_revenue'].sum()
    category_metrics['revenue_percentage'] = (
        category_metrics['total_revenue'] / total_revenue * 100
    ).round(2)
    
    return category_metrics.sort_values('total_revenue', ascending=False)


def calculate_geographic_performance(geographic_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate geographic performance metrics by state.
    
    Args:
        geographic_data: Sales data with customer state information
        
    Returns:
        DataFrame with state-level performance metrics
    """
    state_metrics = geographic_data.groupby('customer_state').agg({
        'price': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    state_metrics.columns = ['state', 'total_revenue', 'total_orders']
    state_metrics['avg_order_value'] = (
        state_metrics['total_revenue'] / state_metrics['total_orders']
    ).round(2)
    
    # Calculate percentages
    total_revenue = state_metrics['total_revenue'].sum()
    state_metrics['revenue_percentage'] = (
        state_metrics['total_revenue'] / total_revenue * 100
    ).round(2)
    
    return state_metrics.sort_values('total_revenue', ascending=False)


def calculate_customer_satisfaction_metrics(review_data: pd.DataFrame) -> Dict:
    """
    Calculate customer satisfaction and delivery performance metrics.
    
    Args:
        review_data: Data with review scores and delivery information
        
    Returns:
        Dictionary with satisfaction metrics
    """
    metrics = {
        'average_review_score': review_data['review_score'].mean(),
        'total_reviews': len(review_data),
        'review_distribution': review_data['review_score'].value_counts(normalize=True).sort_index(),
        'average_delivery_days': review_data['delivery_days'].mean(),
        'delivery_category_distribution': review_data['delivery_category'].value_counts(normalize=True)
    }
    
    # Calculate satisfaction by delivery speed
    if 'delivery_category' in review_data.columns:
        metrics['satisfaction_by_delivery'] = review_data.groupby('delivery_category')['review_score'].mean()
    
    return metrics


def calculate_order_status_metrics(orders_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate order status distribution metrics.
    
    Args:
        orders_data: Orders data with status information
        
    Returns:
        DataFrame with order status metrics
    """
    status_metrics = orders_data['order_status'].value_counts(normalize=True).reset_index()
    status_metrics.columns = ['order_status', 'percentage']
    status_metrics['percentage'] = (status_metrics['percentage'] * 100).round(2)
    status_metrics['count'] = orders_data['order_status'].value_counts().values
    
    return status_metrics


def plot_revenue_trend(monthly_data: pd.DataFrame, year: int, title_suffix: str = "") -> plt.Figure:
    """
    Create revenue trend visualization.
    
    Args:
        monthly_data: DataFrame with monthly revenue data
        year: Year being analyzed
        title_suffix: Additional text for title
        
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Revenue trend
    ax1.plot(monthly_data['month'], monthly_data['revenue'], 
             marker='o', linewidth=2, color=BUSINESS_COLORS['primary'])
    ax1.set_title(f'Monthly Revenue Trend {year}{title_suffix}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Revenue ($)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=0)
    
    # Format y-axis as currency
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Growth rate
    ax2.bar(monthly_data['month'], monthly_data['revenue_growth'], 
            color=BUSINESS_COLORS['secondary'], alpha=0.7)
    ax2.set_title(f'Month-over-Month Revenue Growth Rate {year}{title_suffix}', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Growth Rate (%)')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    plt.tight_layout()
    return fig


def plot_category_performance(category_data: pd.DataFrame, title_suffix: str = "") -> plt.Figure:
    """
    Create product category performance visualization.
    
    Args:
        category_data: DataFrame with category performance data
        title_suffix: Additional text for title
        
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Revenue by category
    top_categories = category_data.head(10)
    bars1 = ax1.bar(range(len(top_categories)), top_categories['total_revenue'], 
                    color=BUSINESS_COLORS['primary'])
    ax1.set_title(f'Revenue by Product Category{title_suffix}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Product Category')
    ax1.set_ylabel('Total Revenue ($)')
    ax1.set_xticks(range(len(top_categories)))
    ax1.set_xticklabels(top_categories['product_category_name'], rotation=45, ha='right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    # Revenue percentage pie chart
    ax2.pie(top_categories['revenue_percentage'], labels=top_categories['product_category_name'],
            autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    ax2.set_title(f'Revenue Share by Category{title_suffix}', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_geographic_performance(state_data: pd.DataFrame, title_suffix: str = "") -> plt.Figure:
    """
    Create geographic performance visualization with interactive map.
    
    Args:
        state_data: DataFrame with state performance data
        title_suffix: Additional text for title
        
    Returns:
        matplotlib Figure object or plotly figure
    """
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Create interactive choropleth map
        fig = px.choropleth(
            state_data,
            locations='state',
            color='total_revenue',
            locationmode='USA-states',
            scope='usa',
            title=f'Revenue by State{title_suffix}',
            color_continuous_scale='Blues',
            hover_data={
                'state': True,
                'total_revenue': ':$,.0f',
                'total_orders': ':,',
                'avg_order_value': ':$.0f',
                'revenue_percentage': ':.1f%'
            },
            labels={
                'total_revenue': 'Total Revenue ($)',
                'state': 'State',
                'total_orders': 'Orders',
                'avg_order_value': 'AOV ($)',
                'revenue_percentage': 'Revenue %'
            }
        )
        
        # Update layout for better appearance
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='albers usa'
            ),
            coloraxis_colorbar=dict(
                title="Revenue ($)",
                tickformat="$,.0s"
            )
        )
        
        # Show the interactive map
        fig.show()
        
        # Also create a complementary scatter plot
        scatter_fig = px.scatter(
            state_data.head(20),  # Top 20 states
            x='total_orders',
            y='avg_order_value',
            size='total_revenue',
            color='revenue_percentage',
            hover_data={
                'state': True,
                'total_revenue': ':$,.0f'
            },
            title=f'Orders vs AOV by State (Top 20){title_suffix}',
            labels={
                'total_orders': 'Total Orders',
                'avg_order_value': 'Average Order Value ($)',
                'revenue_percentage': 'Revenue Share (%)'
            }
        )
        
        scatter_fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            showlegend=True
        )
        
        # Add state labels for top performers
        top_states = state_data.head(10)
        for idx, row in top_states.iterrows():
            scatter_fig.add_annotation(
                x=row['total_orders'],
                y=row['avg_order_value'],
                text=row['state'],
                showarrow=False,
                font=dict(size=10),
                xanchor="center",
                yanchor="bottom"
            )
        
        scatter_fig.show()
        
        return None  # Return None since we're showing interactive plots
        
    except ImportError:
        # Fallback to matplotlib if plotly is not available
        print("Plotly not available. Using matplotlib fallback...")
        return _plot_geographic_performance_matplotlib(state_data, title_suffix)


def _plot_geographic_performance_matplotlib(state_data: pd.DataFrame, title_suffix: str = "") -> plt.Figure:
    """
    Fallback matplotlib version of geographic performance visualization.
    
    Args:
        state_data: DataFrame with state performance data
        title_suffix: Additional text for title
        
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top states by revenue
    top_states = state_data.head(15)
    bars = ax1.barh(range(len(top_states)), top_states['total_revenue'], 
                    color=BUSINESS_COLORS['success'])
    ax1.set_title(f'Revenue by State (Top 15){title_suffix}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Total Revenue ($)')
    ax1.set_ylabel('State')
    ax1.set_yticks(range(len(top_states)))
    ax1.set_yticklabels(top_states['state'])
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_states['total_revenue'])):
        ax1.text(value + value*0.01, bar.get_y() + bar.get_height()/2,
                f'${value:,.0f}', va='center', fontsize=9)
    
    # Average order value by state
    ax2.scatter(top_states['total_orders'], top_states['avg_order_value'], 
                s=top_states['total_revenue']/1000, alpha=0.6, color=BUSINESS_COLORS['neutral'])
    ax2.set_title(f'Orders vs AOV by State{title_suffix}', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Total Orders')
    ax2.set_ylabel('Average Order Value ($)')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Add state labels for top performers
    for i, row in top_states.head(5).iterrows():
        ax2.annotate(row['state'], (row['total_orders'], row['avg_order_value']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    return fig


def plot_customer_satisfaction(review_data: pd.DataFrame, title_suffix: str = "") -> plt.Figure:
    """
    Create customer satisfaction visualization.
    
    Args:
        review_data: DataFrame with review and delivery data
        title_suffix: Additional text for title
        
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Review score distribution
    review_counts = review_data['review_score'].value_counts().sort_index()
    bars1 = ax1.barh(review_counts.index, review_counts.values, color=BUSINESS_COLORS['primary'])
    ax1.set_title(f'Review Score Distribution{title_suffix}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Number of Reviews')
    ax1.set_ylabel('Review Score')
    
    # Add percentage labels
    total_reviews = len(review_data)
    for bar, count in zip(bars1, review_counts.values):
        percentage = count / total_reviews * 100
        ax1.text(bar.get_width() + bar.get_width()*0.01, bar.get_y() + bar.get_height()/2,
                f'{percentage:.1f}%', va='center', fontsize=10)
    
    # Satisfaction by delivery category
    if 'delivery_category' in review_data.columns:
        satisfaction_by_delivery = review_data.groupby('delivery_category')['review_score'].mean()
        bars2 = ax2.bar(range(len(satisfaction_by_delivery)), satisfaction_by_delivery.values,
                       color=BUSINESS_COLORS['secondary'])
        ax2.set_title(f'Average Rating by Delivery Speed{title_suffix}', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Delivery Category')
        ax2.set_ylabel('Average Review Score')
        ax2.set_xticks(range(len(satisfaction_by_delivery)))
        ax2.set_xticklabels(satisfaction_by_delivery.index, rotation=45)
        ax2.set_ylim(0, 5)
        
        # Add value labels
        for bar, value in zip(bars2, satisfaction_by_delivery.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'{value:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    return fig


def generate_business_summary(metrics: Dict, period_name: str) -> str:
    """
    Generate a business summary report from metrics.
    
    Args:
        metrics: Dictionary of calculated metrics
        period_name: Name of the period being analyzed
        
    Returns:
        Formatted summary string
    """
    summary = f"\n=== BUSINESS PERFORMANCE SUMMARY - {period_name.upper()} ===\n"
    summary += f"Total Revenue: ${metrics['total_revenue']:,.2f}\n"
    summary += f"Total Orders: {metrics['total_orders']:,}\n"
    summary += f"Average Order Value: ${metrics['average_order_value']:.2f}\n"
    
    if 'revenue_growth_rate' in metrics:
        summary += f"\n=== YEAR-OVER-YEAR COMPARISON ===\n"
        summary += f"Revenue Growth: {metrics['revenue_growth_rate']:.2f}%\n"
        summary += f"Order Growth: {metrics['order_growth_rate']:.2f}%\n"
        summary += f"AOV Growth: {metrics['aov_growth_rate']:.2f}%\n"
    
    return summary