
class User:
    def __init__(self, id, username, password, email, role):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

class Role:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Complaint:
    def __init__(self, id, content, client_id):
        self.id = id
        self.content = content
        self.client_id = client_id


class Action:
    def __init__(self, id, name, action, client_id):
        self.id = id
        self.name = name
        self.action = action
        self.client_id = client_id

class Client:
    def __init__(self, id, first_name, last_name, age, photo, banned, user_id, information_id, location_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.photo = photo
        self.banned = banned
        self.user_id = user_id
        self.information_id = information_id
        self.location_id = location_id

class Information:
    def __init__(self, id, hobbies, occupation, other):
        self.id = id
        self.hobbies = hobbies
        self.occupation = occupation
        self.other = other

class Chat:
    def __init__(self, id, name, messages, partner):
        self.id = id
        self.name = name
        self.messages = messages
        self.partner = partner

class Message:
    def __init__(self, id, content, datetime, sender, chat):
        self.id = id
        self.content = content
        self.datetime = datetime
        self.sender = sender
        self.chat = chat
