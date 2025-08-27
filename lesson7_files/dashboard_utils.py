"""
Dashboard Utilities Module
Helper functions for creating charts and formatting data for the Streamlit dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional

# Color schemes for consistency
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

def format_value_for_chart(value: float, chart_type: str = 'currency') -> str:
    """
    Format values for chart display based on type.
    
    Args:
        value: Numeric value to format
        chart_type: Type of formatting ('currency', 'percentage', 'number')
    
    Returns:
        Formatted string
    """
    if chart_type == 'currency':
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"${value/1_000:.0f}K"
        else:
            return f"${value:,.0f}"
    elif chart_type == 'percentage':
        return f"{value:.1f}%"
    elif chart_type == 'number':
        if value >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.0f}K"
        else:
            return f"{value:,.0f}"
    else:
        return str(value)

def create_kpi_card_data(current_value: float, previous_value: float, 
                        metric_name: str, format_type: str = 'currency') -> Dict:
    """
    Create KPI card data with trend indicators.
    
    Args:
        current_value: Current period value
        previous_value: Previous period value
        metric_name: Name of the metric
        format_type: How to format the values
    
    Returns:
        Dictionary with formatted values and trend indicators
    """
    if previous_value == 0:
        change_pct = 0
        trend_direction = 'neutral'
    else:
        change_pct = ((current_value - previous_value) / previous_value) * 100
        trend_direction = 'positive' if change_pct > 0 else 'negative' if change_pct < 0 else 'neutral'
    
    return {
        'name': metric_name,
        'current_value': format_value_for_chart(current_value, format_type),
        'previous_value': format_value_for_chart(previous_value, format_type),
        'change_percentage': change_pct,
        'trend_direction': trend_direction,
        'trend_arrow': '↗' if trend_direction == 'positive' else '↘' if trend_direction == 'negative' else '→'
    }

def create_enhanced_line_chart(current_data: pd.DataFrame, previous_data: pd.DataFrame,
                              x_col: str, y_col: str, title: str,
                              current_label: str, previous_label: str) -> go.Figure:
    """
    Create enhanced line chart with current and previous period comparison.
    
    Args:
        current_data: Current period data
        previous_data: Previous period data  
        x_col: X-axis column name
        y_col: Y-axis column name
        title: Chart title
        current_label: Label for current period line
        previous_label: Label for previous period line
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Current period line (solid)
    fig.add_trace(go.Scatter(
        x=current_data[x_col],
        y=current_data[y_col],
        mode='lines+markers',
        name=current_label,
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8, color=COLORS['primary']),
        hovertemplate=f'<b>{current_label}</b><br>' +
                     f'{x_col.title()}: %{{x}}<br>' +
                     f'{y_col.title()}: $%{{y:,.0f}}<extra></extra>'
    ))
    
    # Previous period line (dashed) if data exists
    if not previous_data.empty:
        fig.add_trace(go.Scatter(
            x=previous_data[x_col],
            y=previous_data[y_col],
            mode='lines+markers',
            name=previous_label,
            line=dict(color=COLORS['secondary'], width=2, dash='dash'),
            marker=dict(size=6, color=COLORS['secondary']),
            hovertemplate=f'<b>{previous_label}</b><br>' +
                         f'{x_col.title()}: %{{x}}<br>' +
                         f'{y_col.title()}: $%{{y:,.0f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=COLORS['dark'])),
        xaxis=dict(
            title=x_col.replace('_', ' ').title(),
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title=y_col.replace('_', ' ').title(),
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            tickformat='$,.0f'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=350
    )
    
    return fig

def create_horizontal_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                               title: str, top_n: int = 10) -> go.Figure:
    """
    Create horizontal bar chart with gradient colors.
    
    Args:
        data: DataFrame with data
        x_col: X-axis column (values)
        y_col: Y-axis column (categories)
        title: Chart title
        top_n: Number of top items to show
    
    Returns:
        Plotly figure object
    """
    # Get top N items
    top_data = data.head(top_n).copy()
    
    fig = px.bar(
        top_data,
        x=x_col,
        y=y_col,
        orientation='h',
        title=title,
        color=x_col,
        color_continuous_scale='Blues',
        text=x_col
    )
    
    # Format text on bars
    fig.update_traces(
        texttemplate='%{text:$,.0s}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=11),
        xaxis=dict(
            title="Revenue",
            tickformat='$,.0f',
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(title="", categoryorder="total ascending"),
        showlegend=False,
        coloraxis_showscale=False,
        title=dict(font=dict(size=16, color=COLORS['dark']))
    )
    
    return fig

def create_us_choropleth_map(state_data: pd.DataFrame, title: str = "Revenue by State") -> go.Figure:
    """
    Create US choropleth map for geographic data visualization.
    
    Args:
        state_data: DataFrame with state-level data
        title: Map title
    
    Returns:
        Plotly figure object
    """
    fig = px.choropleth(
        state_data,
        locations='state',
        color='total_revenue',
        locationmode='USA-states',
        scope='usa',
        title=title,
        color_continuous_scale='Blues',
        hover_data={
            'state': True,
            'total_revenue': ':$,.0f',
            'total_orders': ':,',
            'avg_order_value': ':$.0f',
            'revenue_percentage': ':.1f%'
        },
        labels={
            'total_revenue': 'Revenue',
            'total_orders': 'Orders',
            'avg_order_value': 'AOV',
            'revenue_percentage': 'Revenue %'
        }
    )
    
    fig.update_layout(
        height=350,
        title=dict(font=dict(size=16, color=COLORS['dark'])),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            bgcolor='white',
            projection_type='albers usa'
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Revenue", font=dict(size=12)),
            tickformat="$,.0s",
            len=0.7
        )
    )
    
    return fig

def create_satisfaction_bar_chart(review_data: pd.DataFrame, title: str = "Customer Satisfaction by Delivery Speed") -> go.Figure:
    """
    Create bar chart showing satisfaction vs delivery time.
    
    Args:
        review_data: DataFrame with review and delivery data
        title: Chart title
    
    Returns:
        Plotly figure object
    """
    # Group by delivery category and calculate average satisfaction
    satisfaction_by_delivery = review_data.groupby('delivery_category')['review_score'].mean().reset_index()
    
    # Sort delivery categories properly
    category_order = ['1-3 days', '4-7 days', '8+ days']
    satisfaction_by_delivery['delivery_category'] = pd.Categorical(
        satisfaction_by_delivery['delivery_category'], 
        categories=category_order, 
        ordered=True
    )
    satisfaction_by_delivery = satisfaction_by_delivery.sort_values('delivery_category')
    
    fig = px.bar(
        satisfaction_by_delivery,
        x='delivery_category',
        y='review_score',
        title=title,
        color='review_score',
        color_continuous_scale='Blues',
        text='review_score'
    )
    
    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>'
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title="Delivery Time Category",
            showgrid=False
        ),
        yaxis=dict(
            title="Average Review Score",
            range=[3.5, 5.0],
            showgrid=True,
            gridcolor='lightgray',
            tickformat='.1f'
        ),
        showlegend=False,
        coloraxis_showscale=False,
        title=dict(font=dict(size=16, color=COLORS['dark']))
    )
    
    return fig

