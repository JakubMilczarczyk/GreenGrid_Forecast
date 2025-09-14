import os
import json
from pathlib import Path
import polars as pl

SCHEMA_DIR = os.getenv('SCHEMA_DIR', './schemas')

TYPE_ALIASES = {
    "datetime64[us]": "datetime(us)",
    "datetime64[ns]": "datetime(ns)",
    "int64": "i64",
    "float64": "f64",
    "bool": "boolean",
}

class SchemaValidationError(Exception):
    """Custom exception for schema mismatches."""


def load_schema(schema_name: str) -> dict:
    schema_path = Path(SCHEMA_DIR) / schema_name
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_dtype(dtype_str: str) -> str:
    """Normalize Polars dtype string to a canonical form."""
    s = dtype_str.lower().replace(" ", "")

    # uproszczenie zapisów typu Datetime(...)
    if s.startswith("datetime("):
        if "us" in s:
            return "datetime(us)"
        elif "ns" in s:
            return "datetime(ns)"
        else:
            return "datetime"

    # mapowanie aliasów
    return TYPE_ALIASES.get(s, s)

def validate_df(df: pl.DataFrame, schema_name: str) -> None:
    """
    Validate a DataFrame against a schema definition.

    Args:
        df (pl.DataFrame): DataFrame to validate
        schema_path (str): Path to schema JSON file

    Raises:
        SchemaValidationError: if schema mismatch
    """
    schema = load_schema(schema_name)

    for col, expected_dtype in schema.items():
        if col not in df.columns:
            raise SchemaValidationError(f"Missing column: {col}")

        actual_dtype = str(df[col].dtype)
        normalized_actual = normalize_dtype(actual_dtype)
        normalized_expected = normalize_dtype(expected_dtype)

        if normalized_actual != normalized_expected:
            raise SchemaValidationError(
                f"Column '{col}' expected {expected_dtype}, got {actual_dtype}"
            )

    print(f"[VALIDATOR] DataFrame matches schema {schema_name}")
