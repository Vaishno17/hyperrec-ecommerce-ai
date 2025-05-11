# tests/test_recommendations.py
import unittest
from agents.customer_profiler import CustomerProfiler

class TestCustomerProfiler(unittest.TestCase):
    def setUp(self):
        self.profiler = CustomerProfiler('data/customer_data_collection.csv')

    def test_get_customer_profile(self):
        profile = self.profiler.get_customer_profile(1)
        self.assertIsNotNone(profile)

if __name__ == '__main__':
    unittest.main()
