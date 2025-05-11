import pandas as pd
import random

class DiscountEngine:
    def __init__(self, product_data_path):
        self.product_data = pd.read_csv(product_data_path)
        self._add_discounts_if_missing()

    def _add_discounts_if_missing(self):
        # Add 'discount' column with random discounts if missing
        if 'discount' not in self.product_data.columns:
            discounts = [random.choice([0, 5, 10, 15, 20, 25, 30]) for _ in range(len(self.product_data))]
            self.product_data['discount'] = discounts

    def get_discounted_products(self):
        discounted = self.product_data[self.product_data['discount'] > 0]
        sample_n = min(6, len(discounted))
        return discounted.sample(sample_n).to_dict(orient='records')
