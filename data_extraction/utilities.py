import re
from keras.models import model_from_json
import tensorflow as tf
import numpy as np
import urllib
from io import BytesIO


# Loading model
json_file = open('./model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("./model_weights.h5")


# Template based document extractor
def document_extractor_pancard(input):
    data_dict = dict()
    data_dict['DOB'] = ''
    filtered_data = input
    lower_filtered_data = [data.lower() for data in filtered_data]
    name_bool = [(data, index) for (index, data) in enumerate(lower_filtered_data) if
                 'name' in data and 'father' not in data]
    father_bool = [(data, index) for (index, data) in enumerate(lower_filtered_data) if 'father' in data]
    govt_bool = [(data, index) for (index, data) in enumerate(lower_filtered_data) if 'govt' in data]
    if name_bool:
        data_dict["NAME"] = filtered_data[name_bool[0][1] + 1]
    if father_bool:
        data_dict["FATHER NAME"] = filtered_data[father_bool[0][1] + 1]

    for index, data in enumerate(filtered_data):
        if data_dict.get("ID CARD") is None and (
                'income' in data.lower() or 'tax' in data.lower() or 'department' in data.lower()):  # ID CARD
            data_dict["ID CARD"] = 'Pan Card'

        elif data_dict.get("NAME") is None and govt_bool:
            data_dict["NAME"] = filtered_data[govt_bool[0][1] + 1] if 'income' not in filtered_data[
                govt_bool[0][1] + 1].lower() else filtered_data[govt_bool[0][1] + 2]

        elif data_dict.get("FATHER NAME") is None and govt_bool:
            data_dict["FATHER NAME"] = filtered_data[govt_bool[0][1] + 2] if 'income' not in filtered_data[
                govt_bool[0][1] + 1].lower() else filtered_data[govt_bool[0][1] + 3]

        elif re.findall("\d{2}[/-]\d{2}[/-]\d{4}", data):  # extracting 'DOB' of format [-|/]
            pattern = "\d{2}[/-]\d{2}[/-]\d{4}"
            dates = re.findall(pattern, data)
            for date in dates:
                if "-" in date:
                    day, month, year = map(int, date.split("-"))
                else:
                    day, month, year = map(int, date.split("/"))
                if 1 <= day <= 31 and 1 <= month <= 12:
                    data_dict['DOB'] = date

        elif data[0].isalpha() and len(data.replace(' ', '')) == 10 and data[-1].isalpha() and data[
                                                                                               5:9].isdigit():  # ID NO.
            data_dict['ID NO.'] = data.replace(' ', '')
    return data_dict


def document_extractor_aadharcard(input):
    data_dict = dict()
    data_dict['DOB'] = ''
    filtered_data = input
    print(filtered_data)
    for index, data in enumerate(filtered_data):
        if data_dict.get("ID CARD") is None and 'govern' in data.lower():  # ID CARD
            data_dict["ID CARD"] = 'Aadhar Card'
        elif 0 < index < 4 and data.lower()[0].isalpha() and (data.lower()[-1].isalpha() or data[-1] in ['.',
                                                                                                         '-']) and 'female' not in data.lower() and 'male' not in data.lower() and len(
            data) > 3:
            data_dict["NAME"] = data
        elif 'female' in data.lower():  # Gender
            data_dict["GENDER"] = 'FEMALE'
        elif data_dict.get("GENDER") is None and 'male' in data.lower():  # Gender
            data_dict["GENDER"] = 'MALE'
        elif 'year' in data.lower() or 'yob' in data.lower():  # extracting year from date of birth
            data_dict['DOB'] = re.findall(r'-?\d+\.?\d*', data)[0]
        elif re.findall("\d{2}[/-]\d{2}[/-]\d{4}", data):  # extracting 'DOB' of format [-|/]
            pattern = "\d{2}[/-]\d{2}[/-]\d{4}"
            dates = re.findall(pattern, data)
            for date in dates:
                if "-" in date:
                    day, month, year = map(int, date.split("-"))
                else:
                    day, month, year = map(int, date.split("/"))
                if 1 <= day <= 31 and 1 <= month <= 12:
                    data_dict['DOB'] = date
        elif 'DOB' in data:
            data_dict['DOB'] = data[data.index('B') + 1:]
        elif 'D0B' in data:
            data_dict['DOB'] = data[data.index('B') + 1:]
        elif data[0].isdigit() and 11 <= len(data.replace(' ', '')) <= 12 and data[-1].isdigit():  # ID NO.
            data_dict['ID NO.'] = data.replace(' ', '')
        if len(data_dict['DOB']) <= 7 and 'dob' in data.lower():
            if re.findall(r'-?\d+\.?\d*', data):  # extracting without [-|/] dob from data
                data_dict['DOB'] = re.findall(r'-?\d+\.?\d*', data)[0]
    return data_dict


# Document classification model
def model_predict(url):
    check_doc_type = {0: 'AADHARCARD', 1: "PANCARD", 2: 'Other document'}
    with urllib.request.urlopen(url) as url:
        img = tf.keras.utils.load_img(BytesIO(url.read()), target_size=(224, 224))
    # img = tf.keras.utils.load_img(url, target_size=(224, 224))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    features = model.predict(x)
    features = features.flatten()
    doc_type = check_doc_type[int(np.argmax(features))]
    return doc_type