def create_metric_card_html(title: str, value: str, delta: str = None, 
                           delta_color: str = 'neutral') -> str:
    """
    Create HTML for a metric card.
    
    Args:
        title: Card title
        value: Main value to display
        delta: Change indicator (optional)
        delta_color: Color for delta (positive, negative, neutral)
    
    Returns:
        HTML string for the metric card
    """
    delta_colors = {
        'positive': '#28a745',
        'negative': '#dc3545', 
        'neutral': '#6c757d'
    }
    
    delta_html = ""
    if delta:
        color = delta_colors.get(delta_color, delta_colors['neutral'])
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

def format_stars_display(rating: float) -> Tuple[str, str]:
    """
    Create star display for ratings.
    
    Args:
        rating: Numeric rating (1-5)
    
    Returns:
        Tuple of (rating_text, stars_text)
    """
    stars = "⭐" * int(round(rating))
    return f"{rating:.2f}", stars

def calculate_trend_indicators(current_metrics: Dict, previous_metrics: Dict) -> Dict:
    """
    Calculate trend indicators for multiple metrics.
    
    Args:
        current_metrics: Current period metrics
        previous_metrics: Previous period metrics
    
    Returns:
        Dictionary with trend indicators
    """
    trends = {}
    
    for key in current_metrics:
        if key in previous_metrics:
            current = current_metrics[key]
            previous = previous_metrics[key]
            
            if previous != 0:
                change_pct = ((current - previous) / previous) * 100
                if change_pct > 0:
                    trends[key] = {'direction': 'positive', 'value': f"↗ {change_pct:.2f}%"}
                elif change_pct < 0:
                    trends[key] = {'direction': 'negative', 'value': f"↘ {abs(change_pct):.2f}%"}
                else:
                    trends[key] = {'direction': 'neutral', 'value': "→ 0.00%"}
            else:
                trends[key] = {'direction': 'neutral', 'value': "N/A"}
    
    return trends