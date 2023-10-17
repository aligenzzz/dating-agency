-- script which creates empty tables

CREATE TABLE IF NOT EXISTS Users 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Username    VARCHAR (30)    NOT NULL UNIQUE,
    Email    VARCHAR (30)    UNIQUE,
    Password    VARCHAR (30)    NOT NULL UNIQUE,
    
    RoleId    INTEGER    REFERENCES Roles (Id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Roles 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Name    VARCHAR (15)    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Complaints 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Content    VARCHAR (1000)    NOT NULL,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Actions 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Name    VARCHAR (150)    NOT NULL,
    DateTime    DATETIME    NOT NULL,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Clients 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    FirstName    VARCHAR (30)    NOT NULL,
    LastName    VARCHAR (30)    NOT NULL,
    Age    TINYINT    CHECK (Age >= 14) NOT NULL,
    Photo    VARCHAR (1024),
    Banned    BOOLEAN    NOT NULL DEFAULT 0,
    
    UserId    INTEGER    REFERENCES Users (Id) ON DELETE CASCADE,
    InformationId    INTEGER    REFERENCES Informations (Id) ON DELETE SET NULL,
    LocationId    INTEGER    REFERENCES Locations (Id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Informations 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Hobbies    VARCHAR (150),
    Occupation    VARCHAR (150),
    Other    VARCHAR (500)
);

CREATE TABLE IF NOT EXISTS Chats 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Name    VARCHAR (30)    NOT NULL,
    Image    VARCHAR (1024)
);

CREATE TABLE IF NOT EXISTS Messages 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Content    VARCHAR (1000)    NOT NULL,
    DateTime    DATETIME    NOT NULL,
    Sender    VARCHAR (30)    NOT NULL,
    
    ChatId    INTEGER    REFERENCES Chats (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Locations 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Country    VARCHAR (30)    NOT NULL,
    City    VARCHAR (30),
    Address    VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS Meetings 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    Name    VARCHAR (30)    NOT NULL,
    DateTime    DATETIME    NOT NULL,
    Active    BOOLEAN    NOT NULL DEFAULT 1,
    
    LocationId    INTEGER    REFERENCES Locations (Id) ON DELETE SET NULL
);


--junction tables

CREATE TABLE IF NOT EXISTS ClientChats 
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE,
    ChatId    INTEGER    REFERENCES Chats (Id) ON DELETE CASCADE,
    
    UNIQUE (ClientId, ChatId)
);

CREATE TABLE IF NOT EXISTS ClientMeetings
(
    Id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE,
    MeetingId    INTEGER    REFERENCES Meetings (Id) ON DELETE CASCADE,
    
    UNIQUE (ClientId, MeetingId)
);