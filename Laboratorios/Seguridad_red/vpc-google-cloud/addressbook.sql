USE mydb;
CREATE TABLE address (id INT(4) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(30), phone VARCHAR(30), email VARCHAR(30));
INSERT INTO address (name, phone, email) VALUES ( "Bob", "630-555-1254", "bob@fakeaddress.com"), ( "Alice", "571-555-4875", "alice@address2.us" );