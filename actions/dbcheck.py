import re
import requests
from pymongo import MongoClient
from datetime import datetime

# def fetch_record(aadhaar):
#     global record
#     Client = MongoClient(f"mongodb://172.27.22.144:8080")
#     database_name = Client["vkyc"]
#     collection = database_name["kyc_app_person"]
#     record = collection.find_one({"aadhar_number":aadhaar})
#     if record is not None:
#         record = dict(record)
#         Client.close()
#         return True
#     else:
#         Client.close()
#         return False


def task():
    chatbotapi = requests.post(
        url='http://127.0.0.1:5006/data_extraction_image',
        json={"data_path": "https://amitnew.s3.amazonaws.com/pancard/1.jpg"})
    print(chatbotapi.status_code, chatbotapi.text)


def fetch_record(aadhaar):
    global record
    Client = MongoClient(f"mongodb+srv://vkyc:vkyc123@cluster0.va96o1e.mongodb.net/?retryWrites=true&w=majority")
    database_name = Client["data"]
    collection = database_name["person_info"]
    record = collection.find_one({"aadhar_number":aadhaar})
    if record is not None:
        record = dict(record)
        Client.close()
        return True
    else:
        Client.close()
        return False

# data = pd.read_excel('data.xlsx')

def verify_aadhaar(aadhaar):
    aadhaar = str(aadhaar)
    match = re.findall(r'\b\d{12}\b', aadhaar)[0]
    print(match)
    if len(aadhaar) == 12:
        return fetch_record(aadhaar)

def verify_user_name(user_input, message):
    first_name = record["first_name"]
    middle_name = record["middle_name"]
    last_name = record["last_name"]
    user_input = user_input.lower()
    print(first_name)
    if middle_name is None:
        middle_name = ""
    full_name = first_name + " " + middle_name + " " + last_name
    full_name = " ".join(full_name.split()).lower()
    print(full_name)
    if len(re.findall(r"\Amy name is", user_input)) > 0:
        entity = user_input[11:]
        return full_name == str(entity)
    
    elif len(re.findall(r"\Amyself", user_input)) > 0:
        entity = user_input[7:]
        return full_name == str(entity)
    
    elif len(re.findall(r"\Ai am", user_input)) > 0:
        entity = user_input[5:]
        return full_name == str(entity)
    
    elif len(re.findall(r"\bis my name", user_input)) > 0:
        entity = user_input.split(" is")[0]
        return full_name == str(entity)
    
    elif len(re.findall(r"\bmy name", user_input)) > 0:
        entity = user_input.split(" my")[0]
        return full_name == str(entity)
    else:
        return full_name == str(user_input)
     

def verify_pan_number(user_input, message):
    if message is None:
        user_input = str(user_input)
        if not user_input.isupper():
          user_input = user_input.upper()
        re_exp = r"[A-Z]{3}[A-Z]{1}[A-Z]{1}[0-9]{4}[A-Z]{1}"
        entity = re.findall(re_exp, user_input)
        if not bool(len(entity) == 0):
            return record["pan_number"] == entity[0]
    else:
        return record["pan_number"] == str(message).upper()


def verify_gender_type(user_input, message):
    matches = re.findall(r'\b(male|female|other|others)\b', user_input, re.IGNORECASE)
    print(record["gender"])
    if len(matches) == 0:
        return False
    else:
        gender = matches[0][0].upper()
        return record["gender"] == gender


def verify_city(user_input, message):
    # print({"user_input": user_input})
    # print({"message": message})
    user_input = str(user_input).lower()
    message = str(message).lower()
    if message is None:
        if len(re.findall(r"\Aliving in",user_input))>0:
            return record["city"] == user_input[10:]
        elif len(re.findall(r"\Ain",user_input))>0:
            return record["city"] == user_input[3:]
        elif len(re.findall(r"\Ai currently",user_input))>0:
            return record["city"] == user_input[22:]
        elif len(re.findall(r"\Amy city",user_input))>0:
            return record["city"] == user_input[11:]
        elif len(re.findall(r"\bis my city",user_input))>0:
            return record["city"] == user_input.split(" is")[0]
        elif len(re.findall(r"\Amy city name",user_input))>0:
            return record["city"] == user_input[13:]
        elif len(re.findall(r"\Ai live in",user_input))>0:
            return record["city"] == user_input[10:]
        elif len(re.findall(r"\Ai live", user_input))>0:
            return record["city"] == user_input[5:]
        elif len(re.findall(r"city$",user_input))>0:
            return record["city"] == user_input.split(" city")[0]
        elif len(re.findall(r"\Acity",user_input))>0:
            return record["city"] == user_input[5:]
        else:
            return record["city"] == user_input
    else:
        print(record["city"])
        return str(record["city"]).lower() == message


