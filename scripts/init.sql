-- script which fills tables with data

INSERT INTO Roles (Id, Name) VALUES
(1, 'Client'),
(2, 'Moderator'),
(3, 'Admin');

INSERT INTO Users (Id, Username, Password, RoleId) VALUES
(1, 'client1', 'client', 1),
(2, 'client2', 'client', 1),
(3, 'moderator', 'moderator', 2),
(4, 'admin', 'admin', 3);

INSERT INTO Informations (Id, Occupation) VALUES
(1, 'Manager'),
(2, 'Programmer');

INSERT INTO Locations (Id, Country, City, Address) VALUES
(1, 'USA', 'LA', NULL),
(2, 'Canada', 'Montreal', NULL),
(3, 'USA', 'Hawaii', '91-1001 Farrington Hwy Kapolei');

INSERT INTO Clients (Id, FirstName, LastName, Age, UserId, InformationId, LocationId) VALUES
(1, 'Michael', 'Smith', 23, 1, 1, 1),
(2, 'Elena', 'Mason', 22, 2, 2, 2); 

INSERT INTO Complaints (Id, Content, ClientId) VALUES
(1, 'I dont like interface!', 1);

INSERT INTO Actions (Id, Name, DateTime, ClientId) VALUES
(1, 'Has been registered', NOW(), 1),
(2, 'Has been changed password', NOW(), 1),
(3, 'Has been registered', NOW(), 2);

INSERT INTO Chats (Id, Name) VALUES
(1, 'Simple conversation...');

INSERT INTO Messages (Id, Content, DateTime, Sender, ChatId) VALUES
(1, 'Hi!!', NOW(), 'client1', 1),
(2, 'hello, whats up??', NOW() + INTERVAL '1 second', 'client2', 1);

INSERT INTO Meetings (Id, Name, DateTime, LocationId) VALUES
(1, 'Simple meeting...', '2024-03-12', 3);

INSERT INTO ClientChats (Id, ClientId, ChatId) VALUES
(1, 1, 1),
(2, 2, 1);

INSERT INTO ClientMeetings (Id, ClientId, MeetingId) VALUES
(1, 1, 1),
(2, 2, 1);
