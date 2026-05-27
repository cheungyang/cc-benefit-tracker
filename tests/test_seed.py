import unittest
import os
import re

class TestSeed(unittest.TestCase):
    def test_seed_file_exists(self):
        self.assertTrue(os.path.exists('seed.sql'), "seed.sql does not exist")

    def test_seed_content(self):
        with open('seed.sql', 'r') as f:
            content = f.read().lower()
            
            # Check for cards
            self.assertIn('amex gold', content)
            self.assertIn('amex platinum', content)
            self.assertIn('chase sapphire reserve', content)
            self.assertIn('capital one venture x', content)
            
            # Check for benefits count (at least 8)
            benefit_inserts = re.findall(r"insert into benefits", content)
            self.assertGreaterEqual(len(benefit_inserts), 8, "Should have at least 8 benefit entries")

    def test_frequencies(self):
        with open('seed.sql', 'r') as f:
            content = f.read().lower()
            # Frequencies must be monthly or yearly based on spec
            self.assertIn("'monthly'", content)
            self.assertIn("'yearly'", content)

    def test_categories(self):
        allowed_categories = {'dining', 'travel', 'shopping', 'entertainment', 'wellness'}
        with open('seed.sql', 'r') as f:
            content = f.read().lower()
            # Find all categories in insert statements
            # Pattern matches something like: 'Dining', 'monthly',
            categories = re.findall(r"insert into benefits.*?values.*?'.*?',\s*.*?,.*?, '(.*?)',", content, re.DOTALL | re.IGNORECASE)
            
            # Since I used subqueries, the pattern might be different.
            # SELECT id, 'Dining Credit', 10.00, 'Dining', 'monthly'
            categories = re.findall(r"select.*?, '.*?', .*?, '(.*?)',", content, re.DOTALL | re.IGNORECASE)
            
            for cat in categories:
                cat = cat.strip().lower()
                self.assertIn(cat, allowed_categories, f"Category '{cat}' is not in allowed categories")

if __name__ == '__main__':
    unittest.main()
