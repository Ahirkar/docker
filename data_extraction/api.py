from flask import Flask, request, jsonify
from pymongo import MongoClient
from utilities import document_extractor_pancard, document_extractor_aadharcard, model_predict
from paddleocr import PaddleOCR

# creating connection to mongodb database
Client = MongoClient(f"mongodb+srv://vkyc:vkyc123@cluster0.va96o1e.mongodb.net/?retryWrites=true&w=majority")  # mongodb client connection string
database_name = Client["documents"]  # creating connection for a mongodb user
coll = database_name["extracted_info"]  # establishing connection with database

# creating data object for PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory

# creating flask app instance
app = Flask(__name__)


@app.route('/data_extraction_image', methods=['GET', 'POST'])
def data_extraction_image():
    if request.method == 'POST':
        try:
            super_resolved_data = request.get_json()
            super_resolved_image = super_resolved_data['data_path']
            result = ocr.ocr(super_resolved_image, cls=True)
            output_lst = [line[1][0] for line in result[0]]

            # use the vgg16 model to check the image type
            if model_predict(super_resolved_image) == 'PANCARD':
                extracted_data = document_extractor_pancard(output_lst)

                # inserting extracted data into mongodb
                dic = coll.insert_one({
                    'Date of Birth': extracted_data['DOB'],
                    'NAME': extracted_data['NAME'],
                    'FATHER NAME': extracted_data['FATHER NAME'],
                    'ID CARD': extracted_data['ID CARD'],
                    'ID NO': extracted_data['ID NO.'],
                })

            elif model_predict(super_resolved_image) == 'AADHARCARD':
                extracted_data = document_extractor_aadharcard(output_lst)
                dic = coll.insert_one({
                    'Date of Birth': extracted_data['DOB'],
                    'NAME': extracted_data['NAME'],
                    'ID CARD': extracted_data['ID CARD'],
                    'GENDER': extracted_data['GENDER'],
                    'ID NO': extracted_data['ID NO.'],
                })

            # making a check if extracted data pushed to mongodb database
            if dic.inserted_id is not None:
                # chatbotapi = requests.post('chatbotapipath', params=dic.inserted_id)  # make a call to chatbot api
                return jsonify({
                    'message': 'Data extraction completed successfully, pushed to mongodb, complied data send to '
                               'chatbot'}), 200
            else:
                return jsonify({'message': 'Data extraction completed successfully, push to mongodb failed'}), 205
        except Exception as e:
            return jsonify({'message': str(e)}), 400
    else:
        return jsonify({'message': 'Method not supported'}), 405


@app.get('/document_type')
def document_type():
    super_resolved_data = request.get_json()
    file = super_resolved_data['data_path']
    doc_type = model_predict(file)
    return jsonify({"document_type": doc_type})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)
