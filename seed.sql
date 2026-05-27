-- Seed Data for CC Benefit Tracker

-- 1. Cards
INSERT INTO cards (id, name, issuer) VALUES 
(gen_random_uuid(), 'Amex Gold', 'American Express'),
(gen_random_uuid(), 'Amex Platinum', 'American Express'),
(gen_random_uuid(), 'Chase Sapphire Reserve', 'Chase'),
(gen_random_uuid(), 'Capital One Venture X', 'Capital One');

-- 2. Benefits
-- Amex Gold
INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Dining Credit', 10.00, 'Dining', 'monthly', '$10 monthly dining credit'
FROM cards WHERE name = 'Amex Gold';

INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Uber Cash', 10.00, 'Dining/Travel', 'monthly', '$10 monthly Uber Cash'
FROM cards WHERE name = 'Amex Gold';

-- Amex Platinum
INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Uber Cash', 15.00, 'Dining/Travel', 'monthly', '$15 monthly Uber Cash ($35 in Dec)'
FROM cards WHERE name = 'Amex Platinum';

INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Digital Entertainment', 20.00, 'Entertainment', 'monthly', '$20 monthly digital entertainment credit'
FROM cards WHERE name = 'Amex Platinum';

INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Walmart+', 12.95, 'Shopping', 'monthly', 'Walmart+ membership credit'
FROM cards WHERE name = 'Amex Platinum';

INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Airline Fee Credit', 200.00, 'Travel', 'yearly', '$200 annual airline fee credit'
FROM cards WHERE name = 'Amex Platinum';

-- Chase Sapphire Reserve
INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Travel Credit', 300.00, 'Travel', 'yearly', '$300 annual travel credit'
FROM cards WHERE name = 'Chase Sapphire Reserve';

-- Capital One Venture X
INSERT INTO benefits (card_id, name, amount, category, frequency, description)
SELECT id, 'Travel Credit', 300.00, 'Travel', 'yearly', '$300 annual travel credit'
FROM cards WHERE name = 'Capital One Venture X';
