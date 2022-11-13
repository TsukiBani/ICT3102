create database 02db;
use 02db;

CREATE TABLE test_table (
  name VARCHAR(20),
  color VARCHAR(10)
);

INSERT INTO test_table
  (name, color)
VALUES
  ('dev', 'blue'),
  ('pro', 'yellow');