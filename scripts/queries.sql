-- simple and complex queries

--lab3--

-- get all users
SELECT
    Username, Password, Email,
    Roles.Name
FROM Users
JOIN Roles ON RoleId = Roles.Id;

-- get counters of all roles
SELECT 
    Roles.Name AS Role,
    COUNT (*) AS Count
FROM Users
JOIN Roles ON RoleId = Roles.Id
GROUP BY Roles.Name;

-- get all moderators
SELECT Username
FROM Users
JOIN Roles ON RoleId = Roles.Id 
AND Roles.Name = "Moderator";

-- get all admins
SELECT Username
FROM Users
JOIN Roles ON RoleId = Roles.Id 
AND Roles.Name = "Admin";

-- get all clients
SELECT Username
FROM Users
JOIN Roles ON RoleId = Roles.Id 
AND Roles.Name = "Client";

-- get all information about clients
SELECT 
    FirstName, LastName, Age,
    Users.Username, Users.Email,
    Informations.Hobbies, Informations.Occupation, Informations.Other,
    Locations.Country, Locations.City
FROM Clients 
JOIN Users ON UserId = Users.Id
JOIN Informations ON InformationId = Informations.Id
JOIN Locations ON LocationId = Locations.Id;

-- get all messages of all chats
SELECT
    Chats.Name,
    Content, DateTime, Sender
FROM Messages 
JOIN Chats ON ChatId = Chats.Id
ORDER BY DateTime DESC;

-- get all messages of the specific chat
SELECT
    Chats.Name,
    Content, DateTime, Sender
FROM Messages 
JOIN Chats ON ChatId = Chats.Id 
AND Chats.Id = 1
ORDER BY DateTime DESC;

-- get chats of the specific client
SELECT Chats.*
FROM ClientChats
JOIN Chats ON ChatId = Chats.Id
WHERE ClientId = 1;

-- get clients of the specific chats
SELECT Clients.*
FROM ClientChats
JOIN Clients ON ClientId = Clients.Id
WHERE ChatId = 1;

-- get meetings of the specific client
SELECT Meetings.*
FROM ClientMeetings
JOIN Meetings ON MeetingId = Meetings.Id
WHERE ClientId = 1;    

-- get clients of the specific meeting
SELECT Clients.*
FROM ClientMeetings
JOIN Clients ON ClientId = Clients.Id
WHERE MeetingId = 1;

-- get all active meetings
SELECT 
    Name, DateTime,
    Locations.Country, Locations.City, Locations.Address
FROM Meetings
JOIN Locations ON LocationId = Locations.Id
WHERE Active = 1; 

-- get all complaints
SELECT 
    Content,
    Users.Username
FROM Complaints
JOIN Clients ON ClientId = Clients.Id
JOIN Users ON Clients.UserId = Users.Id;

-- get all actions
SELECT
    Name, DateTime,
    Users.Username
FROM Actions
JOIN Clients ON ClientId = Clients.Id
JOIN Users ON Clients.UserId = Users.Id
ORDER BY DateTime DESC;

--lab4--

-- get user by firstName and lastName
SELECT Clients.*
FROM Clients
WHERE FirstName = "Elena" AND LastName = "Mason";

-- get user-client with his full name
SELECT Username, Password, Email, 
    (SELECT FirstName || ' ' || LastName 
     FROM Clients
     WHERE UserId = Users.Id) AS FullName
FROM Users
WHERE RoleId = 1;

-- get chat with the last message
SELECT Id, Name, Image,
    (SELECT Content
     FROM Messages
     GROUP BY ChatId
     HAVING DateTime = MAX(DateTime)) AS LastMessage
FROM Chats;

-- get partitions of clients' actions with row numbers
SELECT 
    Id, Name, DateTime,
    ROW_NUMBER() OVER (PARTITION BY ClientId ORDER BY DateTime DESC) 
                    AS Number,
    Users.Username
FROM Actions
JOIN Clients ON ClientId = Clients.Id
JOIN Users ON Clients.UserId = Users.Id;

-- select clients if user with role client exist
SELECT * 
FROM Clients
WHERE EXISTS 
    (SELECT * 
     FROM Users 
     WHERE RoleId = 1);
     
-- get clients with some classification
SELECT Id, FirstName, LastName, Age,
    CASE
        WHEN Age < 20 THEN 'Teenager'
        WHEN Age < 40 THEN 'Young adult'
        WHEN Age < 60 THEN 'Middle aged adult'
        ELSE 'Retired'
    END AS AgeType,
    IIF(Photo IS NULL, 'No photo', Photo) 
        AS Photo
FROM Clients;
