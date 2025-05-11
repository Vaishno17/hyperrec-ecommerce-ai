import pandas as pd
import random

class CustomerProfiler:
    def __init__(self, customer_data_path):
        self.customer_data = pd.read_csv(customer_data_path)

    def get_customer_profile(self, customer_id):
        profile = self.customer_data[self.customer_data['id'] == customer_id]
        if profile.empty:
            return None
        record = profile.iloc[0].to_dict()
        # Simulate preferred category & budget if not present
        if 'preferred_category' not in record or pd.isna(record.get('preferred_category')):
            record['preferred_category'] = random.choice(['Fashion', 'Electronics', 'Home', 'Beauty', 'Shoes'])
        if 'budget' not in record or pd.isna(record.get('budget')):
            record['budget'] = random.choice([1000, 2000, 3000, 4000, 5000])
        return record
