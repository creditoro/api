DROP INDEX email_idx;
DROP INDEX name_idx;
DROP TABLE users CASCADE;
DROP DOMAIN IF EXISTS email;
DROP EXTENSION IF EXISTS citext RESTRICT;