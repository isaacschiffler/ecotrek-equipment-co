CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone_number INT8,
    preferred_activites TEXT
);

CREATE TABLE processed (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    job_id INT8 null,
    type text null
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INT4 REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    type TEXT UNIQUE,
    description TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku TEXT,
    name TEXT,
    description TEXT,
    category_id INT4 REFERENCES categories(id),
    sale_price INT4,
    daily_rental_price INT4
);

CREATE TABLE cart_items (
    cart_id INT4 REFERENCES carts(id),
    product_id INT4 REFERENCES products(id),
    quantity INT4,
    price INT4,
    PRIMARY KEY (cart_id, product_id)
);

CREATE TABLE stock_ledger (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_id INT4 REFERENCES products(id),
    change INT4,
    description TEXT,
    trans_id INT4 REFERENCES processed(id)
);

CREATE TABLE money_ledger (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change INT4,
    description TEXT,
    trans_id INT4 REFERENCES processed(id)
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    created_at timestamp with time zone not null default now(),
    product_id INT4 REFERENCES products(id),
    customer_id INT4 REFERENCES users(id),
    rating INT4,
    description text null
);

create table
  public.marketplace (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    product_name text null,
    quantity integer null,
    price integer null,
    condition text null,
    description text null,
    constraint marketplace_pkey primary key (id)
) tablespace pg_default;

create table
  public.reviews (
    id serial,
    created_at timestamp with time zone not null default now(),
    product_id integer null,
    customer_id integer null,
    rating integer null,
    description text null,
    constraint reviews_pkey primary key (id),
    constraint reviews_customer_id_fkey foreign key (customer_id) references users (id),
    constraint reviews_product_id_fkey foreign key (product_id) references products (id)
) tablespace pg_default;


-- Insert initial seed data
INSERT INTO money_ledger (change, description) 
VALUES (100000, 'start with $100000 to spend');

INSERT INTO categories(type, description)
VALUES ('SHELTER', Null), 
       ('SLEEPING', Null), 
       ('BACKPACKING', Null), 
       ('COOKING', Null);

INSERT INTO products (sku, name, description, category_id, sale_price, daily_rental_price)
VALUES 
    ('RED_JANSPORT_BCKPK', 'Red Jansport Backpack', 'Primarily for everyday use', 
    (SELECT id FROM categories WHERE type='BACKPACKING'), 70, 5),
    ('BLU_CAMP_TENT', 'Blue Camping Tent', 'Spacious tent for camping', 
    (SELECT id FROM categories WHERE type='SHELTER'), 150, 15),
    ('GRN_CAMP_STOVE', 'Green Camping Stove', 'Portable stove for outdoor cooking', 
    (SELECT id FROM categories WHERE type='COOKING'), 80, 8),
    ('CAMP_UTENSILS_SET', 'Camping Utensils Set', 'Set of essential utensils for camping', 
    (SELECT id FROM categories WHERE type='COOKING'), 30, 3),
    ('LED_FLASHLIGHT', 'LED Flashlight', 'High-lumen LED flashlight for camping', 
    (SELECT id FROM categories WHERE type='SLEEPING'), 25, 2),
    ('CAMP_SLEEPING_BAG', 'Camping Sleeping Bag', 'Warm and comfortable sleeping bag', 
    (SELECT id FROM categories WHERE type='SLEEPING'), 60, 6),
    ('PORTABLE_STOVE', 'Portable Stove', 'Compact and efficient portable stove', 
    (SELECT id FROM categories WHERE type='COOKING'), 90, 9),
    ('CAMPING_CHAIR', 'Camping Chair', 'Comfortable and foldable camping chair', 
    (SELECT id FROM categories WHERE type='SHELTER'), 40, 4);

INSERT INTO processed(job_id, type)
VALUES (1, 'stock_delivery'),
       (2, 'stock_delivery'),
       (3, 'stock_delivery'),
       (4, 'stock_delivery'),
       (5, 'stock_delivery'),
       (6, 'stock_delivery'),
       (7, 'stock_delivery'),
       (8, 'stock_delivery'),
       (9, 'stock_delivery');

INSERT INTO stock_ledger(product_id, change, description, trans_id)
VALUES 
    ((SELECT id FROM products WHERE sku='RED_JANSPORT_BCKPK'), 5, 
    'Delivered 5 units of RED_JANSPORT_BCKPK', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='BLU_CAMP_TENT'), 10, 
    'Delivered 10 units of BLU_CAMP_TENT', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='GRN_CAMP_STOVE'), 7, 
    'Delivered 7 units of GRN_CAMP_STOVE', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='CAMP_UTENSILS_SET'), 15, 
    'Delivered 15 units of CAMP_UTENSILS_SET', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='LED_FLASHLIGHT'), 20, 
    'Delivered 20 units of LED_FLASHLIGHT', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='CAMP_SLEEPING_BAG'), 12, 
    'Delivered 12 units of CAMP_SLEEPING_BAG', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='PORTABLE_STOVE'), 8, 
    'Delivered 8 units of PORTABLE_STOVE', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
    ((SELECT id FROM products WHERE sku='CAMPING_CHAIR'), 10, 
    'Delivered 10 units of CAMPING_CHAIR', 
    (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery'));
