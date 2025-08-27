"""
Data Loading and Processing Module for E-commerce Analysis

This module provides functions for loading, cleaning, and preparing 
e-commerce data for analysis.
"""

import pandas as pd
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


def load_raw_data(data_path: str = 'ecommerce_data') -> Tuple[pd.DataFrame, ...]:
    """
    Load all raw datasets from CSV files.
    
    Args:
        data_path: Path to the directory containing CSV files
        
    Returns:
        Tuple of DataFrames: orders, order_items, products, customers, reviews
    """
    orders = pd.read_csv(f'{data_path}/orders_dataset.csv')
    order_items = pd.read_csv(f'{data_path}/order_items_dataset.csv')
    products = pd.read_csv(f'{data_path}/products_dataset.csv')
    customers = pd.read_csv(f'{data_path}/customers_dataset.csv')
    reviews = pd.read_csv(f'{data_path}/order_reviews_dataset.csv')
    
    return orders, order_items, products, customers, reviews


def clean_and_prepare_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare orders data with proper datetime parsing.
    
    Args:
        orders: Raw orders DataFrame
        
    Returns:
        Cleaned orders DataFrame with datetime columns and extracted date parts
    """
    orders_clean = orders.copy()
    
    # Convert datetime columns
    datetime_cols = [
        'order_purchase_timestamp',
        'order_approved_at', 
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for col in datetime_cols:
        if col in orders_clean.columns:
            orders_clean[col] = pd.to_datetime(orders_clean[col])
    
    # Extract date components from purchase timestamp
    orders_clean['order_year'] = orders_clean['order_purchase_timestamp'].dt.year
    orders_clean['order_month'] = orders_clean['order_purchase_timestamp'].dt.month
    orders_clean['order_day'] = orders_clean['order_purchase_timestamp'].dt.day
    
    return orders_clean


def create_sales_dataset(orders: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    """
    Create consolidated sales dataset by merging orders and order items.
    
    Args:
        orders: Cleaned orders DataFrame
        order_items: Raw order items DataFrame
        
    Returns:
        Merged sales DataFrame
    """
    sales_data = pd.merge(
        left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
        right=orders[[
            'order_id', 'order_status', 'order_purchase_timestamp', 
            'order_delivered_customer_date', 'order_year', 'order_month'
        ]],
        on='order_id',
        how='inner'
    )
    
    return sales_data


def filter_delivered_orders(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter sales data to include only delivered orders.
    
    Args:
        sales_data: Raw sales DataFrame
        
    Returns:
        DataFrame with only delivered orders
    """
    return sales_data[sales_data['order_status'] == 'delivered'].copy()


def filter_by_date_range(
    data: pd.DataFrame, 
    year: Optional[int] = None, 
    month: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None
) -> pd.DataFrame:
    """
    Filter data by specified date range.
    
    Args:
        data: DataFrame with order_year and order_month columns
        year: Specific year to filter (mutually exclusive with start_year/end_year)
        month: Specific month to filter (requires year)
        start_year: Start year for range filtering
        end_year: End year for range filtering
        
    Returns:
        Filtered DataFrame
    """
    filtered_data = data.copy()
    
    if year is not None:
        filtered_data = filtered_data[filtered_data['order_year'] == year]
        if month is not None:
            filtered_data = filtered_data[filtered_data['order_month'] == month]
    elif start_year is not None and end_year is not None:
        filtered_data = filtered_data[
            (filtered_data['order_year'] >= start_year) & 
            (filtered_data['order_year'] <= end_year)
        ]
    elif start_year is not None:
        filtered_data = filtered_data[filtered_data['order_year'] >= start_year]
    elif end_year is not None:
        filtered_data = filtered_data[filtered_data['order_year'] <= end_year]
    
    return filtered_data


def add_delivery_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add delivery performance metrics to sales data.
    
    Args:
        sales_data: Sales DataFrame with delivery dates
        
    Returns:
        DataFrame with delivery speed metrics
    """
    data_with_delivery = sales_data.copy()
    
    # Ensure datetime format
    data_with_delivery['order_delivered_customer_date'] = pd.to_datetime(
        data_with_delivery['order_delivered_customer_date']
    )
    
    # Calculate delivery days
    data_with_delivery['delivery_days'] = (
        data_with_delivery['order_delivered_customer_date'] - 
        data_with_delivery['order_purchase_timestamp']
    ).dt.days
    
    # Categorize delivery speed
    def categorize_delivery_speed(days):
        if pd.isna(days):
            return 'Unknown'
        elif days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'
    
    data_with_delivery['delivery_category'] = data_with_delivery['delivery_days'].apply(
        categorize_delivery_speed
    )
    
    return data_with_delivery


def create_product_sales_data(sales_data: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """
    Create dataset with product category information.
    
    Args:
        sales_data: Sales DataFrame
        products: Products DataFrame
        
    Returns:
        DataFrame with product category information
    """
    return pd.merge(
        left=products[['product_id', 'product_category_name']],
        right=sales_data[['product_id', 'price', 'order_year', 'order_month']],
        on='product_id',
        how='inner'
    )


def create_geographic_sales_data(
    sales_data: pd.DataFrame, 
    orders: pd.DataFrame, 
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Create dataset with geographic sales information.
    
    Args:
        sales_data: Sales DataFrame
        orders: Orders DataFrame  
        customers: Customers DataFrame
        
    Returns:
        DataFrame with geographic sales information
    """
    # Merge sales with customer info through orders
    sales_customers = pd.merge(
        left=sales_data[['order_id', 'price']],
        right=orders[['order_id', 'customer_id']],
        on='order_id',
        how='inner'
    )
    
    return pd.merge(
        left=sales_customers,
        right=customers[['customer_id', 'customer_state', 'customer_city']],
        on='customer_id',
        how='inner'
    )


def create_review_analysis_data(sales_data: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Create dataset combining sales and review information.
    
    Args:
        sales_data: Sales DataFrame with delivery metrics
        reviews: Reviews DataFrame
        
    Returns:
        DataFrame with review and delivery information
    """
    return pd.merge(
        left=sales_data[[
            'order_id', 'delivery_days', 'delivery_category'
        ]].drop_duplicates(),
        right=reviews[['order_id', 'review_score']],
        on='order_id',
        how='inner'
    )


def get_data_summary(data: pd.DataFrame, data_name: str) -> dict:
    """
    Get summary statistics for a dataset.
    
    Args:
        data: DataFrame to summarize
        data_name: Name of the dataset
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'dataset': data_name,
        'rows': len(data),
        'columns': len(data.columns),
        'date_range': {
            'start': data['order_year'].min() if 'order_year' in data.columns else None,
            'end': data['order_year'].max() if 'order_year' in data.columns else None
        },
        'memory_usage': f"{data.memory_usage(deep=True).sum() / 1024**2:.1f} MB"
    }