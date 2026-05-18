"""
northcommerce_preprocess.py
CLI preprocessing pipeline for CommerceInsight.
- Load CSVs
- Validate and clean data
- City normalisation (regex map)
- KNN impute for Quantity
- Mode fill for delivery_status by city
- Add time features and festival windows
- Export to Parquet and cleaned CSV
"""
import argparse
from pathlib import Path
import re

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

FESTIVAL_WINDOWS = {
    'Diwali': [('2018-10-15','2018-11-15')],
    'Lohri': [('2018-01-10','2018-01-20')],
    'Baisakhi': [('2018-04-10','2018-04-20')],
    'Holi': [('2018-03-20','2018-03-30')]
}

CITY_CANONICAL = {
    # small example map - extend to ~50 entries in production
    r'^ludhiana.*': 'Ludhiana',
    r'^amritsar.*': 'Amritsar',
    r'^patiala.*': 'Patiala',
    r'^jalandhar.*': 'Jalandhar',
    r'^bathinda.*': 'Bathinda'
}


def normalise_city(name: str) -> str:
    if pd.isna(name):
        return name
    name = str(name).strip()
    for pat, canon in CITY_CANONICAL.items():
        if re.match(pat, name, flags=re.IGNORECASE):
            return canon
    # fallback: title case
    return name.title()


def load_csvs(base_path: Path) -> pd.DataFrame:
    path = base_path / 'merged_orders.csv'
    if not path.exists():
        raise FileNotFoundError(f'Missing {path}')
    df = pd.read_csv(path)
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    # parse dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    # drop rows without order id or date
    df = df.dropna(subset=['Order ID','Order Date'])
    # remove negative GMV rows
    df = df[df['Amount'] >= 0]
    # deduplicate by order id, keep last
    df = df.sort_values('Order Date').drop_duplicates('Order ID', keep='last')
    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    df['City'] = df['City'].apply(normalise_city)
    # fill delivery_status by city mode
    if 'delivery_status' in df.columns:
        city_mode = df.groupby('City')['delivery_status'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
        df['delivery_status'] = df.apply(lambda row: city_mode.get(row['City']) if pd.isna(row.get('delivery_status')) else row.get('delivery_status'), axis=1)
    # cap GMV at 99th percentile
    cap = df['Amount'].quantile(0.99)
    df['Amount'] = df['Amount'].clip(upper=cap)
    # impute Quantity with KNN on Amount and Profit
    if 'Quantity' in df.columns:
        knn_cols = ['Amount','Profit','Quantity']
        knn_df = df[knn_cols].copy()
        imputer = KNNImputer(n_neighbors=5)
        knn_df[['Amount','Profit','Quantity']] = imputer.fit_transform(knn_df)
        df['Quantity'] = knn_df['Quantity']
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df['year'] = df['Order Date'].dt.year
    df['month'] = df['Order Date'].dt.month
    df['month_start'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    df['week_start'] = df['Order Date'].dt.to_period('W').dt.start_time
    df['weekday'] = df['Order Date'].dt.weekday
    # festival flags
    for fest, ranges in FESTIVAL_WINDOWS.items():
        df[f'is_{fest.lower()}'] = False
        for start,end in ranges:
            s = pd.to_datetime(start)
            e = pd.to_datetime(end)
            df.loc[(df['Order Date'] >= s) & (df['Order Date'] <= e), f'is_{fest.lower()}'] = True
    return df


def detect_anomalies(df: pd.DataFrame, top_n=5):
    # simple z-score on weekly revenue per state
    weekly = df.groupby(['week_start','State'])['Amount'].sum().reset_index()
    weekly['mean_state'] = weekly.groupby('State')['Amount'].transform('mean')
    weekly['std_state'] = weekly.groupby('State')['Amount'].transform('std').fillna(0)
    weekly['z'] = (weekly['Amount'] - weekly['mean_state']) / weekly['std_state'].replace(0, np.nan)
    anomalies = weekly.sort_values('z').head(top_n)
    print('Top anomalies:')
    print(anomalies[['week_start','State','Amount','z']])
    return anomalies


def export(df: pd.DataFrame, base_path: Path):
    out = base_path.parent / 'data'
    out.mkdir(exist_ok=True)
    csv_path = out / 'merged_orders_cleaned.csv'
    pq_path = out / 'merged_orders_cleaned.parquet'
    df.to_csv(csv_path, index=False)
    df.to_parquet(pq_path, index=False)
    print(f'Saved cleaned CSV to {csv_path} and Parquet to {pq_path}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default=str(Path(__file__).resolve().parents[1]), help='repo root')
    args = parser.parse_args()
    base = Path(args.repo)
    try:
        df = load_csvs(base / 'data')
    except FileNotFoundError:
        df = load_csvs(base)
    df = validate(df)
    df = clean_orders(df)
    df = add_time_features(df)
    anomalies = detect_anomalies(df)
    export(df, base)

if __name__ == '__main__':
    main()
