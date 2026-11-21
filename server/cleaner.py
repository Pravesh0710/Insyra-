import os
import pandas as pd
import numpy as np

# support running directly or as a module
try:
    from server.profiler import load_dataset
except ImportError:
    from profiler import load_dataset


def remove_duplicates(df):
    cleaned_df = df.drop_duplicates()
    duplicates_count = int(df.duplicated().sum())
    print("Duplicate rows found:", duplicates_count)
    return cleaned_df


def handle_missing_values(df, drop_threshold=50):
    cleaned_df = df.copy()

    for col in cleaned_df.columns:
        null_count = cleaned_df[col].isnull().sum()
        if null_count == 0:
            continue

        null_percent = (null_count / len(cleaned_df)) * 100

        # drop if more than threshold% is missing
        if null_percent > drop_threshold:
            print(f"Dropping column '{col}' because {round(null_percent, 1)}% is missing.")
            cleaned_df = cleaned_df.drop(columns=[col])
            continue

        # numeric columns -> fill with median
        if np.issubdtype(cleaned_df[col].dtype, np.number):
            median_val = cleaned_df[col].median()
            cleaned_df[col] = cleaned_df[col].fillna(median_val)
            print(f"Filled missing in '{col}' (numeric) with median: {round(median_val, 2)}")

        # text/categorical columns -> fill with mode
        else:
            non_null_modes = cleaned_df[col].dropna().mode()
            if not non_null_modes.empty:
                mode_val = non_null_modes[0]
                cleaned_df[col] = cleaned_df[col].fillna(mode_val)
                print(f"Filled missing in '{col}' (text) with mode: '{mode_val}'")
            else:
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    return cleaned_df


def clean_text_columns(df, make_lowercase=True):
    df_clean = df.copy()
    text_cols = df_clean.select_dtypes(include=['object']).columns

    for col in text_cols:
        # preserve true missing values while cleaning string values
        mask = df_clean[col].notnull()
        series = df_clean.loc[mask, col].astype(str).str.strip()
        series = series.str.replace(r'\s+', ' ', regex=True)

        if make_lowercase:
            series = series.str.lower()

        df_clean.loc[mask, col] = series

    print(f"Cleaned {len(text_cols)} text columns (spaces stripped & formatted safely).")
    return df_clean


def clean_dataset(file_path, output_dir="cleaned files"):
    print("=" * 45)
    print("STARTING DATA CLEANING PROCESS")
    print("=" * 45)

    df = load_dataset(file_path)
    if df is None:
        print("Error: Could not load file.")
        return None

    initial_rows = len(df)
    initial_cols = len(df.columns)
    print(f"Loaded dataset: {initial_rows} rows, {initial_cols} columns")

    # cleaning steps
    df_clean = remove_duplicates(df)
    df_clean = clean_text_columns(df_clean, make_lowercase=False)
    df_clean = handle_missing_values(df_clean)

    # make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(file_path)
    output_filename = f"cleaned_{base_name}"
    output_path = os.path.join(output_dir, output_filename)

    df_clean.to_csv(output_path, index=False)

    final_rows = len(df_clean)
    final_cols = len(df_clean.columns)

    print("=" * 45)
    print("CLEANING COMPLETED SUCCESSFULLY!")
    print(f"Rows: {initial_rows} -> {final_rows} (removed {initial_rows - final_rows})")
    print(f"Cols: {initial_cols} -> {final_cols}")
    print(f"Saved to: {output_path}")
    print("=" * 45)

    return {
        "original_file": file_path,
        "cleaned_file": output_path,
        "rows_before": initial_rows,
        "rows_after": final_rows,
        "columns_before": initial_cols,
        "columns_after": final_cols,
        "rows_removed": initial_rows - final_rows
    }


if __name__ == "__main__":
    input_file = "server/netflix_customer_churn.csv"
    clean_dataset(input_file)
