import pandas as pd

class DataLoader:
    def __init__(self, path):
        self.path = path

    def load_csv(self):
        df = pd.read_csv(self.path)
        df = df.rename(columns=str.lower)

        required = ["timestamp", "open", "high", "low", "close", "volume"]

        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df.to_dict("records")
