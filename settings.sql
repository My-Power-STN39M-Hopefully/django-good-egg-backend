-- settings.sql
CREATE DATABASE good_egg;
CREATE USER good_egg_super_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE good_egg TO good_egg_super_user;