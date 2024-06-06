-- Creating table for customers and transactions 
-- Products and Stores table will be created in the function app
CREATE TABLE customers (
    customer_id VARCHAR(10),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    dob DATE,
    address VARCHAR(255),
    city VARCHAR(50),
    region VARCHAR(50),
    PRIMARY KEY (customer_id)
);

CREATE TABLE Transactions (
    order_id VARCHAR(10) PRIMARY KEY,
    transaction_id VARCHAR(10) NOT NULL,
    customer_id VARCHAR(10) NOT NULL,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date DATE NOT NULL,
    payment_method VARCHAR(20) NOT NULL
);

--Drop already existed product data before sinking transformed product data as PRE sql script
DROP TABLE products

--Drop already existed store data before sinking transformed store data as PRE sql script
DROP TABLE products



