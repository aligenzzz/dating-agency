CREATE VIEW IF NOT EXISTS ClientDetails AS
SELECT 
    FirstName, LastName, Age,
    Users.Username, Users.Email,
    Informations.Hobbies, Informations.Occupation, Informations.Other,
    Locations.Country, Locations.City
FROM Clients 
JOIN Users ON UserId = Users.Id
JOIN Informations ON InformationId = Informations.Id
JOIN Locations ON LocationId = Locations.Id;

SELECT *
FROM ClientDetails;
