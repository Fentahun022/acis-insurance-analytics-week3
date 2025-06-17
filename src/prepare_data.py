import pandas as pd
import numpy as np
from pathlib import Path
import logging
import argparse

# Configure basic logging to see detailed output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_column_names(df):
    """Standardizes column names to lowercase and replaces spaces with underscores."""
    logging.info("Cleaning column names...")
    original_columns = df.columns.tolist()
    df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    logging.info(f"Original columns: {original_columns}")
    logging.info(f"Cleaned columns: {df.columns.tolist()}")
    return df

def create_features(df):
    """Engineers new features for risk and profitability analysis."""
    logging.info("Starting feature engineering...")
    
    # --- DIAGNOSTIC: Check if 'transactionmonth' exists before using it ---
    if 'transactionmonth' not in df.columns:
        logging.error("'transactionmonth' column not found! Cannot create 'transactiondate'.")
        # You could raise an error here to stop the script, which is good practice
        raise KeyError("'transactionmonth' column is missing from the raw data.")
    
    # Create 'transactiondate'
    logging.info("Creating 'transactiondate' column...")
    df['transactiondate'] = pd.to_datetime(df['transactionmonth'], format='%b-%y', errors='coerce')
    
    # --- DIAGNOSTIC: Check if parsing worked ---
    successful_parses = df['transactiondate'].notna().sum()
    total_rows = len(df)
    logging.info(f"Successfully parsed {successful_parses}/{total_rows} dates. "
                 f"({total_rows - successful_parses} rows have NaT).")

    if successful_parses == 0:
        logging.warning("Warning: All date parsing failed. The 'transactiondate' column will be all NaT. "
                        "Check the 'format=%b-%y' argument in pd.to_datetime.")

    # Continue with other features...
    financial_cols = ['totalpremium', 'totalclaims', 'customvalueestimate']
    for col in financial_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(subset=['totalpremium', 'totalclaims'], inplace=True)
    df['hasclaim'] = (df['totalclaims'] > 0).astype(int)
    df['margin'] = df['totalpremium'] - df['totalclaims']
    df['lossratio'] = df['totalclaims'] / (df['totalpremium'] + 1e-6)
    
    if 'registrationyear' in df.columns:
        current_year = pd.to_datetime('today').year
        df['vehicleage'] = current_year - pd.to_numeric(df['registrationyear'], errors='coerce')
    
    logging.info("Finished feature engineering.")
    return df

def handle_missing_values(df):
    # (This function can remain the same as before)
    logging.info("Handling missing values...")
    for col in df.columns:
        if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
            df[col].fillna(df[col].mode()[0], inplace=True)
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].median(), inplace=True)
    logging.info(f"Missing values handled. Remaining NaNs: {df.isnull().sum().sum()}")
    return df

def main(input_path, output_path):
    try:
        logging.info(f"Loading raw data from {input_path}...")
        df = pd.read_csv(input_path, sep='|', low_memory=False)
        logging.info("Raw data loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return

    df = clean_column_names(df)
    df = create_features(df)
    df = handle_missing_values(df)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info(f"Processed data saved to {output_path}")

if __name__ == '__main__':
    # This allows you to run the script from the command line
    parser = argparse.ArgumentParser(description="Process ACIS insurance data.")
    parser.add_argument('--input', type=str, default='data/raw/MachineLearningRating_v3.txt', help='Path to the raw data file.')
    parser.add_argument('--output', type=str, default='data/processed/MachineLearningRating_v3.txt', help='Path to save the processed data file.')
    
    args = parser.parse_args()
    
    main(input_path=args.input, output_path=args.output)