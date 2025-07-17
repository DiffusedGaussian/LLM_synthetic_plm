import pandas as pd
from pathlib import Path

def load_raw(path:Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=None, dtype=str)
    # guess header row: first row where ≥70 % cells are non-null & unique
    for i, row in df.iterrows():
        non_null = row.notna().sum()
        unique   = row.nunique(dropna=True)
        if non_null / len(row) > 0.7 and unique == non_null:
            header_idx = i
            break
    df = pd.read_excel(path, header=header_idx, dtype=str)
    # drop columns that are entirely null or duplicate
    df = df.dropna(axis=1, how="all").loc[:, ~df.columns.duplicated()]
    return df

