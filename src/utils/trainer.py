"""Script to train the forecasting model."""

from pathlib import Path
import joblib
import polars as pl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

train_features_path = Path(__file__).parent.parent.parent / "data" / "processed"
train_features_path.mkdir(parents=True, exist_ok=True)
train_features_file = train_features_path / "train_features.parquet"

models_path = Path(__file__).parent.parent.parent / "models" / "saved_models"
models_path.mkdir(parents=True, exist_ok=True)
model_file = models_path / 'linear_regression_model.joblib'

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """Cleans the input DataFrame by removing rows with NaN values."""
    df_nulls = df.filter(pl.any_horizontal(pl.all().is_null()))
    print(f'Null values found: {df_nulls.shape[0]}')
    return df.drop_nulls()

def prepare_data(df: pl.DataFrame) -> tuple:
    """Prepares the data for training by splitting into features and target."""
    df = df_cleaned.to_pandas()
    df_encoded = pd.get_dummies(df, columns=['business_type'])

    x = df_encoded.drop(columns=['actual_OZE_MWh', 'timestamp'])
    y = df_encoded['actual_OZE_MWh']
    return x, y

if __name__ == '__main__':
    # Load the training features
    df = pl.read_parquet(train_features_file)
    print(f'Loaded training features from {train_features_file}')

    # Clean data
    df_cleaned = clean_data(df)
    print(f'Cleaned data shape: {df_cleaned.shape}')
    
    x, y = prepare_data(df_cleaned)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42
        )

    model = LinearRegression()
    model.fit(x_train, y_train)

    # Przewiduj wartości na danych testowych
    y_pred = model.predict(x_test)

    # Oblicz błąd średniokwadratowy (MSE)
    mse = mean_squared_error(y_test, y_pred)

    # Oblicz współczynnik determinacji (R2)
    r2 = r2_score(y_test, y_pred)

    print(f'''
    training complete successfully with score:
        Błąd średniokwadratowy (MSE): {mse}
        Współczynnik determinacji (R2): {r2}
    ''')

    joblib.dump(model, model_file)
    print(f'Model saved successfully as {model_file}')
