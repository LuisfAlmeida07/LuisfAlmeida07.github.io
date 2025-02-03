SHOW DATABASES;
USE bookstore;


CREATE TABLE Publisher (
publisher_id INT AUTO_INCREMENT PRIMARY KEY,
publisher_name VARCHAR(255) NOT NULL,
address VARCHAR(255)
);


CREATE TABLE Author (
author_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
bio TEXT
);

CREATE TABLE Book (
book_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
title VARCHAR(255) NOT NULL,
isbn VARCHAR(20) NOT NULL UNIQUE,
publication_date DATE NOT NULL,
price DECIMAL(10, 2),
publisher_id INT,
FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id)
);


CREATE TABLE BookAuthor (
book_id INT,
author_id INT,
PRIMARY KEY (book_id, author_id),
FOREIGN KEY (book_id) REFERENCES Book(book_id),
FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE Genre (
genre_id INT AUTO_INCREMENT PRIMARY KEY,
genre_name VARCHAR(100) NOT NULL
);



CREATE TABLE BookGenre(
book_id INT,
genre_id INT,
PRIMARY KEY (book_id, genre_id),
FOREIGN KEY (book_id) REFERENCES Book(book_id),
FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);


CREATE TABLE Customer (
customer_id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
email VARCHAR(255) NOT NULL,
address VARCHAR(255)
);

CREATE TABLE ClientOrder (
order_id INT AUTO_INCREMENT PRIMARY KEY,
order_date DATE NOT NULL, 
customer_id INT,
FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);


CREATE TABLE OrderItem (
order_id INT, 
book_id INT,
quantity INT NOT NULL,
price_at_purchase DECIMAL(10,2),
PRIMARY KEY (order_id, book_id),
FOREIGN KEY (order_id) REFERENCES ClientOrder(order_id),
FOREIGN KEY (book_id) REFERENCES Book(book_Id)
);






