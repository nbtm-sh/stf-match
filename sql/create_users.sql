CREATE USER 'stf'@'localhost' IDENTIFIED BY 'xdcstfdefault1!';
GRANT INSERT, SELECT, UPDATE, DELETE ON stf.* TO 'stf'@'localhost';
