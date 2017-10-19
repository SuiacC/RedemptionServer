from pymongo import MongoClient


DBNAME = 'redemptionDB'
DBCOLLECTION = 'aggregate'
DBHOST = 'localhost'
DBPORT = 32768
DBUSERNAME = ''
DBPASSWORD = ''

#Connect Mongo by means of creation of MongoClient
def connectMongoDB():
    return MongoClient(DBHOST, DBPORT)

#Close MongoClient connection
def closeMongoDB(client):
    client.close()

#Select the collection, implying dbname as default DBNAME
def selectCollectionMongoDB(client, dbcollection=DBCOLLECTION, dbname=DBNAME):
    db = client[dbname]
    return db[dbcollection]

#Returns all the data
def selectAllSources():
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find()


#Get MAC address in DB
def getMAC(MAC):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find({"MAC": MAC})

#Insert and element into a collection
def insertElementMongoDB(data):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.insert_one(data)