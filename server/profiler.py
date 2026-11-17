import pandas as pd
import numpy as np
import os


def load_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Supported formats: .csv, .xlsx, .xls")



def get_dataset_overview(df):
    memory_bytes = int(df.memory_usage(deep=True).sum())
    duplicate_count = int(df.duplicated().sum())
    total_rows = len(df)
    
    return {
        "total_rows": total_rows,
        "total_columns": int(df.shape[1]),
        "memory_usage_bytes": memory_bytes,
        "duplicate_rows": duplicate_count,
        "duplicate_percentage": round((duplicate_count / total_rows * 100), 2) if total_rows > 0 else 0.0
    }


def get_column_types(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    boolean_cols = df.select_dtypes(include=['bool']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
    
    all_dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    return {
        "all_dtypes": all_dtypes,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "boolean_columns": boolean_cols,
        "datetime_columns": datetime_cols
    }


def get_missing_values(df):
    total_cells = df.size
    total_missing = int(df.isnull().sum().sum())
    missing_by_column = {}
    columns_with_missing = []
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        null_pct = round((null_count / len(df) * 100), 2) if len(df) > 0 else 0.0
        missing_by_column[col] = {
            "missing_count": null_count,
            "missing_percentage": null_pct
        }
        if null_count > 0:
            columns_with_missing.append(col)
            
    return {
        "total_missing_cells": total_missing,
        "overall_missing_percentage": round((total_missing / total_cells * 100), 2) if total_cells > 0 else 0.0,
        "columns_with_missing": columns_with_missing,
        "by_column": missing_by_column
    }


def get_numerical_summary(df):
    numeric_df = df.select_dtypes(include=[np.number])
    summary = {}
    
    for col in numeric_df.columns:
        series = numeric_df[col].dropna()
        if series.empty:
            continue
            
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outlier_count = int(((series < lower_bound) | (series > upper_bound)).sum())
        
        summary[col] = {
            "count": int(series.count()),
            "mean": round(float(series.mean()), 4),
            "std": round(float(series.std()), 4) if series.count() > 1 else 0.0,
            "min": round(float(series.min()), 4),
            "25%": round(q1, 4),
            "median": round(float(series.median()), 4),
            "75%": round(q3, 4),
            "max": round(float(series.max()), 4),
            "skewness": round(float(series.skew()), 4) if series.count() > 2 else 0.0,
            "iqr": round(iqr, 4),
            "outlier_count": outlier_count,
            "outlier_percentage": round((outlier_count / len(series) * 100), 2) if len(series) > 0 else 0.0
        }
    return summary


def get_categorical_summary(df, top_n=5):
    """Compute cardinality and top frequent categories for categorical columns."""
    categorical_df = df.select_dtypes(include=['object', 'category'])
    summary = {}
    
    for col in categorical_df.columns:
        series = categorical_df[col].dropna().astype(str)
        distinct_count = int(series.nunique())
        value_counts = series.value_counts().head(top_n)
        
        top_categories = [
            {
                "value": val,
                "count": int(count),
                "percentage": round((count / len(series) * 100), 2) if len(series) > 0 else 0.0
            }
            for val, count in value_counts.items()
        ]
        
        summary[col] = {
            "distinct_count": distinct_count,
            "top_categories": top_categories
        }
    return summary


def get_correlations(df, threshold=0.7):
    """Identify highly correlated numeric column pairs."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return {"high_correlations": []}
        
    corr_matrix = numeric_df.corr()
    high_corr = []
    cols = numeric_df.columns
    
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                high_corr.append({
                    "column_1": cols[i],
                    "column_2": cols[j],
                    "correlation": round(float(val), 4)
                })
                
    return {"high_correlations": high_corr}


def get_data_quality_warnings(df, overview, missing_info, num_summary, cat_summary):
    """Generate automatic business alerts and data quality warnings."""
    warnings = []
    
    if overview["duplicate_rows"] > 0:
        warnings.append({
            "type": "DUPLICATES",
            "severity": "medium",
            "message": f"Dataset contains {overview['duplicate_rows']} duplicate rows ({overview['duplicate_percentage']}%)."
        })
        
    for col, stats in missing_info["by_column"].items():
        if stats["missing_percentage"] > 40.0:
            warnings.append({
                "type": "HIGH_MISSING_VALUES",
                "severity": "high",
                "column": col,
                "message": f"Column '{col}' has {stats['missing_percentage']}% missing values. Consider imputation or dropping."
            })
            
    for col, stats in cat_summary.items():
        if stats["distinct_count"] == 1:
            warnings.append({
                "type": "ZERO_VARIANCE",
                "severity": "high",
                "column": col,
                "message": f"Column '{col}' has only 1 distinct value (constant column)."
            })
        elif stats["distinct_count"] == overview["total_rows"] and overview["total_rows"] > 1:
            warnings.append({
                "type": "HIGH_CARDINALITY",
                "severity": "low",
                "column": col,
                "message": f"Column '{col}' has 100% unique values (likely an ID or identifier)."
            })
            
    for col, stats in num_summary.items():
        if stats["outlier_percentage"] > 5.0:
            warnings.append({
                "type": "OUTLIERS_DETECTED",
                "severity": "medium",
                "column": col,
                "message": f"Column '{col}' has {stats['outlier_count']} outliers ({stats['outlier_percentage']}% of values)."
            })
            
    return warnings


def generate_profile_report(file_or_df):
    """
    Main function: Generates a complete, structured profile report.
    Returns a dictionary suitable for JSON responses or reporting.
    """
    if isinstance(file_or_df, str):
        df = load_dataset(file_or_df)
    else:
        df = file_or_df

    overview = get_dataset_overview(df)
    col_types = get_column_types(df)
    missing = get_missing_values(df)
    num_summary = get_numerical_summary(df)
    cat_summary = get_categorical_summary(df)
    correlations = get_correlations(df)
    warnings = get_data_quality_warnings(df, overview, missing, num_summary, cat_summary)

    return {
        "overview": overview,
        "column_types": col_types,
        "missing_values": missing,
        "numerical_summary": num_summary,
        "categorical_summary": cat_summary,
        "correlations": correlations,
        "quality_warnings": warnings
    }


def print_profile_summary(report):
    """Clean command-line visualizer for the generated report."""
    ov = report["overview"]
    print("=" * 60)
    print("           INSYRA DATASET PROFILING REPORT           ")
    print("=" * 60)
    print(f"Total Rows:            {ov['total_rows']:,}")
    print(f"Total Columns:         {ov['total_columns']}")
    print(f"Duplicate Rows:        {ov['duplicate_rows']} ({ov['duplicate_percentage']}%)")
    print(f"Missing Cells:         {report['missing_values']['total_missing_cells']} ({report['missing_values']['overall_missing_percentage']}%)")
    print("-" * 60)
    
    ct = report["column_types"]
    print(f"Numeric Columns ({len(ct['numeric_columns'])}):       {', '.join(ct['numeric_columns'])}")
    print(f"Categorical Columns ({len(ct['categorical_columns'])}):   {', '.join(ct['categorical_columns'])}")
    print("-" * 60)
    
    print("DATA QUALITY WARNINGS:")
    warnings = report["quality_warnings"]
    if not warnings:
        print("  ✓ No critical data quality issues detected.")
    else:
        for w in warnings:
            print(f"  [{w['severity'].upper()}] {w['message']}")
    print("=" * 60)


if __name__ == "__main__":
    file_path = "server/netflix_customer_churn.csv"
    report = generate_profile_report(file_path)
    print_profile_summary(report)


# alias for convenience
profile_dataset = generate_profile_report

