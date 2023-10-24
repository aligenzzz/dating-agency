-- script which fills tables with data

INSERT INTO Users (Username, Password, RoleId) VALUES
("client1", "client", 1),
("client2", "client", 1),
("moderator", "moderator", 2),
("admin", "admin", 3);

INSERT INTO Roles (Name) VALUES
("Client"),
("Moderator"),
("Admin");

INSERT INTO Complaints (Content, ClientId) VALUES
("I dont like interface!", 1);

INSERT INTO Actions (Name, DateTime, ClientId) VALUES
("Has been registered", datetime('now'), 1),
("Has been registered", datetime('now'), 2);
INSERT INTO Actions (Name, DateTime, ClientId) VALUES
("Has been changed password", datetime('now'), 1);

INSERT INTO Clients (FirstName, LastName, Age, UserId, InformationId, LocationId) VALUES
("Michael", "Smith", 23, 1, 1, 1),
("Elena", "Mason", 22, 2, 2, 2); 

INSERT INTO Informations (Occupation) VALUES
("Manager"),
("Programmer");

INSERT INTO Chats (Name) VALUES
("Simple conversation...");

INSERT INTO Messages (Content, DateTime, Sender, ChatId) VALUES
("Hi!!", datetime('now'), "client1", 1),
("hello, whats up??", datetime('now'), "client2", 1);

INSERT INTO Locations (Country, City, Address) VALUES
("USA", "LA", NULL),
("Canada", "Montreal", NULL),
("USA", "Hawaii", "91-1001 Farrington Hwy Kapolei");

INSERT INTO Meetings (Name, DateTime, LocationId) VALUES
("Simple meeting...", '2024-03-12', 3);

INSERT INTO ClientChats (ClientId, ChatId) VALUES
(1, 1),
(2, 1);

INSERT INTO ClientMeetings (ClientId, MeetingId) VALUES
(1, 1),
(2, 1);
