import pymongo
from pymongo import MongoClient

class Database:
    
    def __init__(self):
        #remember to add the server ip to the ip whitelist in the mongoDB
        self.cluster = MongoClient("mongodb+srv://heyCortona:Hc123456@heycortona-1woqm.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.cluster["heyCortona"]
        self.users = self.db["users"]
        
    def addUser(self,phone_number,name,city):
        post = {"phone_number": phone_number, "name": name, "city": city}
        self.users.insert_one(post)

    def findUser(self,phone_number):
        result = self.users.find_one({"phone_number":phone_number})
        return result

    def getAllUsers(self):
        myUsers = []
        users = self.users.find({})
        for user in users:
            myUsers.append(user)
        return myUsers            

    def deleteUser(self, phone_number):
        self.users.delete_one({"phone_number":phone_number})

    def deleteAllUsers(self):
        self.users.delete_many({})
