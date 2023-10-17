-- simple queries

-- get all users
SELECT
    Username, Password, Email,
    Roles.Name
FROM Users
JOIN Roles ON RoleId = Roles.Id;

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
