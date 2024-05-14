CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone_number INT8,
    preferred_activites TEXT
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INT4 REFERENCES user(id),
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
    category_id INT4 REFERENCES categories(id)
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

CREATE TABLE processed (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    job_id INT8 null,
    type text null
);

CREATE TABLE USERS (
    id serial,
    name text null,
    email text null,
    phone_number bigint null,
    preferred_activities text null,
    constraint customers_pkey primary key (id)
  );

INSERT INTO money_ledger (change, description) 
VALUES (1000, 'start with $1000 to spend');

INSERT INTO products (sku, name, description, category_id, sale_price, daily_rental_price)
VALUES ('RED_JANSPORT_BCKPK', 'Red Jansport Backpack', 'Primarily for everyday use', 2, 70, 5);

INSERT INTO stock_ledger(product_id, change, description, trans_id)
VALUES (1, 5, 'Delivered 5 units of RED_JANSPORT_BCKPK', 1);

INSERT INTO processed(job_id, type)
VALUES (1, 'stock_delivery')

INSERT INTO categories(type, description)
VALUES ('SHELTER', Null);

INSERT INTO categories(type, description)
VALUES ('SLEEPING', Null);

INSERT INTO categories(type, description)
VALUES ('BACKPACKING', Null);

INSERT INTO categories(type, description)
VALUES ('COOKING', Null);
