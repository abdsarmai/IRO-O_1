-- Commande pour créer la base de données 
CREATE DATABASE RESEAU_IRO_O;
-- Commande pour créer l'utilisateur adminJonathan avec le mot de passe azerty
CREATE USER 'adminAbdallah'@'192.168.1.64' IDENTIFIED BY 'azerty';
-- Commande pour donner tous les droits au compte adminJonathan
GRANT ALL PRIVILEGES ON RESEAU_IRO_O.* TO 'adminAbdallah'@'192.168.1.64';
FLUSH PRIVILEGES;
-- Commande pour se placer dans la base de données RESEAU_IRO_O
USE RESEAU_IRO_O;
-- Commande pour créer une table nommé "element" avec 4 colonnes pour stocker toutes les adresses ip trouvés dans le réseau.
CREATE TABLE element (
    id INTEGER AUTO_INCREMENT NOT NULL,
    nom VARCHAR(30) DEFAULT '',
    ip VARCHAR(15) NOT NULL,
    mac CHAR(17) NOT NULL,
    PRIMARY KEY(id)
);



