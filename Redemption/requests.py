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
            database.insertElementMongoDB({"MAC": MAC,"key": self.createKey(),"payed": False})
            response.setResponse("response", False)
        else:
            response.setResponse("response", True)
            response.setResponse("key", dbFunction["key"])
            
        return response


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
            response = self.returnAllDevices()

        print "response: "
        print response.getResponse()

        # If we haven't a response
        if not response.getResponse():
            response.setResponse("reponse", False)
            response.setResponse("Message", "Qualcosa e' andato storto")

        # Return the response
        return response.getResponse()