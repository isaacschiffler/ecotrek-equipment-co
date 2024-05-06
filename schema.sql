CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    customer_id INT4 REFERENCES customers(id)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku TEXT,
    name TEXT,
    description TEXT,
    price INT4,
    quantity INT4
);

CREATE TABLE cart_items (
    cart_id INT4 REFERENCES carts(id),
    potion_id INT4 REFERENCES products(id),
    quantity INT4,
    price INT4,
    PRIMARY KEY (cart_id, potion_id)
);

CREATE TABLE stock_ledger (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_id INT4 REFERENCES products(id),
    change INT4,
    description TEXT
);
    
