CREATE OR REPLACE FUNCTION getClientByUserId
(
    IN user_id INTEGER
)
RETURNS SETOF Clients
AS
$$
DECLARE
    clientInfo Clients%ROWTYPE; 
BEGIN
    SELECT * INTO clientInfo
    FROM Clients
    WHERE Clients.UserId = user_id;

    RETURN NEXT clientInfo;
END;
$$
LANGUAGE plpgsql;

SELECT * FROM getClientByUserId(1);