CREATE TABLE Produit (
    id_produit INT not null IDENTITY(1,1) PRIMARY KEY,
    Nom VARCHAR(50),
    Description VARCHAR(200),
    PrixUnitaire DECIMAL(10, 2),
);

CREATE TABLE magasin (
    id_magasin INT not null IDENTITY(1,1) PRIMARY KEY,
    Nom VARCHAR(50),
    adresse VARCHAR(200),
    Telephone INT,
    mail DECIMAL(10, 2),
);

CREATE TABLE vente (
    Codevente INT not null IDENTITY(1,1) PRIMARY KEY,
);

CREATE TABLE stock (
    Codestock INT not null IDENTITY(1,1) PRIMARY KEY,
    id_produit INT,
    id_magasin INT,
    StockActuel INT,
    FOREIGN KEY (id_produit) REFERENCES Produit(id_produit),
    FOREIGN KEY (id_magasin) REFERENCES magasin(id_magasin)
);