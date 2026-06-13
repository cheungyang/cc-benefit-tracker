import pytest
import os
import re

SQL_FILE = 'schema.sql'

def read_sql():
    if not os.path.exists(SQL_FILE):
        return ""
    with open(SQL_FILE, 'r') as f:
        return f.read().lower()

def test_users_table_columns():
    content = read_sql()
    assert 'create table users' in content
    assert 'email varchar(255)' in content
    assert 'password_hash text' in content
    assert 'created_at timestamptz' in content

def test_issuers_table_columns():
    content = read_sql()
    assert 'create table issuers' in content
    assert 'name varchar(100)' in content

def test_cards_table_columns():
    content = read_sql()
    assert 'create table cards' in content
    assert 'user_id uuid' in content
    assert 'issuer_id uuid' in content
    assert 'card_name varchar(255)' in content
    assert 'annual_fee decimal(10, 2)' in content
    assert 'renewal_date date' in content

def test_benefits_table_columns():
    content = read_sql()
    assert 'create table benefits' in content
    assert 'card_id uuid' in content
    assert 'name varchar(255)' in content
    assert 'total_value decimal(10, 2)' in content
    assert 'reset_cycle varchar(50)' in content

def test_benefit_usage_table_columns():
    content = read_sql()
    assert 'create table benefit_usage' in content
    assert 'benefit_id uuid' in content
    assert 'user_id uuid' in content
    assert 'amount_used decimal(10, 2)' in content
    assert 'transaction_date date' in content

def test_uuids_used_as_primary_keys():
    content = read_sql()
    tables = ['users', 'issuers', 'cards', 'benefits', 'benefit_usage']
    for table in tables:
        pattern = rf'create table {table}\s*\(\s*id\s+uuid\s+primary\s+key'
        assert re.search(pattern, content) is not None, f"Table {table} does not use UUID for primary key"

def test_indices_exist():
    content = read_sql()
    assert 'create index idx_usage_benefit_date on benefit_usage(benefit_id, transaction_date)' in content
    assert 'create index idx_cards_user on cards(user_id)' in content

def test_foreign_keys_exist():
    content = read_sql()
    assert 'references users(id)' in content
    assert 'references issuers(id)' in content
    assert 'references cards(id)' in content
    assert 'references benefits(id)' in content
