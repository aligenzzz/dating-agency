CREATE OR REPLACE PROCEDURE addRegisteredAction
(
	IN clientId	INTEGER	
)
AS
$$
DECLARE
	action_datetime TIMESTAMP := NOW();
	action_name VARCHAR := 'Has been registered';
	action_id INTEGER;
BEGIN
	INSERT INTO Actions (Name, DateTime, ClientId)
    VALUES (action_name, action_datetime, clientId)
    RETURNING Id INTO action_id;

	RAISE NOTICE 'Action added with ID: %', action_id;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE addPasswordChangedAction
(
	IN userId INTEGER	
)
AS
$$
DECLARE
	action_datetime TIMESTAMP := NOW();
	action_name VARCHAR := 'Has been changed password';
	action_id INTEGER;
	clientId INTEGER;
BEGIN
	SELECT Id INTO clientId 
	FROM Clients WHERE UserId = userId;
	
	INSERT INTO Actions (Name, DateTime, ClientId)
    VALUES (action_name, action_datetime, clientId)
    RETURNING Id INTO action_id;

	RAISE NOTICE 'Action added with ID: %', action_id;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE deleteClientComplaints
(
	IN clientId INTEGER	
)
AS
$$
BEGIN
	DELETE FROM Complaints
    WHERE ClientId = clientId;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE addMessage
(
	IN message_content VARCHAR,
	IN sender VARCHAR,
	IN chat_id INTEGER	
)
AS
$$
DECLARE
	message_datetime TIMESTAMP := NOW();
	message_id INTEGER;
BEGIN
	INSERT INTO Messages (Content, DateTime, Sender, ChatId)
    VALUES (message_content, message_datetime, sender, chat_id)
    RETURNING Id INTO message_id;

	RAISE NOTICE 'Message added with ID: %', message_id;
END;
$$
LANGUAGE plpgsql;



