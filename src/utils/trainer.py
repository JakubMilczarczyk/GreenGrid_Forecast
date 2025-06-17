"""Script to train the forecasting model."""

from pathlib import Path
import polars as pl

train_features_path = Path(__file__).parent.parent.parent / "data" / "processed"
train_features_path.mkdir(parents=True, exist_ok=True)
train_features_file = train_features_path / "train_features.parquet"

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """Cleans the input DataFrame by removing rows with NaN values."""
    df_nulls = df.filter(pl.any_horizontal(pl.all().is_null()))
    print(f'Null values found: {df_nulls.shape[0]}')
    return df.drop_nulls()

if __name__ == '__main__':
    # Load the training features
    df = pl.read_parquet(train_features_file)
    print(f'Loaded training features from {train_features_file}')

    # Clean data
    df_cleaned = clean_data(df)
    print(f'Cleaned data shape: {df_cleaned.shape}')

