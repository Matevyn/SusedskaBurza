-- 1. Vytvorenie databázy SusedskaBurza
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SusedskaBurza')
BEGIN
    CREATE DATABASE SusedskaBurza;
END
GO

USE SusedskaBurza;
GO

-- 2. Tabuľka Používateľov (Users)
CREATE TABLE Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(150) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Phone NVARCHAR(20) NULL,
    City NVARCHAR(100) NOT NULL,
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- 3. Tabuľka Kategórií (Categories)
CREATE TABLE Categories (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL UNIQUE
);

-- 4. Tabuľka Inzerátov (Posts)
CREATE TABLE Posts (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    CategoryId INT NOT NULL,
    Type NVARCHAR(20) NOT NULL CHECK (Type IN ('dopyt', 'ponuka')),
    Title NVARCHAR(150) NOT NULL,
    Description NVARCHAR(MAX) NOT NULL,
    City NVARCHAR(100) NOT NULL,
    Status NVARCHAR(20) DEFAULT 'active' CHECK (Status IN ('active', 'completed')),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    
    -- Cudzie kľúče (Relácie medzi tabuľkami)
    CONSTRAINT FK_Posts_Users FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Posts_Categories FOREIGN KEY (CategoryId) REFERENCES Categories(Id) ON DELETE CASCADE
);
GO

-- 5. Vloženie základných kategórií
INSERT INTO Categories (Name) VALUES
(N'Drevo a palivo'),
(N'Záhrada a dvor'),
(N'Preprava a sťahovanie'),
(N'Stavba a opravy'),
(N'Domácnosť a upratovanie'),
(N'Iné');

-- 6. Vloženie vzorového používateľa a inzerátu pre testovanie
INSERT INTO Users (FullName, Email, PasswordHash, Phone, City) VALUES
(N'Ján Novák', N'jan.novak@example.com', N'$2b$10$hashedpasswordexample', N'+421901123456', N'Banská Bystrica');

INSERT INTO Posts (UserId, CategoryId, Type, Title, Description, City) VALUES
(1, 1, N'dopyt', N'Pomoc s ukladaním palivového dreva', N'Hľadám niekoho na 2 hodiny na uloženie 5 m³ dreva pod prístrešok.', N'Banská Bystrica');
GO
