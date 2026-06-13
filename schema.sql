-- PostgreSQL 15+ Schema for Credit Card Benefit Tracker

-- Extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for user email
CREATE INDEX idx_users_email ON users(email);

-- 2. issuers
CREATE TABLE issuers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL
);

-- 3. cards
CREATE TABLE cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    issuer_id UUID NOT NULL REFERENCES issuers(id) ON DELETE RESTRICT,
    card_name VARCHAR(255) NOT NULL,
    annual_fee DECIMAL(10, 2) DEFAULT 0.00,
    renewal_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for cards by user
CREATE INDEX idx_cards_user ON cards(user_id);

-- 4. benefits
CREATE TABLE benefits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    card_id UUID NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    total_value DECIMAL(10, 2) NOT NULL,
    reset_cycle VARCHAR(50) NOT NULL, -- Enum: 'monthly', 'calendar_year', 'card_anniversary'
    category VARCHAR(100) NOT NULL
);

-- 5. benefit_usage
CREATE TABLE benefit_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benefit_id UUID NOT NULL REFERENCES benefits(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount_used DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast balance calculation
CREATE INDEX idx_usage_benefit_date ON benefit_usage(benefit_id, transaction_date);
