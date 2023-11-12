-- script which creates empty tables

CREATE TABLE IF NOT EXISTS Roles 
(
    Id    SERIAL   PRIMARY KEY,
    
    Name    VARCHAR(15)    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Users 
(
    Id    SERIAL    PRIMARY KEY,
    
    Username    VARCHAR (30)    NOT NULL UNIQUE,
    Email    VARCHAR (30),
    Password    VARCHAR (30)    NOT NULL,
    
    RoleId    INTEGER    REFERENCES Roles (Id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Informations 
(
    Id    SERIAL    PRIMARY KEY,
    
    Hobbies    VARCHAR (150),
    Occupation    VARCHAR (150),
    Other    VARCHAR (500)
);

CREATE TABLE IF NOT EXISTS Locations 
(
    Id    SERIAL    PRIMARY KEY,
    
    Country    VARCHAR (30)    NOT NULL,
    City    VARCHAR (30),
    Address    VARCHAR (50)
);

CREATE TABLE IF NOT EXISTS Clients 
(
    Id    SERIAL    PRIMARY KEY,
    
    FirstName    VARCHAR (30)    NOT NULL,
    LastName    VARCHAR (30)    NOT NULL,
    Age    SMALLINT    CHECK (Age >= 14) NOT NULL,
    Photo    VARCHAR (1024),
    Banned    BOOLEAN    NOT NULL DEFAULT FALSE,
    
    UserId    INTEGER    REFERENCES Users (Id) ON DELETE CASCADE,
    InformationId    INTEGER    REFERENCES Informations (Id) ON DELETE SET NULL,
    LocationId    INTEGER    REFERENCES Locations (Id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Complaints 
(
    Id    SERIAL    PRIMARY KEY,
    
    Content    VARCHAR (1000)    NOT NULL,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Actions 
(
    Id    SERIAL    PRIMARY KEY,
    
    Name    VARCHAR (150)    NOT NULL,
    DateTime    TIMESTAMP    NOT NULL,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Chats 
(
    Id    SERIAL    PRIMARY KEY,
    
    Name    VARCHAR (30)    NOT NULL,
    Image    VARCHAR (1024)
);

CREATE TABLE IF NOT EXISTS Messages 
(
    Id    SERIAL    PRIMARY KEY,
    
    Content    VARCHAR (1000)    NOT NULL,
    DateTime    TIMESTAMP    NOT NULL,
    Sender    VARCHAR (30)    NOT NULL,
    
    ChatId    INTEGER    REFERENCES Chats (Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Meetings 
(
    Id    SERIAL    PRIMARY KEY,
    
    Name    VARCHAR (30)    NOT NULL,
    DateTime    TIMESTAMP    NOT NULL,
    Active    BOOLEAN    NOT NULL DEFAULT TRUE,
    
    LocationId    INTEGER    REFERENCES Locations (Id) ON DELETE SET NULL
);


--junction tables

CREATE TABLE IF NOT EXISTS ClientChats 
(
    Id    SERIAL    PRIMARY KEY,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE,
    ChatId    INTEGER    REFERENCES Chats (Id) ON DELETE CASCADE,
    
    UNIQUE (ClientId, ChatId)
);

CREATE TABLE IF NOT EXISTS ClientMeetings
(
    Id    SERIAL    PRIMARY KEY,
    
    ClientId    INTEGER    REFERENCES Clients (Id) ON DELETE CASCADE,
    MeetingId    INTEGER    REFERENCES Meetings (Id) ON DELETE CASCADE,
    
    UNIQUE (ClientId, MeetingId)
);