# src/backend/services/inventory_service.py

import os
import pandas as pd

def fetch_inventory():
    """
    Reads inventory data from CSV or Database and returns a list/dict.
    For the MVP, we’ll assume CSV read.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to point to your data folder
    data_path = os.path.join(base_dir, '../../../data/cleaned_data.csv')

    
    df = pd.read_csv(data_path)
    # Return as a list of dicts for easy JSON serialization
    return df.to_dict(orient='records')
import math

def _load_inventory_df():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../../../data/cleaned_data.csv')
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['delivery_time'] = pd.to_datetime(df['delivery_time'], errors='coerce')
    return df.dropna(subset=['date', 'delivery_time']).copy()


def fetch_inventory():
    """
    Returns full historical inventory records.
    """
    df = _load_inventory_df().copy()
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['delivery_time'] = df['delivery_time'].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')


def fetch_inventory_summary():
    """
    Returns the latest stock snapshot per item.
    """
    df = _load_inventory_df()
    latest = (
        df.sort_values('date')
        .groupby('item', as_index=False)
        .tail(1)
        .sort_values('stock', ascending=True)
    )
    latest['date'] = latest['date'].dt.strftime('%Y-%m-%d')
    latest['delivery_time'] = latest['delivery_time'].dt.strftime('%Y-%m-%d')
    return latest[['item', 'stock', 'sold', 'date', 'delivery_time']].to_dict(orient='records')


def fetch_reorder_plan(horizon_days=14, safety_days=2, lookback_days=60):
    """
    Creates reorder recommendations using average demand and lead-time-aware reorder points.
    """
    df = _load_inventory_df()

    latest_date = df['date'].max()
    window_start = latest_date - pd.Timedelta(days=lookback_days)
    demand_window = df[df['date'] >= window_start]

    demand_stats = (
        demand_window.groupby('item', as_index=False)['sold']
        .mean()
        .rename(columns={'sold': 'avg_daily_demand'})
    )

    lead_time = (df['delivery_time'] - df['date']).dt.days.clip(lower=0)
    df = df.assign(lead_time_days=lead_time)
    lead_time_stats = (
        df.groupby('item', as_index=False)['lead_time_days']
        .mean()
        .rename(columns={'lead_time_days': 'avg_lead_time_days'})
    )

    latest_stock = (
        df.sort_values('date')
        .groupby('item', as_index=False)
        .tail(1)[['item', 'stock']]
        .rename(columns={'stock': 'current_stock'})
    )

    merged = latest_stock.merge(demand_stats, on='item', how='left').merge(lead_time_stats, on='item', how='left')
    merged['avg_daily_demand'] = merged['avg_daily_demand'].fillna(0.0)
    merged['avg_lead_time_days'] = merged['avg_lead_time_days'].fillna(0.0)

    merged['reorder_point'] = (
        merged['avg_daily_demand'] * (merged['avg_lead_time_days'] + safety_days)
    )
    merged['target_stock'] = (
        merged['avg_daily_demand'] * (merged['avg_lead_time_days'] + horizon_days)
    )
    merged['recommended_order_qty'] = (
        (merged['target_stock'] - merged['current_stock']).clip(lower=0).apply(math.ceil)
    )
    merged['days_until_stockout'] = merged.apply(
        lambda row: None if row['avg_daily_demand'] <= 0 else round(row['current_stock'] / row['avg_daily_demand'], 1),
        axis=1,
    )
    merged['risk_level'] = merged.apply(
        lambda row: 'high' if row['current_stock'] <= row['reorder_point'] else 'normal',
        axis=1,
    )

    merged = merged.sort_values(['risk_level', 'days_until_stockout'], ascending=[True, True], na_position='last')

    numeric_cols = ['avg_daily_demand', 'avg_lead_time_days', 'reorder_point', 'target_stock']
    for col in numeric_cols:
        merged[col] = merged[col].round(2)

    return merged[
        [
            'item',
            'current_stock',
            'avg_daily_demand',
            'avg_lead_time_days',
            'reorder_point',
            'target_stock',
            'recommended_order_qty',
            'days_until_stockout',
            'risk_level',
        ]
    ].to_dict(orient='records')
