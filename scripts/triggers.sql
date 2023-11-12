CREATE OR REPLACE FUNCTION addClientTrigger()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.RoleId = 1 THEN
        CALL addRegisteredAction(NEW.Id);
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- add action when client was registered
CREATE OR REPLACE TRIGGER addClient
    AFTER INSERT ON Clients
    FOR EACH ROW
	EXECUTE FUNCTION addClientTrigger();


CREATE OR REPLACE FUNCTION updateClientPasswordTrigger()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.Password <> OLD.Password AND
	   NEW.RoleId = 1 THEN
       CALL addPasswordChangedAction(NEW.Id);
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- add action when password was changes
CREATE OR REPLACE TRIGGER updateClientPassword
	AFTER UPDATE ON Users
	FOR EACH ROW
	EXECUTE FUNCTION updateClientPasswordTrigger();
	

CREATE OR REPLACE FUNCTION deleteBannedClientComplaintsTrigger()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.Banned = TRUE THEN
       CALL deleteClientComplaints(NEW.Id);
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- delete all client's complaints if he was banned
CREATE OR REPLACE TRIGGER deleteBannedClientComplaints
	AFTER UPDATE ON Clients
	FOR EACH ROW
	EXECUTE FUNCTION deleteBannedClientComplaintsTrigger();
