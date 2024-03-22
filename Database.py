import os
import json
import time

class Database:
    def __init__(self, path):
        if path[:5] != ".json" :
            path + ".json"
        self.path = path
        self.data : dict = {}
        self.load()

    def load(self):
        # if not os.path.exists(self.path) :
        #     self.data = {"test" : "test"}
        #     self.save()
            
        with open(self.path, "r") as f :
            self.data = json.load(f)

    def save(self):
        with open(self.path, "w") as f :
            json.dump(self.data , f)

    def get(self, key : str):
        print( self.data.keys() )
        if not key in self.data.keys() :
            return False
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value
        self.save()
        return True

    def delete(self, key):
        if not key in self.data.keys() :
            return False
        
        del self.data[key]
        self.save()
        return True

    def exists(self, key):
        return key in self.data.keys() 

    def keys(self):
        return self.data.keys()

    def values(self):
            return self.data.values()

    def items(self):
        return self.data.items()

    def clear(self):
        self.data = {}
        self.save()
        return 1

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)
    
def main():
    db = Database("./db/db.json")
    print(db.data)

    db.set(key="keykeykey", value="valuevaluevalue")
    print("db.get(keykeykey) = ", db.get(key="keykeykey"))
    is_exist = db.exists("keykeykey")
    print("db.exists(keykeykey) = ", is_exist)
    db.delete("keykeykey")
    print("db.get(keykeykey) = ", db.get(key="keykeykey"), " after delete")
    is_exist = db.exists("keykeykey")
    print("db.exists(keykeykey) = ", is_exist)

if __name__ == "__main__":

   main()