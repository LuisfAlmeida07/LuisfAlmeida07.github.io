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

ALTER TABLE publisher 
MODIFY publisher_name VARCHAR(255) NULL;

INSERT INTO publisher (publisher_id)
VALUES
(0),
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15),
(16),
(17),
(18),
(19),
(20),
(21),
(22),
(23),
(24),
(25);

INSERT INTO Book (title, isbn, publication_date, price, publisher_id)
VALUES
('Ilíada', '978-8563560568', '2013-02-06', '49.08', 1),
('Odisseia', '978-8563560278', '2011-10-10', '42.89', 2),
('Orestéia', '978-9724413976', '2008-08-08', '89.10', 3),
('Édipo Rei', '978-8537817360', '2018-04-12', '33.72', 4),
('A República', '978-8581862538', '2017-01-01', '56.30', 5),
('A Bíblia', 'B084W44SRZ', '2020-01-01', '94.82', 6),
('A Eneida', '978-8551307915', '2022-07-20', '78.67', 7),
('Confissões', '978-8582850473', '2017-04-12', '36.79', 8),
('A Divina Comédia', '978-6559100156', '2021-02-24', '87.37', 9),
('O Decamerão', 'B07GL321VT', '2018-08-10', '121.47', 10),
('Os Contos de Canterbury', '978-8573265620', '2014-01-01', '102.07', 11),
('Ensaios', '978-8573266504', '2016-01-01', '119.87', 12),
('Dom Quixote', '978-8563560551', '2012-12-05', '78.99', 13),
('Hamlet', '978-6560950207', '2024-06-22', '27.99', 14),
('Rei Lear', '978-8582851111', '2020-08-24', '36.79', 15),
('A Tempestade', '978-8582852453', '2022-04-13', '33.72', 16),
('O Leviatã', '978-1840227338', '2014-07-07', '106.68', 17),
('Paraíso Perdido', '978-8573266115', '2016-01-01', '112.61', 18),
('Fausto', '978-8573262919', '2016-01-01', '78.99', 19),
('Orgulho e Preconceito', '978-6587817149', '2021-09-16', '18.15', 20),
('Frankenstein', '978-8537818589', '2020-01-16', '36.77', 21),
('Moby-Dick', '978-8573267389', '2019-07-26', '99.90', 22),
('Madame Bovary', '978-8544000717', '2009-02-10', '53.13', 23),
('Guerra e Paz', '978-8535930047', '2017-11-21', '188.90', 24),
('Os Irmãos Karamazov', '978-8573265385', '2019-02-27', '96.13', 25);






