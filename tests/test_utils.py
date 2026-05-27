import unittest
from datetime import date
from app.utils import get_window_id, get_window_info, get_previous_window_id

class TestUtils(unittest.TestCase):
    def test_window_id_monthly(self):
        d = date(2026, 5, 15)
        self.assertEqual(get_window_id(d, 'monthly'), '2026-05')
        
    def test_window_id_quarterly(self):
        self.assertEqual(get_window_id(date(2026, 2, 1), 'quarterly'), '2026-Q1')
        self.assertEqual(get_window_id(date(2026, 5, 1), 'quarterly'), '2026-Q2')
        self.assertEqual(get_window_id(date(2026, 8, 1), 'quarterly'), '2026-Q3')
        self.assertEqual(get_window_id(date(2026, 11, 1), 'quarterly'), '2026-Q4')

    def test_window_id_semiannually(self):
        self.assertEqual(get_window_id(date(2026, 3, 1), 'semiannually'), '2026-H1')
        self.assertEqual(get_window_id(date(2026, 9, 1), 'semiannually'), '2026-H2')

    def test_window_id_yearly(self):
        self.assertEqual(get_window_id(date(2026, 7, 1), 'yearly'), '2026')

    def test_previous_window_id(self):
        # Monthly
        self.assertEqual(get_previous_window_id(date(2026, 5, 15), 'monthly'), '2026-04')
        self.assertEqual(get_previous_window_id(date(2026, 1, 15), 'monthly'), '2025-12')
        # Quarterly
        self.assertEqual(get_previous_window_id(date(2026, 5, 1), 'quarterly'), '2026-Q1')
        self.assertEqual(get_previous_window_id(date(2026, 1, 1), 'quarterly'), '2025-Q4')
        # Semiannually
        self.assertEqual(get_previous_window_id(date(2026, 8, 1), 'semiannually'), '2026-H1')
        self.assertEqual(get_previous_window_id(date(2026, 3, 1), 'semiannually'), '2025-H2')
        # Yearly
        self.assertEqual(get_previous_window_id(date(2026, 5, 1), 'yearly'), '2025')

    def test_window_info_monthly(self):
        d = date(2026, 5, 26)
        info = get_window_info(d, 'monthly')
        self.assertEqual(info['reset_date'], date(2026, 6, 1))
        self.assertEqual(info['days_remaining'], 6)

    def test_window_info_leap_year(self):
        d = date(2024, 2, 28)
        info = get_window_info(d, 'monthly')
        self.assertEqual(info['reset_date'], date(2024, 3, 1))
        self.assertEqual(info['days_remaining'], 2) 

if __name__ == '__main__':
    unittest.main()
