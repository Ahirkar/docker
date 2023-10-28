from pymongo import MongoClient
from urllib.parse import quote_plus

# password = quote_plus("Idrbt@123")
# username = quote_plus("milindahirkar10")
# connection = f"mongodb+srv://{username}:{password}@cluster0.c196v7q.mongo.net/test"

# password = quote_plus("Vkycadmin@1234")
# username = quote_plus("admin")
# password = os.environ.get('PASSWORD_DB')
# username = os.environ.get("USER_NAME")
# encoded_password = quote_plus(password)
# Client = MongoClient(f"mongodb://172.27.22.144:8080")
Client = MongoClient(f"mongodb+srv://vkyc:vkyc123@cluster0.va96o1e.mongodb.net/?retryWrites=true&w=majority")
# database_name = Client.list_database_names()
database_name = Client["data"]
collection = database_name["person_info"]
record = collection.find_one({"aadhar_number":"365412489964"})
print(record)
# Client.close()
# print(record)
# first_name = record["first_name"]
# middle_name = record["middle_name"]
# last_name = record["last_name"]
# dat = record["date_of_birth"]
# print(dat)
# print(first_name)
# if middle_name is None:
#     middle_name = ""
# full_name = first_name + " " + middle_name + " " + last_name
# full_name = " ".join(full_name.split()).lower()
# print(full_name)

# import re
# matches = re.findall(r'\b(male|female|others)\b', "i am male")
# print(matches[0][0].upper())

# dat = "2002-08-20T00:00:00.000+00:00"
# record_dt = dat.split("T")
# print(record_dt)


# from pymongo import MongoClient
# import csv

# # MongoDB Atlas connection string
# connection_string = "mongodb+srv://vkyc:vkyc123@cluster0.va96o1e.mongodb.net/?retryWrites=true&w=majority"

# # Local JSON file path
# csv_file_path = "/home/vkyc/person.csv"

# # Connect to MongoDB Atlas
# client = MongoClient(connection_string)

# # Access the database
# db = client.get_database("data")

# # Choose the collection
# collection = db.get_collection("person_info")

# # Open and read the JSON file
# # Open and read the CSV file
# with open(csv_file_path, "r") as file:
#     reader = csv.DictReader(file)
#     data = list(reader)

# # Insert the data into the collection
# collection.insert_many(data)

# # Close the MongoDB Atlas connection
# client.close()



# mongodb://172.27.22.144:8080/