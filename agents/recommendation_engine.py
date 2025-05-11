import pandas as pd

class RecommendationEngine:
    def __init__(self, product_data_path):
        self.product_data = pd.read_csv(product_data_path)

    def recommend_products(self, customer_profile):
        df = self.product_data

        preferred_cat = customer_profile.get('preferred_category', None)
        budget = customer_profile.get('budget', None)

        filtered = df
        if preferred_cat:
            filtered = filtered[filtered['category'] == preferred_cat]
        if budget:
            filtered = filtered[filtered['price'] <= budget]

        if filtered.empty:
            filtered = df

        sample_n = min(8, len(filtered))
        return filtered.sample(n=sample_n).to_dict(orient='records')
