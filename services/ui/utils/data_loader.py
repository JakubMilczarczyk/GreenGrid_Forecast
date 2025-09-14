import pandas as pd 
import datetime

def load_mock_data(model: str, benchmark: str) -> dict:
    """Generate mock data if API is unavaiable."""
    today = datetime.date.today()
    dates = [today - datetime.timedelta(days=i) for i in range(10)][::-1]

    data = {
        'date': dates,
        'actual': [i * 10 for i in range(10)],
        'predicted': [i * 10 + 5 for i in range(10)],
    }
    return data
