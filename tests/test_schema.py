import unittest
import os

class TestSchema(unittest.TestCase):
    def test_schema_file_exists(self):
        self.assertTrue(os.path.exists('schema.sql'), "schema.sql does not exist")

    def test_tables_defined(self):
        with open('schema.sql', 'r') as f:
            content = f.read().lower()
            self.assertIn('create table cards', content)
            self.assertIn('create table user_cards', content)
            self.assertIn('create table benefits', content)
            self.assertIn('create table claims', content)

    def test_unique_constraint_on_claims(self):
        with open('schema.sql', 'r') as f:
            content = f.read().lower()
            # Check for unique constraint on benefit_id and window_id
            self.assertIn('unique (benefit_id, window_id)', content)

    def test_foreign_keys(self):
        with open('schema.sql', 'r') as f:
            content = f.read().lower()
            self.assertIn('references cards(id)', content)
            self.assertIn('references benefits(id)', content)

    def test_enum_frequency(self):
        with open('schema.sql', 'r') as f:
            content = f.read().lower()
            self.assertIn('create type benefit_frequency as enum', content)
            self.assertIn("'monthly'", content)
            self.assertIn("'quarterly'", content)
            self.assertIn("'semiannually'", content)
            self.assertIn("'yearly'", content)

if __name__ == '__main__':
    unittest.main()
