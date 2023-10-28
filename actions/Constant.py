
from dbcheck import *

FAQ = {
    "greet":"utter_greet",
    "What Vkyc":"utter_WhatVkyc",
    "KYC Process":"utter_KYCProcess",
    "Time required":"utter_TimeRequired1",
    "eligibility":"utter_eligibility",
    "Device":"utter_device",
    "Bot availbility":"utter_BotAvailibility",
    "Vkyc Repeat":"utter_VkycRepeat",
    "StartVkyc":"utter_confirm",
    "Vkyc Timecycle":"utter_VkycTimecycle",
    "Post Vkyc":"utter_PostKyc",
    "StartVkyc":"utter_VerifyKyc", 
    "Required Documents":"utter_DocumentRequirement",
    "Reply to Answer1":"utter_ReplyToAnswer1",
    "Why Vkyc":"utter_WhyVkyc",
    "Registration Completion":"utter_RegistrationCompletion",
    "Question about Data":"utter_QuestionAboutData"
}


RESPONSES = {
        "utter_Gender Type":verify_gender_type,
        "utter_city name":verify_city, 
        "utter_name":verify_user_name,
        "utter_Pan Card":verify_pan_number,
        "utter_state name":verify_state,
        "utter_Pincode":verify_Pin_code, 
        "utter_Mobile Number":verify_mobileNO,
        "utter_Date of Birth":verify_birth_date
}

# BLOCK_INTENTS = ["greet", "What Vkyc", "Time required", "Notconform",
#                  "eligibility", "Device", "Bot availbility", "Vkyc Repeat",
#                  "StartVkyc", "Vkyc Timecycle", "Post Vkyc", 
#                  "Required Documents", "Reply to Answer1", 
#                  "Question about Data", "StartVkyc","Registration Completion"
# ]
VERIFY_INTENT = [
    "name", "Date of Birth", "gender", "City", "State", "pincode", "Mobile Number", "Pan Number"
]

VERIFY_UTTERANCES = [
    "utter_Gender Type", "utter_city name",
    "utter_name", "utter_Pan Card",
    "utter_state name", "utter_Date of Birth",
    "utter_Pincode", "utter_Mobile Number"
]


WARNINGS_AUDIO = [
    "utter_audiostrike1",
    "utter_audiostrike2",
    "utter_audiostrike3"
]

WARNINGS_VIDEO = [
    "utter_videostrike1",
    "utter_videostrike2",
    "utter_videostrike3"
]

WARNING_AADHAAR = [
    "utter_aadhaarstrike1",
    "utter_aadhaarstrike2",
    "utter_aadhaarstrike3"
]

ACTION_LIST = [
    "action_welcome_msg", "action_start_camera",
    "action_Que_Selection", "action_verify_aadhaar",
    "action_first_aadhaar", "action_video_capture", "action_FAQ"
]

STRIKE = [
    "utter_strike1", "utter_strike2", "utter_strike3"
]

skip_list = [
    "utter_skip", "utter_warn","confirm",
    "Notconfirm", "utter_confirmcapture",
    "utter_Gender Type", "utter_city name",
    "utter_bame", "utter_Pan Card",
    "utter_state name", "utter_Date of Birth",
    "utter_Pincode", "utter_Mobile Number"
]

USE_CASE = ["Update", "Consent", "Forget Password", "Know Info", "Info using"]

CAP_CONFIRMATION = [
    "utter_confirmcapture", "utter_waitconfirmation",
    "utter_interrupt", "utter_waitconfirmation1",
    "utter_fcdone", "utter_acdn",
    "utter_PvideoQng", "utter_FvideoQNG",
    "utter_Avideoqng", "utter_audiostrike1", 
    "utter_audiostrike2", "utter_audiostrike3", 
    "utter_videostrike1", "utter_videostrike2", 
    "utter_videostrike3"
]


