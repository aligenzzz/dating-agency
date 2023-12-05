import psycopg2 as pg
from models import User, Client, Chat


class Database:
    connection = None

    @staticmethod
    def connect():
        try:
            Database.connection = pg.connect(
                host='localhost',
                database='myDb',
                port=2222,
                user='postgres',
                password='alina'
            )     
        except Exception as e:
            print("Something went wrong.")
            print(e)


    @staticmethod
    def disconnect():
        Database.connection.close()
    

    @staticmethod
    def get_user(username: str, password: str):
        query = "SELECT " \
                "Users.Id, Username, Password, Email, Roles.Name " \
                "FROM Users JOIN Roles ON RoleId = Roles.Id " \
                f"WHERE Username = '{username}' AND Password = '{password}';"
        
        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        
        if result is None:
            return None
        
        user = User(*result)

        return user
    

    @staticmethod
    def get_clients():
        query = "SELECT * FROM ClientDetails;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result


    @staticmethod
    def get_client_profile(username: str):
        query = f"SELECT * FROM ClientDetails WHERE Username = '{username}';"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_client_chats(username: str):
        client = Database.get_client(username)

        if client is None:
            return None
        
        query = "SELECT Chats.Id, Chats.Name, " \
	            "(SELECT Users.Username FROM ClientChats " \
	            "JOIN Clients ON ClientId = Clients.Id " \
	            "JOIN Users ON Clients.UserId = Users.Id " \
	            f"WHERE ChatId = Chats.Id AND ClientId != {client.id}) AS Partner " \
                f"FROM ClientChats JOIN Chats ON ChatId = Chats.Id WHERE ClientId = {client.id};"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_client_meetings(username: str):
        client = Database.get_client(username)

        if client is None:
            return None
        
        query = "SELECT Meetings.Name, Meetings.Datetime, " \
                "Locations.Country, Locations.City, Locations.Address, " \
	            "(SELECT Users.Username FROM ClientMeetings " \
	            "JOIN Clients ON ClientId = Clients.Id " \
	            "JOIN Users ON Clients.UserId = Users.Id " \
	            f"WHERE MeetingId = Meetings.Id AND ClientId != {client.id}) AS Partner " \
                "FROM ClientMeetings JOIN Meetings ON MeetingId = Meetings.Id " \
                f"JOIN Locations ON Meetings.LocationId = Locations.Id WHERE ClientId = {client.id};"

        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        return result
    

    @staticmethod
    def get_clients_with_banned():
        query = "SELECT " \
                "FirstName, LastName, Age, Banned, " \
                "Users.Username, Users.Email, " \
                "Informations.Hobbies, Informations.Occupation, Informations.Other, " \
                "Locations.Country, Locations.City " \
                "FROM Clients JOIN Users ON UserId = Users.Id " \
                "JOIN Informations ON InformationId = Informations.Id " \
                "JOIN Locations ON LocationId = Locations.Id;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    
    
    @staticmethod
    def get_actions():
        query = "SELECT " \
                "Name, DateTime, Users.Username " \
                "FROM Actions " \
                "JOIN Clients ON ClientId = Clients.Id " \
                "JOIN Users ON Clients.UserId = Users.Id " \
                "ORDER BY DateTime DESC;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_client_actions(username: str):
        if Database.get_client(username) is None:
            return None

        query = "SELECT " \
                "Name, DateTime FROM Actions " \
                "JOIN Clients ON ClientId = Clients.Id " \
                "JOIN Users ON Clients.UserId = Users.Id " \
                f"WHERE Users.Username = '{username}' " \
                "ORDER BY DateTime DESC;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_client(username: str):
        query = "SELECT * FROM Users " \
                f"WHERE Users.Username = '{username}'" \
                f"AND Users.RoleId = 1;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return None

        query = "SELECT * FROM Clients " \
                 f"WHERE UserId = {result[0]};"
        
        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return None

        client = Client(*result)
        
        return client
    

    @staticmethod
    def ban_unban_client(username: str):
        client = Database.get_client(username)

        if client is None:
            return None

        query = f"UPDATE Clients SET Banned = {str(not client.banned)} WHERE Id = {client.id}"
    
        cursor = Database.connection.cursor()
        cursor.execute(query)
        Database.connection.commit()
        cursor.close()

        return not client.banned
    

    @staticmethod
    def get_complaints():
        query = "SELECT " \
                "Complaints.Id, Content, Users.Username " \
                "FROM Complaints " \
                "JOIN Clients ON ClientId = Clients.Id " \
                "JOIN Users ON Clients.UserId = Users.Id;"

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_client_complaints(username: str):
        if Database.get_client(username) is None:
            return None

        query = "SELECT " \
                "Complaints.Id, Content " \
                "FROM Complaints " \
                "JOIN Clients ON ClientId = Clients.Id " \
                "JOIN Users ON Clients.UserId = Users.Id " \
                f"WHERE Users.Username = '{username}' "

        cursor = Database.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        return result
    

    @staticmethod
    def get_id(table: str): 
        query = f"SELECT MAX(Id) FROM {table};"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            id = cursor.fetchone()[0]
            cursor.close()
            return id + 1
        except Exception as e:
            print(e)
            return -1
    

    @staticmethod
    def add_client(username: str, password: str, email: str, first_name: str, last_name: str,
                   age: int, hobbies: str, occupation: str, other: str, country: str, city: str):
        location_id = Database.get_id('Locations')
        if location_id == -1:
            return None
        query = "INSERT INTO Locations (Id, Country, City) " \
                f"VALUES ({location_id}, '{country}', '{city}');"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        information_id = Database.get_id('Informations')
        if information_id == -1:
            return None
        query = "INSERT INTO Informations (Id, Hobbies, Occupation, Other) " \
                f"VALUES ({information_id}, '{hobbies}', '{occupation}', '{other}');"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        user_id = Database.get_id('Users')
        if user_id == -1:
            return None
        query = "INSERT INTO Users (Id, Username, Password, Email, RoleId) " \
                f"VALUES ({user_id}, '{username}', '{password}', '{email}', 1);"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        client_id = Database.get_id('Clients')
        if client_id == -1:
            return None
        query = "INSERT INTO Clients (Id, FirstName, LastName, Age, LocationId, InformationId, UserId) " \
                f"VALUES ({client_id}, '{first_name}', '{last_name}', '{age}', '{location_id}', '{information_id}', " \
                f"'{user_id}');"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        Database.connection.commit()
        
        client = Client(client_id, first_name, last_name, age, '', False, 
                        user_id, information_id, location_id)

        return client
    

    @staticmethod
    def edit_client(user: User, username: str, password: str, email: str, first_name: str,
                    last_name: str, age: int, hobbies: str, occupation: str, other: str, country: str, city: str):
        client = Database.get_client(user.username)
        if client is None:
            return None

        if not username.isspace() and username != '':
            query = f"UPDATE Users SET Username = '{username}' WHERE Id = {user.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 
                
            user.username = username

        if not password.isspace() and password != '':
            query = f"UPDATE Users SET Password = '{password}' WHERE Id = {user.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 
            
            user.password = password

        if not email.isspace() and email != '':
            query = f"UPDATE Users SET Email = '{email}' WHERE Id = {user.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 
            
            user.email = email

        if not first_name.isspace() and first_name != '':
            query = f"UPDATE Clients SET FirstName = '{first_name}' WHERE Id = {client.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not last_name.isspace() and last_name != '':
            query = f"UPDATE Clients SET LastName = '{last_name}' WHERE Id = {client.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if age != -1:
            query = f"UPDATE Clients SET Age = {age} WHERE Id = {client.id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not hobbies.isspace() and hobbies != '':
            query = f"UPDATE Informations SET Hobbies = '{hobbies}' WHERE Id = {client.information_id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not occupation.isspace() and occupation != '':
            query = f"UPDATE Informations SET Occupation = '{occupation}' WHERE Id = {client.information_id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not other.isspace() and other != '':
            query = f"UPDATE Informations SET Other = '{other}' WHERE Id = {client.information_id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not country.isspace() and country != '':
            query = f"UPDATE Locations SET Country = '{country}' WHERE Id = {client.location_id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        if not city.isspace() and city != '':
            query = f"UPDATE Locations SET City = '{city}' WHERE Id = {client.location_id};"

            try:
                cursor = Database.connection.cursor()
                cursor.execute(query)
                cursor.close()
            except Exception as e:
                print(e)
                return None 

        Database.connection.commit()

        return user
    

    @staticmethod
    def edit_client_role(username: str):
        client = Database.get_client(username)

        if client is None:
            return False

        query = f"UPDATE Users SET RoleId = 2 WHERE Username = '{username}';"
    
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return False
        
        query = f"DELETE FROM Clients WHERE Id = {client.id};"
    
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return False
        
        # Database.connection.commit()

        return True
    

    @staticmethod
    def is_banned(username: str):
        client = Database.get_client(username)

        if client is None or not client.banned:
            return False
        else:
            return True


    @staticmethod
    def add_chat(client_username: str, guest_username: str, name: str):
        if client_username == guest_username:
            return None
        
        client = Database.get_client(client_username)
        if client is None:
            return None
        
        guest = Database.get_client(guest_username)
        if guest is None:
            return None
        
        chat_id = Database.get_id('Chats')
        if chat_id == -1:
            return None
        
        query = "INSERT INTO Chats (Id, Name) " \
                f"VALUES ({chat_id}, '{name}');"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        clientchat_id = Database.get_id('ClientChats')
        if clientchat_id == -1:
            return None
        
        query = "INSERT INTO ClientChats (Id, clientId, chatId) " \
                f"VALUES ({clientchat_id}, {client.id}, {chat_id}), " \
                f"({clientchat_id + 1}, {guest.id}, {chat_id});"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        Database.connection.commit()

        return True


    @staticmethod
    def add_meeting(client_username: str, guest_username: str, name: str, 
                    datetime: str, country: str, city: str, address: str):
        if guest_username.isspace() or name.isspace() or datetime.isspace() or \
           country.isspace() or city.isspace() or address.isspace():
            return None

        if client_username == guest_username:
            return None
        
        client = Database.get_client(client_username)
        if client is None:
            return None
        
        guest = Database.get_client(guest_username)
        if guest is None:
            return None

        location_id = Database.get_id('Locations')
        if location_id == -1:
            return None
        
        query = "INSERT INTO Locations (Id, Country, City, Address) " \
                f"VALUES ({location_id}, '{country}', '{city}', '{address}');"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        meeting_id = Database.get_id('Meetings')
        if meeting_id == -1:
            return None
        
        query = "INSERT INTO Meetings (Id, Name, Datetime, LocationId) " \
                f"VALUES ({meeting_id}, '{name}', '{datetime}', {location_id});"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        clientmeeting_id = Database.get_id('ClientMeetings')
        if clientmeeting_id == -1:
            return None

        query = "INSERT INTO ClientMeetings (Id, clientId, meetingId) " \
                f"VALUES ({clientmeeting_id}, {client.id}, {meeting_id}), " \
                f"({clientmeeting_id + 1}, {guest.id}, {meeting_id});"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        Database.connection.commit()
        
        return True
        

    @staticmethod
    def add_complaint(username: str, content: str):
        client = Database.get_client(username)
        if client is None or content == '' or content.isspace():
            return None
        
        complaint_id = Database.get_id('Complaints')
        if complaint_id == -1:
            return None
        
        query = "INSERT INTO Complaints (Id, Content, ClientId) " \
                f"VALUES ({complaint_id}, '{content}', {client.id});"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        Database.connection.commit()

        return True 
    

    @staticmethod
    def get_chat(id: str, username: str):
        try:
            chat_id = int(id)
        except Exception as e:
            return None 
        
        client = Database.get_client(username)
        if client is None:
            return None
        
        query = "SELECT Content, DateTime, Sender FROM Messages " \
                f"JOIN Chats ON ChatId = Chats.Id AND Chats.Id = {chat_id} " \
                "ORDER BY DateTime ASC;"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None

        chats = Database.get_client_chats(username)
        if chats is None:
            return None
        
        for chat in chats:
            if chat[0] == chat_id:
                return Chat(chat_id, chat[1], result, chat[2])    


    @staticmethod
    def add_message(content: str, sender: str, chat: int): 
        message_id = Database.get_id('Messages')
        if message_id == -1 or content.isspace() or content == '':
            return None

        query = "INSERT INTO Messages (Id, Content, DateTime, Sender, ChatId) " \
                f"VALUES ({message_id}, '{content}', NOW(), '{sender}', {chat});"
        try:
            cursor = Database.connection.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        Database.connection.commit()

        return True 
    