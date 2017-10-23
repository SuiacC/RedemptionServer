from cryptography.fernet import Fernet
import json
import responses
import database

class Requests:

    req = any

    def __init__(self, req, type = "POST"):
        if type == "POST":
            self.req = json.loads(req.body)
        else:
            self.req = req


     # getters
    def getBody(self):
        return self.req

    def getReq(self, r):
        return r["r"]

    def createKey(self):
        # Put this somewhere safe!
        return Fernet.generate_key()

    #
    def checkMAC(self,data):
        # Initialize response
        response = responses.Responses()

        MAC = data["MAC"]
        dbFunction = database.getMAC(MAC)
        if not dbFunction:
            key = self.createKey()
            database.insertElementMongoDB({"MAC": MAC,"key": key,"payed": False})
            response.setResponse("response", False)
            response.setResponse("key",key)
        else:
            response.setResponse("response", True)
            response.setResponse("key", dbFunction["key"])
            
        return response

    def deleteUser(self,data):

        response = responses.Responses()

        MAC = data["MAC"]
        dbFunction = database.getMAC(MAC)
        if not dbFunction:
            response.setResponse("response",False)
        else:
            database.deleteUser(MAC)
            response.setResponse("response",True)
            response.setResponse("key", dbFunction["key"])



    def postRequest(self):

        # Initialize response
        response = responses.Responses()

        # Grub body from request
        data = self.getBody()

        # Grub request from body
        r = self.getReq(data)
        print "request: " + r

        # Switch 'r' for every possible request
        if r == "CheckMAC":
            response = self.checkMAC(data)
        elif r == "IfUserPayed":
            response = self.deleteUser(data)

        print "response: "
        print response.getResponse()

        # If we haven't a response
        if not response.getResponse():
            response.setResponse("response", False)
            response.setResponse("Message", "Qualcosa e' andato storto")

        # Return the response
        return response.getResponse()