def verify_mobileNO(user_input, message):
    if message is None:
        if bool(re.search(r'\d', user_input)):
            number = re.findall(r'\b\d{10}\b', user_input)[0]
            return record["mobile_number"] == str(number)
    else:
        print(record["mobile_number"])
        return str(record["mobile_number"]) == str(message)


def verify_Pin_code(user_input, message):
    if message is None:
        if bool(re.search(r'\d', user_input)):
            number = re.findall(r'\b\d{6}\b', user_input)[0]
            return record["pincode"] == str(number)
    else:
        print(record["pincode"])
        return str(record["pincode"]) == str(message)


def verify_state(user_input, message):
    user_input = str(user_input).lower()
    message = str(message).lower()
    if message is None:
        if len(re.findall(r"\Aliving in",user_input))>0:
            return record["state"] == user_input[10:]
        elif len(re.findall(r"\Ain",user_input))>0:
            return record["state"] == user_input[3:]
        elif len(re.findall(r"\Ai currently in",user_input))>0:
            return record["state"] == user_input[22:]
        elif len(re.findall(r"\Amy state",user_input))>0:
            return record["state"] == user_input[12:]
        elif len(re.findall(r"\bis my state",user_input))>0:
            return record["state"] == user_input.split(" is")[0]
        elif len(re.findall(r"\Amy state name",user_input))>0:
            return record["state"] == user_input[13:]
        elif len(re.findall(r"\Ai live in",user_input))>0:
            return record["state"] == user_input[10:]
        elif len(re.findall(r"\Ai live", user_input))>0:
            return record["state"] == user_input[5:]
        elif len(re.findall(r"state$",user_input))>0:
            return record["state"] == user_input.split(" city")[0]
        elif len(re.findall(r"\Astate",user_input))>0:
            return record["state"] ==  user_input[5:]
        else:
            record["state"] == user_input
    else:
        print(record["state"])
        return str(record["state"]).lower() == message


def verify_birth_date(user_input, message):
    print({"user_input":user_input})
    record_dt = str(record["date_of_birth"]).split("T")[0]
    # dates = datetime.strptime(record_dt, '%d %B %Y')
    # form_new = dates.strftime('%Y-%m-%d')
    regEx = r"(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<month>\w+)\s+(?P<year>\d{4})"
    result = re.search(regEx, user_input)
    print({"record_dt":record_dt})
    dt = None
    if result:
        day = result.group('day')
        month = result.group('month')
        year = result.group('year')
        # Convert month name to title case
        month = month.capitalize()
        try:
            dt = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
        except ValueError:
            try:
                dt = datetime.strptime(f"{day} {month[:3]} {year}", "%d %b %Y")
            except ValueError:
                pass
    if dt:
        formatted_date = dt.strftime('%Y-%m-%d')
        print({"formatted_date":formatted_date})
        return str(record_dt) == str(formatted_date)
    

# def verify_birth_date(user_input, message):
#     print(record["DOB"])
#     return record["DOB"] == str(user_input)


# def verify_district(user_input, message):
#     print({"user_input": user_input})
#     print({"message": message})
#     if message is None:
#         if len(re.findall(r"\Aliving in",user_input))>0:
#             return record["DISTRICT"] == user_input[10:]
#         elif len(re.findall(r"\Ain",user_input))>0:
#             return record["DISTRICT"] == user_input[3:]
#         elif len(re.findall(r"\Ai currently in",user_input))>0:
#             return record["DISTRICT"] == user_input[22:]
#         elif len(re.findall(r"\Amy district",user_input))>0:
#             return record["DISTRICT"] == user_input[12:]
#         elif len(re.findall(r"\bis my district",user_input))>0:
#             return record["DISTRICT"] == user_input.split(" is")[0]
#         elif len(re.findall(r"\Amy district name",user_input))>0:
#             return record["DISTRICT"] == user_input[16:]
#         elif len(re.findall(r"\Ai live in",user_input))>0:
#             return record["DISTRICT"] == user_input[10:]
#         elif len(re.findall(r"\Ai live", user_input))>0:
#             return record["DISTRICT"] == user_input[5:]
#         elif len(re.findall(r"district$",user_input))>0:
#             return record["DISTRICT"] == user_input.split(" city")[0]
#         elif len(re.findall(r"\Adistrict",user_input))>0:
#             return record["DISTRICT"] ==  user_input[5:]
#         elif len(re.findall(r"\Amy district is ",user_input))>0:
#             return record["DISTRICT"] == user_input[15:]
#         else:
#             return record["DISTRICT"] == user_input
#     else:
#         print(record["DISTRICT"])
#         return record["DISTRICT"] == str(message)