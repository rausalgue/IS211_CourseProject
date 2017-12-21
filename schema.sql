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
  Author TEXT,
  PageCount INTEGER,
  AverageRating INTEGER
);

CREATE TABLE clouds (
  Identifier INTEGER PRIMARY KEY,
  UserObject INTEGER,
  Name TEXT,
  FOREIGN KEY (UserObject) REFERENCES users(Identifier)
);

CREATE TABLE items (
  Identifier INTEGER PRIMARY KEY,
  UserObject INTEGER,
  CloudObject INTEGER,
  ContentObject INTEGER,
  FOREIGN KEY (UserObject) REFERENCES users(Identifier),
  FOREIGN KEY (CloudObject) REFERENCES clouds(Identifier),
  FOREIGN KEY (ContentObject) REFERENCES books(Identifier)
);