-- PostgreSQL Schema for CC Benefit Tracker

-- Extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enums
CREATE TYPE benefit_frequency AS ENUM ('monthly', 'quarterly', 'semiannually', 'yearly');

-- Tables

-- 1. cards
CREATE TABLE cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    issuer VARCHAR(255) NOT NULL,
    image_url TEXT
);

-- 2. user_cards
CREATE TABLE user_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    card_id UUID NOT NULL REFERENCES cards(id) ON DELETE CASCADE
);

-- 3. benefits
CREATE TABLE benefits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    card_id UUID NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    frequency benefit_frequency NOT NULL,
    description TEXT
);

-- 4. claims
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benefit_id UUID NOT NULL REFERENCES benefits(id) ON DELETE CASCADE,
    window_id VARCHAR(50) NOT NULL,
    claimed_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (benefit_id, window_id)
);

-- Indices
CREATE INDEX idx_benefits_card_id ON benefits(card_id);
CREATE INDEX idx_user_cards_card_id ON user_cards(card_id);
CREATE INDEX idx_claims_benefit_window ON claims(benefit_id, window_id);
