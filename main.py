from Database import Database

db = Database("./db/db.json")
# db.set("test2", "testsets")

# db.save()
db.load()
db.delete("key")

print(db)
print ( db.get("test2") )
