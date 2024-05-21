import sqlite3
import json

def store_encoding(encoding_list):
    db = sqlite3.connect("/home/bisher/facial_recognition/Local Database/PiGuardian.db")
    cursor = db.cursor()
    
    #Now we can create our table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS encodings(encoding TEXT)")
    
    #Convert to JSON
    encoding_json = json.dumps(encoding_list)
    
    #Insert the JSON list    
    cursor.execute("INSERT INTO encodings (encoding) VALUES (?)", (encoding_json,))
    
    db.commit()
    db.close()
    
def store_name(username):
    db = sqlite3.connect("/home/bisher/facial_recognition/Local Database/PiGuardian.db")
    cursor = db.cursor()
    
    #Now we can create our table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS names(name TEXT)")
    
    #Insert the name   
    cursor.execute("INSERT INTO names (name) VALUES (?)", (username,))
    
    db.commit()
    db.close()
    
def store_attempt(success):
    db = sqlite3.connect("/home/bisher/facial_recognition/Local Database/PiGuardian.db")
    cursor = db.cursor()
    
    #Now we can create our table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS attempts(outcome TEXT)")
    
    cursor.execute("INSERT INTO attempts (outcome) VALUES (?)", (success,))
    
    db.commit()
    db.close()