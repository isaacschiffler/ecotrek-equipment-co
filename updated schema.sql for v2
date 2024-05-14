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
