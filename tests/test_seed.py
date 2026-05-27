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
            benefit_inserts = re.findall(r"insert into benefits", content, re.IGNORECASE)
            self.assertGreaterEqual(len(benefit_inserts), 8, "Should have at least 8 benefit entries")

    def test_frequencies(self):
        with open('seed.sql', 'r') as f:
            content = f.read().lower()
            # Frequencies must be monthly or yearly based on spec
            self.assertIn("'monthly'", content)
            self.assertIn("'yearly'", content)

    def test_categories_and_uber_cash_spec(self):
        with open('seed.sql', 'r') as f:
            content = f.read()
            
            # 1. Verify Uber Cash category is 'Dining/Travel'
            uber_cash_entries = re.findall(r"SELECT.*?'Uber Cash',\s*[\d\.]+,\s*'(.*?)'", content, re.IGNORECASE)
            self.assertGreater(len(uber_cash_entries), 0, "No Uber Cash entries found")
            for cat in uber_cash_entries:
                self.assertEqual(cat.strip(), 'Dining/Travel', f"Uber Cash category should be 'Dining/Travel', found '{cat}'")

            # 2. Verify Amex Platinum Uber Cash description reflects the $35 bump
            # We look for the statement that contains both 'Uber Cash', '$35 in Dec', and 'Amex Platinum'
            # Each statement ends with a semicolon.
            statements = content.split(';')
            found_plat_uber = False
            for stmt in statements:
                if 'Uber Cash' in stmt and 'Amex Platinum' in stmt:
                    found_plat_uber = True
                    self.assertIn('$35 in Dec', stmt, "Amex Platinum Uber Cash description missing '$35 in Dec' bump info")
            
            self.assertTrue(found_plat_uber, "Could not find Amex Platinum Uber Cash SQL statement")

    def test_general_categories(self):
        allowed_categories = {'dining', 'travel', 'shopping', 'entertainment', 'wellness', 'dining/travel'}
        with open('seed.sql', 'r') as f:
            content = f.read()
            # SELECT id, 'Benefit Name', amount, 'Category', 'Frequency'
            categories = re.findall(r"SELECT.*?,\s*'.*?',\s*[\d\.]+,\s*'(.*?)',", content, re.IGNORECASE)
            
            for cat in categories:
                cat_clean = cat.strip().lower()
                self.assertIn(cat_clean, allowed_categories, f"Category '{cat_clean}' is not in allowed categories")

if __name__ == '__main__':
    unittest.main()
