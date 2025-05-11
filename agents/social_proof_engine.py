import pandas as pd

class SocialProofEngine:
    def __init__(self, product_data_path):
        self.product_data = pd.read_csv(product_data_path)

    def get_trending_products(self):
        # Check if popularity column exists
        if 'popularity' in self.product_data.columns:
            df = self.product_data.sort_values(by='popularity', ascending=False)
        elif 'ratings' in self.product_data.columns:
            df = self.product_data.sort_values(by='ratings', ascending=False)
        else:
            # Fallback to sorting by price descending (simulate premium products)
            df = self.product_data.sort_values(by='price', ascending=False)

        top_n = min(6, len(df))
        return df.head(top_n).to_dict(orient='records')
