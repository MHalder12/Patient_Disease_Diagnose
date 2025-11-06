# src/utils.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# symptom level mapping for ordinal symptoms if represented as strings
SYMPTOM_ORDINAL = {
    "None": 0,
    "Mild": 1,
    "Moderate": 1,
    "High": 2,
    "Severe": 2
}

def fill_missing_values(df):
    """Fill numeric columns with median, categorical with mode."""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype.kind in "biufc":  # numeric
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        else:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode().iloc[0], inplace=True)
    return df

def map_symptom_ordinal(df, cols):
    """Map symptom string levels to ordinal ints (inplace on copy)."""
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).map(SYMPTOM_ORDINAL).fillna(0).astype(int)
    return df

def encode_categoricals(df, exclude_cols=None):
    """
    Label-encode non-numeric columns. Returns (df_encoded, encoders_dict).
    exclude_cols: list of columns to skip (already numeric or target).
    """
    df = df.copy()
    encoders = {}
    exclude_cols = exclude_cols or []
    for col in df.columns:
        if col in exclude_cols:
            continue
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    return df, encoders

def apply_encoders(df, encoders):
    """Apply saved LabelEncoders mapping to a dataframe (for prediction)."""
    df = df.copy()
    for col, le in encoders.items():
        if col in df.columns:
            # transform safely (map unknowns to most frequent class)
            vals = df[col].astype(str).tolist()
            transformed = []
            classes = set(le.classes_)
            for v in vals:
                if v in classes:
                    transformed.append(le.transform([v])[0])
                else:
                    # fallback to mode (class 0)
                    transformed.append(0)
            df[col] = transformed
    return df
