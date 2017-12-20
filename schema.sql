DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS clouds;

CREATE TABLE users (
  Identifier INTEGER PRIMARY KEY,
  FirstName TEXT,
  LastName TEXT,
  UserId TEXT,
  UserPassword TEXT
);

CREATE TABLE books (
  Identifier INTEGER PRIMARY KEY,
  Title TEXT,
  Author TEXT
);

CREATE TABLE clouds (
  Identifier INTEGER PRIMARY KEY,
  UserObject INTEGER,
  Book INTEGER,
  Name TEXT,
  FOREIGN KEY (UserObject) REFERENCES users(Identifier),
  FOREIGN KEY (Book) REFERENCES books(Identifier)
);