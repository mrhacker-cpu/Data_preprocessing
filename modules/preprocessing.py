import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA

# ---------------- CLEANING ----------------
def remove_nulls(df):
    
    return df.dropna()

def fill_nulls(df):
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna("Unknown", inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

    return df

def drop_duplicates(df):
    return df.drop_duplicates()

# ---------------- TRANSFORMATION ----------------
def encode_categorical(df):
    return pd.get_dummies(df)

def minmax_scale(df):
    scaler = MinMaxScaler()
    num_cols = df.select_dtypes(include='number').columns
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df

def standard_scale(df):
    scaler = StandardScaler()
    num_cols = df.select_dtypes(include='number').columns
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df

# ---------------- INTEGRATION ----------------
def merge_data(dfs):
    return pd.concat(dfs, ignore_index=True)

def join_data(df1, df2, on_col):
    return df1.merge(df2, on=on_col, how='inner')

# ---------------- REDUCTION ----------------
def sample_data(df, frac=0.5):
    return df.sample(frac=frac)

def apply_pca(df, n_components=2):
    num_cols = df.select_dtypes(include='number')
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(num_cols)
    return pd.DataFrame(reduced, columns=[f'PC{i+1}' for i in range(n_components)])