import pandas as pd

class ProductAnalyzer:
    def __init__(self, product_data_path):
        self.product_data = pd.read_csv(product_data_path)

    def get_product_details(self, product_id):
        prod = self.product_data[self.product_data['id'] == product_id]
        if prod.empty:
            return None
        return prod.iloc[0].to_dict()