BOT_UTTERANCES = {
'utter_confirm': 'Great!! lets start, Now give me your 12 digit Aadhaar number.',
 'utter_VerifyKyc': 'Now, I will start your verification process. Please give your 12 digit Aadhaar Number',
 'utter_askagain': 'Heyy, hope your doing well. Should I start your vKYC.',
 'utter_TimeRequired1': 'Within 5-10 minutes your online vKYC verification will be done.',
 'utter_DocumentRequirement': 'To complete vKYC you should have your Aadhar Card and Pan Card with you.',
 'utter_KYCProcess': 'After registration on portal you will get a link for vKYC verification, follow that link it will open vkyc Bot first it will ask aadhaar number for initial verification then it will ask three random questions from the data you gave on portal. After giving all correct answers chatbot will capture your face, Aadhaar Card and PAN card.',
 'utter_WhyVkyc': 'To do any banking related works, you need your video-KYC to be completed.',
 'utter_QuestionAboutData': 'Your data is completely safe with us and it will not be shared with anyone.',
 'utter_TimeRequired2': 'Do you get your answer, now can we proceed to your vKYC verification.',
 'utter_PostKyc': "Vkyc process is for user registration & verification, so he/she can avail the bank services, you don't have to go anywhere after vkyc.",
 'utter_device': 'You can use PC, Laptop, SmartPhone.',
 'utter_VkycTimecycle': 'After completing registration for vkyc your URN is valid for next 5 years',
 'utter_RegistrationCompletion': 'At the end of your registration you will receive a SMS that give information about completion of vkyc process',
 'utter_eligibility': 'These are the following criterion for the eligibility of vkyc process',
 'utter_VkycRepeat': "Once you complete the vkyc process you don't need do it again for next few years",
 'utter_greet': 'Heyy hope you are doing well, should I start your VKYC verification.',
 'utter_Notconfirm': 'Ok, What is your doubt?.',
 'utter_randomQ': ' Ok, what do you want to know about VKYC.',
 'utter_name': 'Tell me your full name e.g.: Aman Kedar Jadhav.',
 'utter_Pan Card': 'Give me your Pan number.',
 'utter_state name': 'Which state your from?',
 'utter_city name': 'Which city you from?',
 'utter_Gender Type': 'Tell me your gender identity e.g.: Male, Female or Others.',
 'utter_Pincode': 'Please tell me your area Pincode.',
 'utter_Mobile Number': 'Give me your 10-digit mobile number.',
 'utter_aadhaar number': 'Give me your 12-digit Aadhaar number.',
 'utter_Date of Birth': 'Give me your birth_date e.g.: 1 February 1997.',
 'utter_facecapture': 'Now, please sit straight and look into the camera for the next 5 sec.',
 'utter_fcdone': 'Great , your face capture has been done successfully. Now I need to capture your Aadhaar card, once you are ready with it give me a confirmation as PROCEED',
 'utter_acdn': 'Done with the aadhaar card. Now I need to capture your PAN card, once you are ready with it give me a confirmation as PROCEED. ',
 'utter_sign': 'Ok now hold your signature in-front of the camera for 3 sec. ',
 'utter_fcf': 'Face capture Failed. Please try again.',
 'utter_acf': 'Aadhaar capture Failed. Please try again.',
 'utter_pcf': 'Pan capture Failed. Please try again.',
 'utter_signf': 'Sign capture Failed. Please try again.',
 'utter_exit': 'I am happy to help you thanks.',
 'utter_WhatVkyc': 'vKYC is a secure solution that enables your customers to verify themselves from the comfort of their homes. It allows you to authenticate customer details in real-time through video & AI-driven face match, geo-tagging, and eKYC verification of your documents.',
 'utter_doneSC': 'Congratulations Your Video-KYC has been initiated and sent for further approval. SMS confirmation will be sent to your registered mobile number within 7-10 working days. Thank you for choosing our service. Have a nice day.',
 'utter_ReplyToAnswer2A': 'Please visit the link below to get complete details.',
#  'utter_ReplyToAnswer2B': 'https://twitter.com/idrbt?lang=en',
 'utter_BotAvailibility': 'Bot is available 24*7 you can complete vKYC process any time.',
 'utter_ReplyToAnswer1': 'I am happy that your satisfied with the answer',
 'utter_FvideoQNG': 'Face video quality is not good. Please sit straight under bright light.',
 'utter_Avideoqng': 'Document Aadhar video quality is not good. Please hold it in-front of the camera.',
 'utter_PvideoQng': 'Document Pan video quality is not good. Please hold it in-front of the camera.',
 'utter_feedback': 'Are you satisfied with the explanation',
 'utter_strike1': 'This is not your {name}, please check your {name} and answer the given question properly.',
 'utter_strike2': 'You provided a wrong {name} now you have only one chance left. After that your session will be closed.',
 'utter_strike3': 'You have exceed the limit, Goodbye.',
 'utter_present': 'You already have provided {name}, please answer the given questions.',
 'utter_skip': 'Are you sure you want to skip this question ?',
 'utter_warn': 'Remember that You can skip only one question.',
 'utter_Thanks': 'Thanks for your Co-operation.',
 'utter_audiostrike1': 'Only three attempts are given to complete the voice capture. Now you are remained with 2 attempts only.',
 'utter_audiostrike2': 'Your remained with one last attempt.',
 'utter_audiostrike3': 'You have exceeded the limit. Better luck next time, Goodbye.',
 'utter_videostrike1': 'Only three attempts are given to complete the document capture. Now you are remained with 2 attempts only.',
 'utter_videostrike2': 'Your remained with one last attempt.',
 'utter_videostrike3': 'You have exceeded the limit. Better luck next time, Goodbye.',
 'utter_confirmcapture': 'Great!! Now we can start your video capturing when you are ready please give confirmation as START or I am READY.',
 'utter_waitconfirmation': 'Ok, When you are ready please give me the confirmation.',
 'utter_interrupt': 'We are in the middle of vKYC verification, if you have any doubt or query please ask after the completion of verification process.',
 'utter_rephrase': 'I can answer you the questions related to video-KYC process only, now try again.',
 'utter_skiprepeate': 'You already have skip one question now please answer the given question.',
 'utter_skipatstart': 'First you have to verify the Aadhaar card',
 'utter_firstaadhaar': 'I already answer the question, please first verify Aadhaar Number.',
 'utter_refuse': 'Alright!, Give me the answer of above Question.',
 'utter_wronginput': 'The input you provided is not Aadhaar Number please check your Aadhaar & try again.',
 'utter_repeateaadhaar': 'You have already given the Aadhaar Number now please answer the given question.',
 'utter_askagain1': 'Should I start your video-KYC process.',
 'utter_askagain2': 'Do you have any doubts ?',
 'utter_verified': 'I already verify you by asking random questions please proceede to face and documents capture by giving confirmation.',
 'utter_requestanswer': 'Please answer given question that mentioned above.',
 'utter_freeask': 'Please free to ask',
 'utter_wrongdoc': 'You are Providing Document please give correct document mentioned above',
 'utter_updateverified': 'Your verification is done. Now you will be directed to the portal to perform the required task you want.',
 'utter_finalMsg': 'Now your session will be closed.Thanks,goodbye.',
 'utter_aadhaarstrike1': 'You have given a wrong Aadhaar number, I need your registered Aadhaar number to proceed. Now please try again. After 3 wrong attempts chatbot will shutdown.',
 'utter_aadhaarstrike2': 'Your remained with one last attempt',
 'utter_aadhaarstrike3': 'You have exceeded the limit. Better luck next time, Goodbye',
 'utter_suggest': "Please answer the given question, If you can't answer this question you can skip this question",
 'utter_middleprocess': 'We are already in the process please answer the given questions.',
 'utter_waitdirecting': 'Please be Petient we redirecting to you portal for further process',
 'utter_completeagain': 'You already complete KYC process, If you have any doubts please ask',
 'utter_waitconfirmation1': 'You already give answer of three questions please give us confirmation so we can proceed further',
 'utter_repeatlimit': 'You Already cross the limit of asking same question please try later.',
 'utter_aboutinfo': 'All information related VKYC process mentioned in the above link please visit the link',
 'utter_angry': "I apologize if my previous explanation didn't meet your expectations or fully address your concern.",
 'utter_requestaadhaar': 'PLease give aadhaar card number',
 'utter_responseAfterLink': 'Hope your satisfied with information. No we will start your VKYC process. Give me your 12-digit aadhaar number.',
 }