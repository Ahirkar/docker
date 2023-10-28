import os
import json
import random
import tempfile
import requests
import threading
import numpy as np
from dbcheck import *
from Constant import *
from gtts import gTTS
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher



intent_list = []
# utter_list = []
count = 0
counter = 0

def random_selection(dict_:dict):
    return random.sample(list(dict_.items()), k = 1)


class ActionWelcomeMsg(Action):
    """
    This class display wellcome Message
    """
    def name(self) -> Text:
        return "action_welcome_msg"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="""Hi Welcome to our vKYC platform, How may I assist you""")
        return []


def text_to_speech(bot_utter:str, **kwargs):

    # generating  temporary file to store the speech output
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        audio_file_path = temp_audio.name
        # Generate the speech output using gTTS
        # tts = gTTS(text=speech_output, lang='en', slow=True)
        utter = bot_utter.format(**kwargs)
        tts = gTTS(utter)
        # tts = gTTS(text=speech_output, lang='hi')
        tts.save(audio_file_path)
        #  get voice o/p
        return os.system(f"ffplay -nodisp -autoexit {audio_file_path}")


class ActionVerifyAadhaar(Action):
    """ This class verify the user by using the Aadhaar card"""
    def name(self) -> Text:
        return "action_verify_aadhaar"
    
    # verify the Aadhaar card
    def aadhaar_verification(self, adhaar:int, intent:Text, dispatcher: CollectingDispatcher):
        global RESPONSES
        global selected
        global count
        # function to verify aadhar number
        if verify_aadhaar(adhaar):
            selected = random_selection(RESPONSES)
            dispatcher.utter_message(response=selected[0][0])
            text_to_speech(BOT_UTTERANCES[selected[0][0]])
            intent_list.append(intent)
            intent_list.append("aadhaar_verified")
            RESPONSES.pop(selected[0][0])
            print(selected)
            count = 0
            return []
        else:
            # TODO
            # after count = 3 chatbot should close
            count += 1
            if count<4:
                # Give warning when Aadhaar Number is wrong
                text_to_speech(BOT_UTTERANCES[WARNING_AADHAAR[count-1]])
                return dispatcher.utter_message(response = WARNING_AADHAAR[count-1])
            # if count == 4:
            #     count -= 1
            #     flag = False
            #     # check whether the Aadhaar Number giving again
            #     return dispatcher.utter_message(response="utter_present", name = intent)   
    # Function for verify Aadhaar Number
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global counter
        global intent_list
        # print(tracker.get_last_event_for("action")["name"])
        # print(tracker.events)
        intent = tracker.get_intent_of_latest_message()
        print(intent)
        print(intent_list)   
        utterance = []
        event = tracker.events
        # to find all bot uterrances
        for evnt in event:
            try:
                if evnt["event"] == "bot":
                    bot_utter = evnt['metadata']["utter_action"]
                    utterance.append(bot_utter)
            except:
                pass
        a = np.random.randint(0, 10)
        if a != 0:
            adhaar = None
            if intent == "Aadhaar Number":
                adhaar = tracker.get_slot("aadhaar number")[0]
            intent = tracker.get_intent_of_latest_message()
        # if user give any input while directing to the portal other than onbording cases
            if "Aadhaar Number" and "completly verified1" in intent_list:
                text_to_speech(BOT_UTTERANCES["utter_waitdirecting"])
                return dispatcher.utter_message(response = "utter_waitdirecting")

            # conversation for update and other use cases
            if intent in USE_CASE or any([element in USE_CASE for element in intent_list]):
                if len(utterance) !=0:
                    if utterance[-1] == "utter_confirmcapture":
                        # to handle if user give aadhaar number during the face and document capturing
                        text_to_speech(BOT_UTTERANCES["utter_confirmcapture1"])
                        return dispatcher.utter_message(response="utter_confirmcapture1")

                    # handle to avoid again restarting the conversation
                    if "Aadhaar Number" in intent_list and intent in USE_CASE:
                        text_to_speech(BOT_UTTERANCES["utter_middleprocess"])
                        return dispatcher.utter_message(response="utter_middleprocess")

                    # if user give again aadhaar nuber after verifying the aadhaar number
                    if "Aadhaar Number" in intent_list:
                        text_to_speech(BOT_UTTERANCES["utter_repeateaadhaar"])
                        return dispatcher.utter_message(response = "utter_repeateaadhaar")
                    # give reply when user want to update or other use cases
                    if adhaar is None:
                        # intent_list.append(intent)
                        text_to_speech(BOT_UTTERANCES["utter_VerifyKyc"])
                        return dispatcher.utter_message(response="utter_VerifyKyc")
                    # aadhaar verification
                    return self.aadhaar_verification(adhaar = adhaar, intent = intent, dispatcher=dispatcher)
                else:
                    if intent in USE_CASE or any([element in USE_CASE for element in intent_list]):
                        if adhaar is None:
                            intent_list.append(intent)
                            text_to_speech(BOT_UTTERANCES["utter_VerifyKyc"])
                            return dispatcher.utter_message(response="utter_VerifyKyc")

            # handle onbording case when user come first time
            if len(utterance) !=0:
                # to handle if user give aadhaar number during the face and document capturing
                if utterance[-1] == "utter_confirmcapture":
                    print("adhaar")
                    text_to_speech(BOT_UTTERANCES["utter_waitconfirmation1"])
                    return dispatcher.utter_message(response="utter_waitconfirmation1")
                # to handle if user give the aadhaar number again after completly verified
                if ("Aadhaar Number" and "completly verified" in intent_list):
                    text_to_speech(BOT_UTTERANCES["utter_completeagain"])
                    return dispatcher.utter_message(response = "utter_completeagain") 
                # avoid conversation restart
                if "Aadhaar Number" in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_repeateaadhaar"])
                    return dispatcher.utter_message(response = "utter_repeateaadhaar")
            return self.aadhaar_verification(adhaar = adhaar, intent = intent, dispatcher=dispatcher)
        else:
            # TODO
            # after counter = 3 chatbot should close
            counter += 1
            if counter < 4:
                # Give warning When user audio is not clear
                text_to_speech(BOT_UTTERANCES[WARNINGS_AUDIO[counter-1]])
                return dispatcher.utter_message(response = WARNINGS_AUDIO[counter-1])
    
class ActionQueSelection(Action):
    """
    This Class provide follwing functionality:
    * Generate random quetion and verify this question by using user input
    * Check audio quality of user
    * Check user should not repeat the answer
    * Give indication to user for starting video capturing Process
    """
    def name(self) -> Text:
        return "action_Que_Selection"
    
    def question_verification(self, user_input, intent, dispatcher: CollectingDispatcher, tracker: Tracker, utterance):
        global selected
        global count
        global intent_list
        # global utter_list
        global RESPONSES
        print(intent_list.count("Repeat Question"))
        # handle ask to repeate question
        if intent == "Repeat Question":
            if "aadhaar_verified" in intent_list:
                # user can repeat questions 3 time only
                if intent_list.count("Repeat Question") <= 2:
                    verify_list = []
                    if len(utterance) !=0:
                        for element in VERIFY_UTTERANCES:
                            if element in set(utterance):
                                verify_list.append(element)
                        intent_list.append(intent)
                        # bot give instruction to user to give aadhaar number
                        text_to_speech(BOT_UTTERANCES[verify_list[-1]])
                        return dispatcher.utter_message(response = verify_list[-1])
                else:
                    # when your limit of asking question is over
                    text_to_speech(BOT_UTTERANCES["utter_repeatlimit"])
                    return dispatcher.utter_message(response="utter_repeatlimit")
            elif len(intent_list) == 0:
                # if the user directly give repeat question input to bot
                text_to_speech(BOT_UTTERANCES["utter_skipatstart"])
                return dispatcher.utter_message(response="utter_skipatstart")
            elif "verified" in intent_list:
                # if the user want change the question after answering the three questions
                print("questionsel2")
                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation1"])
                return dispatcher.utter_message(response="utter_waitconfirmation1")
            else:
                # if the user want change the question after completing KYC process
                text_to_speech(BOT_UTTERANCES["utter_completeagain"])
                return dispatcher.utter_message(response="utter_completeagain")
            
        # when user give verify intent without verifying the aadhaar number            
        if "Aadhaar Number" not in intent_list and intent in VERIFY_INTENT:
            text_to_speech(BOT_UTTERANCES["utter_wronginput"])
            return dispatcher.utter_message(response = "utter_wronginput")
    
        common = set(intent_list) & set(VERIFY_INTENT)
        # counter for verification questions
        if len(common) < 3:
            slot_name = selected[0][0].split("_")
            message = tracker.get_slot(slot_name[1])
            print(message)
            if message is not None:
                message = tracker.get_slot(slot_name[1])[0]
                print({"message":message})
            # function for verification of random question
            if len(common) < 2:
                if selected[0][1](message = message, user_input = user_input):
                    # Remove the latest selected question to avoid the repeatation
                    intent_list.append(intent)
                    selected = random_selection(RESPONSES)
                    text_to_speech(BOT_UTTERANCES[selected[0][0]])
                    dispatcher.utter_message(response=selected[0][0])
                    RESPONSES.pop(selected[0][0])
                    # utter_list.append(slot_name[1])
                    return []
                else:
                    count += 1
                    # TODO
                    # after count = 3 chatbot should close
                    if count < 4:
                        # Give warning when user give incorrect input OR give Wrong answer
                        text_to_speech(BOT_UTTERANCES[STRIKE[count-1]], name = slot_name[1])
                        return dispatcher.utter_message(response=STRIKE[count-1], name = slot_name[1])
            else:
                intent_list.append("verified")
                count = 0
                # Waiting for the user confirmation to start capturing
                text_to_speech(BOT_UTTERANCES["utter_confirmcapture"])
                return dispatcher.utter_message(response = "utter_confirmcapture")
    
        else:
            # when user want ask repeat question after three questions
            text_to_speech(BOT_UTTERANCES["utter_verified"])
            return dispatcher.utter_message(response = "utter_verified")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global counter
        user_input = tracker.latest_message["text"]
        intent = tracker.get_intent_of_latest_message()
        print(intent)
        utterance = []
        event = tracker.events
        for evnt in event:
            try:
                if evnt["event"] == "bot":
                    bot_utter = evnt['metadata']["utter_action"]
                    utterance.append(bot_utter)
            except:
                pass
        print({"ans":utterance})
        if len(utterance) !=0:
            if  utterance[-1] == "utter_confirmcapture":
                # when user give input to bot from verified question
                print("questionsel1")
                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation1"])
                return dispatcher.utter_message(response="utter_waitconfirmation1")
        # if any(USE_CASE in intent_list):
        a = np.random.randint(0, 10)
        if a != 0:
            # to handle Update and other use cases
            user_input = tracker.latest_message["text"]
            intent = tracker.get_intent_of_latest_message()
            if any([element in USE_CASE for element in intent_list]):
                return self.question_verification(
                    user_input= user_input,
                    intent= intent,
                    dispatcher=dispatcher,
                    tracker=tracker,
                    utterance = utterance
                    )
            else:
                # handle onboarding case
                return self.question_verification(
                    user_input= user_input,
                    intent= intent,
                    dispatcher=dispatcher,
                    tracker=tracker,
                    utterance = utterance
                    )  
        else:
            counter += 1
            # TODO
            # after counter = 3 chatbot should close
            if counter < 4:
                text_to_speech(BOT_UTTERANCES[WARNINGS_AUDIO[counter-1]])
                return dispatcher.utter_message(response = WARNINGS_AUDIO[counter-1])  
        # return []


    
class ActionFAQ(Action):
    """
    This Class provide following functionality:
    * Answer the quesries related to the VKYC Process
    * Make sure user sould not allowed to answer question in middle of verification
    * Reply to the question which not understand to bot
    """
    def name(self):
        return "action_FAQ"

    # function for answer the queries and doubts related VKYC process
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global intent_list
            global counter
            last_action = tracker.latest_action_name
            print(last_action)
            utterance = []
            event = tracker.events
            intent = tracker.get_intent_of_latest_message()
            print(intent)
            for evnt in event:
                try:
                    if evnt["event"] == "bot":
                        bot_utter = evnt['metadata']["utter_action"]
                        utterance.append(bot_utter)
                        print(utterance)
                except:
                    pass
            a = np.random.randint(0, 10)
            if a != 0:
                intent = tracker.get_intent_of_latest_message()
                intent_list.append(intent)
                if utterance.count("utter_feedback") >= 3:
                # providing link to user when it not satisfied with explaination
                    text_to_speech(BOT_UTTERANCES["utter_ReplyToAnswer2A"])
                    dispatcher.utter_message(response = "utter_ReplyToAnswer2A")
                    dispatcher.utter_message(response = "utter_ReplyToAnswer2B")
    
                    if "completly verified" in intent_list:
                        text_to_speech(BOT_UTTERANCES["utter_finalMsg"])
                        return dispatcher.utter_message(response = "utter_finalMsg")
                    if "completly verified" not in intent_list:
                        text_to_speech(BOT_UTTERANCES["utter_responseAfterLink"])
                        return dispatcher.utter_message(response = "utter_responseAfterLink")
                    

                if "completly verified" in intent_list:
                    if intent in list(FAQ.keys()):
                        if intent != "greet":
                            text_to_speech(BOT_UTTERANCES[FAQ[intent]])
                            dispatcher.utter_message(response=FAQ[intent])
                            # asking user if he/she satisfied with explaination
                            text_to_speech(BOT_UTTERANCES["utter_feedback"])
                            dispatcher.utter_message(response = "utter_feedback")
                            return[]
                        elif intent == "greet":
                            # greeting message reply
                            text_to_speech(BOT_UTTERANCES[FAQ[intent]])
                            return dispatcher.utter_message(response=FAQ[intent])
                    else:
                    # Give reply when bot not understand the user intention
                        text_to_speech(BOT_UTTERANCES["utter_rephrase"])
                        return dispatcher.utter_message(response = "utter_rephrase")
                
                if "aadhaar_verified" in intent_list or "verified" in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_interrupt"])
                    return  dispatcher.utter_message(response = "utter_interrupt")
            # for item in ["action_Que_Selection", "action_verify_aadhaar", "action_skip_question"]:
            #     if tracker.last_executed_action_has(name = item, skip = 1):

                if len(utterance) !=0:
                    if utterance[-1] == "utter_confirmcapture":
                        text_to_speech(BOT_UTTERANCES["utter_interrupt"])
                        return dispatcher.utter_message(response = "utter_interrupt")
                # for answer the questions related to KYC process
                if intent in list(FAQ.keys()):
                    if intent != "greet":
                        text_to_speech(BOT_UTTERANCES[FAQ[intent]])
                        dispatcher.utter_message(response=FAQ[intent])
                        text_to_speech(BOT_UTTERANCES["utter_feedback"])
                        dispatcher.utter_message(response = "utter_feedback")
                    elif intent == "greet":
                        text_to_speech(BOT_UTTERANCES[FAQ[intent]])
                        return dispatcher.utter_message(response=FAQ[intent])
                else:
                    # Give reply when bot not understand the user intention
                    text_to_speech(BOT_UTTERANCES["utter_rephrase"])
                    return dispatcher.utter_message(response = "utter_rephrase")
            else:
                counter += 1
                #TODO
                # bot should close after counter = 3
                if counter < 4:
                    text_to_speech(BOT_UTTERANCES[WARNINGS_AUDIO[counter-1]])
                    dispatcher.utter_message(response = WARNINGS_AUDIO[counter-1])

    
class ActionSkipQuestion(Action):
    """
    This class use to skip only one question
    """
    def name(self) -> Text:
        return "action_skip_question"
    def skip_que(self, dispatcher: CollectingDispatcher, tracker: Tracker):
        global RESPONSES
        global selected
        global intent_list
        intent = tracker.get_intent_of_latest_message()
        utterance = []
        event = tracker.events
        for evnt in event:  
            if evnt["event"] == "bot":
                try:
                    bot_utter = evnt['metadata']["utter_action"]
                    utterance.append(bot_utter)
                except:
                    pass
                    # return dispatcher.utter_message(response = "utter_firstaadhaar")
        print({"skip":utterance})
        if len(utterance) !=0:
            if  utterance[-1] == "utter_confirmcapture":
                # when user want skip after giving answer of three questions
                print("skip_quesstions")
                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation1"])
                return dispatcher.utter_message(response="utter_waitconfirmation1")
        
            if "utter_warn" in utterance:
                # when user want skip question more than one time
                text_to_speech(BOT_UTTERANCES["utter_skiprepeate"])
                return dispatcher.utter_message(response = "utter_skiprepeate")
        
        if "Aadhaar Number" not in intent_list:
                # when user want to skip question without verification of aadhaar card
                text_to_speech(BOT_UTTERANCES["utter_skipatstart"])
                return dispatcher.utter_message(response = "utter_skipatstart")
        else:
            # to skip only one question
            intent_list.append(intent)
            selected = random_selection(RESPONSES)
            text_to_speech(BOT_UTTERANCES["utter_warn"])
            dispatcher.utter_message(response = "utter_warn")
            text_to_speech(BOT_UTTERANCES[selected[0][0]])
            dispatcher.utter_message(response=selected[0][0])
            RESPONSES.pop(selected[0][0])
            return []
            # when user refuse to skip question
            
    # Function to skip one question
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global counter
        intent = tracker.get_intent_of_latest_message()
        print(intent)
        a = np.random.randint(0, 10)
        if a != 0:
            # to handl skip one question
            return self.skip_que(dispatcher=dispatcher, tracker=tracker)
        else:
            counter += 1
            # TODO
            # after counter = 3 chatbot should close
            if counter < 4:
                text_to_speech(BOT_UTTERANCES[WARNINGS_AUDIO[counter-1]])
                return dispatcher.utter_message(response = WARNINGS_AUDIO[counter-1])


class VideoEvaluationAction(Action):
    """
    This Class have Following Functionality:
    * Check the video quality for document verification and face capturing
    * capturing documents
    * Proper confirmation and not confirmation reply for various input of user
    """
    def name(self) -> Text:
        return "action_video_capture"
    # this method handle the multiple confirmation and refusal 
    def video_confirmation(self, dispatcher:CollectingDispatcher, tracker:Tracker, utterance:list):

        intent = tracker.get_intent_of_latest_message()
        global intent_list

        # this give proper reply on various confirmation
        if len(utterance) !=0:
            # if utterance[-1] == "utter_askagain1" and intent == "Notconfirm":
            #     return dispatcher.utter_message(response = "")
            # if user want more information about VKYC process
            #TODO
            if intent == "More Info":
                text_to_speech(BOT_UTTERANCES["utter_ReplyToAnswer2A"])
                dispatcher.utter_message(response = "utter_ReplyToAnswer2A")
                dispatcher.utter_message(response = "utter_ReplyToAnswer2B")
    
                if "completly verified" in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_finalMsg"])
                    return dispatcher.utter_message(response = "utter_finalMsg")
                if "completly verified" not in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_responseAfterLink"])
                    return dispatcher.utter_message(response = "utter_responseAfterLink")
                
            if utterance.count("utter_feedback") >= 3:
                # providing link to user when it not satisfied with explaination
                text_to_speech(BOT_UTTERANCES["utter_ReplyToAnswer2A"])
                dispatcher.utter_message(response = "utter_ReplyToAnswer2A")
                dispatcher.utter_message(response = "utter_ReplyToAnswer2B")
    
                if "completly verified" in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_finalMsg"])
                    return dispatcher.utter_message(response = "utter_finalMsg")
                if "completly verified" not in intent_list:
                    text_to_speech(BOT_UTTERANCES["utter_responseAfterLink"])
                    return dispatcher.utter_message(response = "utter_responseAfterLink")
            # when user give reply to audio warning
            if utterance[-1] in WARNINGS_AUDIO:
                if ["aadhaar_verified", "verified"] in intent_list and (intent == "Notconfirm" or intent == "confirm"):
                    text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                    return dispatcher.utter_message(response = "utter_requestanswer")
                if not any(item in intent_list for item in ["verified", "completly verified", "aadhaar_verified"]) or "completly verified" in intent_list:
                    if len(utterance) < 3 and (utterance[-1] in WARNINGS_AUDIO or utterance[-2] in WARNINGS_AUDIO) :
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response = "utter_Notconfirm")                        
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response = "utter_confirm")
                        
                    if (utterance[-2] == "utter_feedback" or utterance[-3] == "utter_feedback") and utterance[-1] in WARNINGS_AUDIO:
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response = "utter_Notconfirm")
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_exit"])
                            dispatcher.utter_message(response="utter_exit")
                            if "completly verified" not in intent_list:
                                text_to_speech(BOT_UTTERANCES["utter_confirm"])
                                return dispatcher.utter_message(response = "utter_confirm")
                    
                    if (utterance[-2] == "utter_greet" or utterance[-3] == "utter_greet") and utterance[-1] in WARNINGS_AUDIO:
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response="utter_confirm")
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response="utter_Notconfirm")    
                        
                    if utterance[-1] in WARNINGS_AUDIO and "aadhaar_verified" in intent_list:
                        text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                        return dispatcher.utter_message(response= "utter_requestanswer")
                    
                    if (utterance[-2] == "utter_askagain1" or utterance[-3] == "utter_askagain1") and utterance[-1] in WARNINGS_AUDIO:
                    # if utterance[-2] == "utter_askagain1" or utterance[-3] in WARNINGS_AUDIO:
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response= "utter_confirm")
                        
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response= "utter_Notconfirm")
                    
                        
                    if (utterance[-2] == "utter_askagain2" or utterance[-3] == "utter_askagain2") and utterance[-1] in WARNINGS_AUDIO:
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response= "utter_Notconfirm")
                        
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["finalMsg"])
                            return dispatcher.utter_message(response= "finalMsg")
                        
                    if utterance[-2] == "utter_confirm":
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response= "utter_requestaadhaar")
                        
                        if intent == "Notconfirm":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response= "utter_Notconfirm")


                    
            # when user give reply to the when bot give warning to user of limit of skip question
            if utterance[-1] == "utter_skiprepeate" and (intent == "confirm" or intent == "Notconfirm"):
                text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                return dispatcher.utter_message(response = "utter_requestanswer")
            # when user give reply to bot when bot request to answer the question
            if utterance[-1] == "utter_requestanswer": 
                if intent == "confirm" or intent == "Notconfirm":
                    text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                    return dispatcher.utter_message(response = "utter_requestanswer")
                if intent == "Doubts":
                    text_to_speech(BOT_UTTERANCES["utter_interrupt"])
                    return dispatcher.utter_message(response = "utter_interrupt")
            # when user give reply to bot when request answer given question
            if utterance[-1] in VERIFY_UTTERANCES and intent == "confirm":
                text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                return dispatcher.utter_message(response = "utter_requestanswer")
    
            if utterance[-1] in VERIFY_UTTERANCES:
                if intent == "Notconfirm":
                    text_to_speech(BOT_UTTERANCES["utter_suggest"])
                    return dispatcher.utter_message(response = "utter_suggest")
                if intent == "Doubts":
                    text_to_speech(BOT_UTTERANCES["utter_interrupt"])
                    return dispatcher.utter_message(response = "utter_interrupt")
            
            # check last and fourth last utterances are same of not
            # def check_element(lst):
            #     try:
            #         if lst[-1] == lst[-4]:
            #             return True
            #     except:
            #         return False
                
            #TODO
            # if utterance.count("utter_feedback") >= 3:
            #     # providing link to user when it not satisfied with explaination
            #     text_to_speech(BOT_UTTERANCES["utter_ReplyToAnswer2A"])
            #     dispatcher.utter_message(response = "utter_ReplyToAnswer2A")
            #     dispatcher.utter_message(response = "utter_ReplyToAnswer2B")
    
            #     if "completly verified" in intent_list:
            #         text_to_speech(BOT_UTTERANCES["utter_finalMsg"])
            #         return dispatcher.utter_message(response = "utter_finalMsg")
            #     if "completly verified" not in intent_list:
            #         text_to_speech(BOT_UTTERANCES["utter_confirm"])
            #         return dispatcher.utter_message(response = "utter_responseAfterLink")
            
            if utterance[-1]=="utter_feedback":
                if intent == "confirm":
                    text_to_speech(BOT_UTTERANCES["utter_exit"])
                    dispatcher.utter_message(response = "utter_exit")
                    if "verified" not in intent_list:
                        if "completly verified" not in intent_list:
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response = "utter_confirm")
                        return
                        
                    if " completly verified" not in intent_list:
                        if "verified" not in intent_list:
                            text_to_speech(BOT_UTTERANCES["utter_askagain1"])
                            return dispatcher.utter_message(response = "utter_askagain1")
                        return

                if intent =="Notconfirm" or intent == "Doubts":
                    return dispatcher.utter_message(response = "utter_Notconfirm")

            # when user reply to bot if he/she have any doubts
            if utterance[-1] == "utter_askagain2" and intent == "Notconfirm":
                text_to_speech(BOT_UTTERANCES["utter_exit"])
                return dispatcher.utter_message(response = "utter_exit")
            
            if utterance[-1] == "utter_askagain2" and intent == "Doubts":
                text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                return dispatcher.utter_message(response = "utter_Notconfirm")
            

            if utterance[-1] == "utter_askagain2" and intent == "confirm":
                text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                return dispatcher.utter_message(response = "utter_Notconfirm")
            
            if utterance[-1] == "utter_askagain1" or utterance[-1] == "utter_greet":
                if intent == "confirm":
                    text_to_speech(BOT_UTTERANCES["utter_confirm"])
                    return dispatcher.utter_message(response = "utter_confirm")
                
                if intent == "Notconfirm":
                    text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                    return dispatcher.utter_message(response = "utter_Notconfirm")

            # when user not ready or asking any Doubts while capturing the documents and face
            if utterance[-1] == "utter_confirmcapture":
                if intent == "Notconfirm":
                    text_to_speech(BOT_UTTERANCES["utter_waitconfirmation"])
                    return  dispatcher.utter_message(response = "utter_waitconfirmation")
                if intent == "Doubts":
                    text_to_speech(BOT_UTTERANCES["utter_interrupt"])
                    return dispatcher.utter_message(response = "utter_interrupt")
            
            # when user give reply to the interruption during verifcation
            for item in ["action_Que_Selection", "action_verify_aadhaar", "action_skip_question"]:
                if tracker.last_executed_action_has(name = item, skip = 1) and\
                    utterance[-1] == "utter_interrupt" and (intent == "confirm" or intent == "Notconfirm"):
                    text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                    return dispatcher.utter_message(response = "utter_requestanswer")
            # when user reply iterruption while video capturing 
            if utterance[-1] == "utter_interrupt" and "verified" not in intent_list:
                text_to_speech(BOT_UTTERANCES["utter_requestanswer"])
                return dispatcher.utter_message(response="utter_requestanswer")
            
            if utterance[-1] == "utter_Notconfirm":
                if intent == "confirm":
                    text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                    return dispatcher.utter_message(response = "utter_Notconfirm")
                
                if intent == "Notconfirm":
                    if "completly verified" not in intent_list:
                        text_to_speech(BOT_UTTERANCES["utter_askagain1"])
                        return dispatcher.utter_message(response = "utter_askagain1")
                    text_to_speech(BOT_UTTERANCES["utter_finalMsg"])
                    return dispatcher.utter_message(response = "utter_finalMsg")
        else:
            if intent == "Notconfirm":
                text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                return dispatcher.utter_message(response="utter_Notconfirm")
            if intent == "confirm":
                text_to_speech(BOT_UTTERANCES["utter_confirm"])
                return dispatcher.utter_message(response="utter_confirm")


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global count
        global counter
        global intent_list
        utterance = []
        event = tracker.events
        intent = tracker.get_intent_of_latest_message()
        print(intent)
        for evnt in event:
            try:
                if evnt["event"] == "bot":
                    bot_utter = evnt['metadata']["utter_action"]
                    utterance.append(bot_utter)
            except:
                pass
        a = np.random.randint(0, 10)
        b = np.random.randint(0, 10)
        if b != 0:
            intent = tracker.get_intent_of_latest_message()
            #  handle video capture Update and other use cases
            if any(element in USE_CASE for element in intent_list):
                # give confirmation by user to start capturing face and documents
                if (utterance[-1] in CAP_CONFIRMATION) and intent == "confirm":
                    if a != 0:
                        text_to_speech(BOT_UTTERANCES["utter_facecapture"])
                        dispatcher.utter_message(response="utter_facecapture")
                    text_to_speech(BOT_UTTERANCES["utter_updateverified"])
                    dispatcher.utter_message(response="utter_updateverified")
                    intent_list.append("completly verified1")
                    return []
                # give denial by user to start capturing face and documents
                if (utterance[-1] in CAP_CONFIRMATION) and intent == "Notconfirm":
                    text_to_speech(BOT_UTTERANCES["utter_waitconfirmation"])
                    return dispatcher.utter_message(response = "utter_waitconfirmation")
                return self.video_confirmation(dispatcher = dispatcher, tracker = tracker, utterance = utterance)
        
            # elif ((len(utterance) == 0) or (utterance[-1] == "utter_greet" and (intent == "confirm" or intent == "confirm")) or \
            #     ((utterance[-1] == "utter_askagain1" and (intent == "confrom" or intent == "confirm"))) or\
            #     ((("aadhaar_verified" not in intent_list) and (intent == "confirm" or intent == "Notconfirm")) and \
            #     (("verified" not in intent_list) and (intent == "confirm" or intent == "Notconfirm")) and \
            #     (("completly verified" not in intent_list) and (intent == "confirm" or intent == "confirm")))):
            elif len(utterance) == 0 or utterance[-1] == "utter_greet" or utterance[-1] == "utter_askagain1" or\
                (not any(item in intent_list for item in ["verified", "completly verified", "aadhaar_verified"])):

                if len(utterance) != 0:    
                    if utterance[-1] == "utter_greet":
                        # bot reply when user not ready or he/she have doubts 
                        if intent == "Notconfirm" or intent == "Doubts":
                            text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                            return dispatcher.utter_message(response = "utter_Notconfirm")
                        # when user give conformation to start VKYC process
                        if intent == "confirm":
                            text_to_speech(BOT_UTTERANCES["utter_confirm"])
                            return dispatcher.utter_message(response = "utter_confirm")
                # user request to start vkyc process
                if intent == "Start KYC":
                    text_to_speech(BOT_UTTERANCES["utter_confirm"])
                    return dispatcher.utter_message(response="utter_confirm")
                # if user have some doubts 
                if intent == "Doubts":
                    print({"not ok":utterance})
                    text_to_speech(BOT_UTTERANCES["utter_Notconfirm"])
                    return dispatcher.utter_message(response="utter_Notconfirm")
                return self.video_confirmation(dispatcher = dispatcher, tracker = tracker, utterance = utterance)

            else:
                # handling conversation while capture face and documentation
                print(intent_list)
                print(utterance)
                if (utterance[-1] in CAP_CONFIRMATION) and (intent == "confirm" or intent == "Notconfirm") and\
                    ("completly verified" not in intent_list) and ("verified" in intent_list):
                    if a!=0: # video quality check
                        # when aadhaar card is completly verified
                        if "aadhar card verified" in intent_list:
                            condition = True # if documents are correct
                            if intent == "confirm":
                                document = requests.get(
                                    url = "http://127.0.0.1:5006/document_type",
                                    json = {"data_path": "https://amitnew.s3.amazonaws.com/pancard/1.jpg"}
                                )
                                document_type = json.loads(document.text)
                                if document_type['document_type'] == 'PANCARD':
                                #if condition:
                                    intent_list.append("completly verified")
                                    intent_list.remove("aadhar card verified")
                                    backendapicall = threading.Thread(target=task)
                                    backendapicall.start()
                                    # give reply when capturing of pan card is done and successfull of KYC process
                                    text_to_speech(BOT_UTTERANCES["utter_doneSC"])
                                    dispatcher.utter_message(response = "utter_doneSC") # when pan card is done
                                    # after completion of KYC process bot ask if he/she have any doubts
                                    text_to_speech(BOT_UTTERANCES["utter_askagain2"])
                                    dispatcher.utter_message(response = "utter_askagain2")
                                    intent_list.remove("aadhaar_verified")
                                    intent_list.remove("verified")
                                else:
                                    # when user give wrong documents
                                    text_to_speech(BOT_UTTERANCES["utter_wrongdoc"])
                                    return dispatcher.utter_message(response = "utter_wrongdoc")
                            if intent == "Notconfirm":
                                # when user not ready for capturing
                                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation"])
                                return dispatcher.utter_message(response = "utter_waitconfirmation")
                        elif "face verified" in intent_list:
                            condition = True # if documents are correct
                            if intent == "confirm":
                                document = requests.get(
                                    url = "http://127.0.0.1:5006/document_type",
                                    json = {"data_path": "https://amitnew.s3.amazonaws.com/aadhar/1.jpg"}
                                )
                                document_type = json.loads(document.text)
                                if document_type['document_type'] == 'AADHARCARD':
                                #if condition:
                                    intent_list.append("aadhar card verified")
                                    intent_list.remove("face verified")
                                    # confirming successfull capture of aadhar and ask for pan card
                                    text_to_speech(BOT_UTTERANCES["utter_acdn"])
                                    return dispatcher.utter_message(response = "utter_acdn") # when aadhaar card is done
                                else:
                                    # when user give wrong documents
                                    text_to_speech(BOT_UTTERANCES["utter_wrongdoc"])
                                    return dispatcher.utter_message(response = "utter_wrongdoc")
                            if intent == "Notconfirm":
                                # when user not ready for capturing
                                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation"])
                                return dispatcher.utter_message(response = "utter_waitconfirmation")
                        else :
                            #TODO
                            condition = True # when face quality is good
                            if intent == "confirm":
                                if condition:
                                    # when face capture successfully and ask for aadhaar card
                                    intent_list.append("face verified") # when face is done
                                    text_to_speech(BOT_UTTERANCES["utter_fcdone"])
                                    return dispatcher.utter_message(response = "utter_fcdone")
                                else:
                                    # when
                                    text_to_speech(BOT_UTTERANCES["utter_FvideoQNG"]) 
                                    dispatcher.utter_message(response="utter_FvideoQNG")
                            if intent == "Notconfirm":
                                # when user not ready for capturing
                                text_to_speech(BOT_UTTERANCES["utter_waitconfirmation"]) 
                                return dispatcher.utter_message(response = "utter_waitconfirmation")
                    else:
                        # when video quality is not good
                        if "aadhar card verified" in intent_list:
                            text_to_speech(BOT_UTTERANCES["utter_PvideoQng"])
                            dispatcher.utter_message(response="utter_PvideoQng")
                            count+=1
                            # TODO
                            # after count = 3 chatbot should close
                            if count < 4:
                                text_to_speech(BOT_UTTERANCES[WARNINGS_VIDEO[count-1]])
                                return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])
                        if "face verified" in intent_list:
                            text_to_speech(BOT_UTTERANCES["utter_Avideoqng"])
                            dispatcher.utter_message(response="utter_Avideoqng")
                            count+=1
                            # TODO
                            # after count = 3 chatbot should close
                            if count < 4:
                                text_to_speech(BOT_UTTERANCES[WARNINGS_VIDEO[count-1]])
                                return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])
                        if "verified" in intent_list:
                            text_to_speech(BOT_UTTERANCES[WARNINGS_VIDEO[count-1]])
                            dispatcher.utter_message(response="utter_FvideoQNG")
                            count+=1
                            # TODO
                            # after count = 3 chatbot should close
                            if count < 4:
                                text_to_speech(BOT_UTTERANCES[WARNINGS_VIDEO[count-1]])
                                return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])
                        else:
                            count+=1
                            # TODO
                            # after counter = 3 chatbot should close
                            if count < 4:
                                text_to_speech(BOT_UTTERANCES[WARNINGS_VIDEO[count-1]])
                                return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])
                else:
                    # various reply for different confirmation
                    return self.video_confirmation(dispatcher = dispatcher, tracker = tracker, utterance = utterance)
        else:
                # when audio quality in not good
            counter += 1
            # TODO
            # after counter = 3 chatbot should close
            if counter < 4:
                text_to_speech(BOT_UTTERANCES[WARNINGS_AUDIO[counter-1]])
                return dispatcher.utter_message(response = WARNINGS_AUDIO[counter-1])


                

                # condition = True # if documents are correct

                #     # a dummy function for video quality check if a = 0 not good quality else good quality
                #     if a == 0:
                #         #TODO
                #     # when face quality is not good
                #         dispatcher.utter_message(response="utter_FvideoQNG")
                #         count += 1
                #         # provide warning related to video issues
                #         return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  
                #     else:
                #         # when quality good will capture face
                #         dispatcher.utter_message(response="utter_fcdone")
                #         # a dummy function for video quality check if a = 0 not good quality else good quality
                #         a = np.random.randint(0, 10)
                #         if a == 0:
                #             #TODO
                #             # when aadhaar card quality not good
                #             dispatcher.utter_message(response="utter_Avideoqng")
                #             count += 1
                #             # provide warning related to video issues
                #             return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  
                #         else:
                #             # when quality of aadhaar card is good and correct Document
                #             condition = True # dummy fuction for check correct document
                #             if condition:
                #                 dispatcher.utter_message(response="utter_acdn")
                #             else:
                #                 #when you providing wrong document
                #                 dispatcher.utter_message(response = "utter_wrongdoc")
                #         # a dummy function for video quality check if a = 0 not good quality else good quality
                #         a = np.random.randint(0, 10)
                #         if a == 0:
                #             #TODO
                #             # when Pan Card video quality is not good
                #             dispatcher.utter_message(response="utter_PvideoQng")
                #             count += 1
                #             # provide warning related to video issues
                #             return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  
                #         else:
                #             condition = True # dummy fuction for check correct document
                #             if condition:
                #                 intent_list.append("completly verified")
                #                 try:
                #                     intent_list.remove("verified")
                #                     intent_list.remove("aadhaar_verified")
                #                 except:
                #                     pass
                #                 # when Pan Card quality is good and document is correct
                #                 dispatcher.utter_message(response="utter_doneSC")
                #                 # after completion of KYC proces if user have any Doubts
                #                 dispatcher.utter_message(response = "utter_askagain2")
                #             else:
                #                 #when you providing wrong document
                #                 dispatcher.utter_message(response = "utter_wrongdoc")
                #             return


# class VideoEvaluationAction(Action):
#     """
#     This Class have Following Functionality:
#     * Check the video quality for document verification and face capturing
#     * capturing documents
#     * Proper confirmation and not confirmation reply for various input of user
#     """
#     def name(self) -> Text:
#         return "action_video_capture"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         global count
#         global intent_list
#         intent = tracker.get_intent_of_latest_message()
#         intent_list.append(intent)
#         utterance = []
#         event = tracker.events
#         print(intent)
#         for evnt in event:
#             try:
#                 if evnt["event"] == "bot":
#                     bot_utter = evnt['metadata']["utter_action"]
#                     utterance.append(bot_utter)
#             except:
#                 pass
#         # this give proper reply on various confirmation
#         if len(utterance) !=0:
#             if utterance[-1] in WARNINGS_AUDIO and (intent == "confirm" or intent == "Notconfirm"):
#                 return dispatcher.utter_message(response = "utter_requestanswer")
            
#             if utterance[-1] == "utter_skiprepeate" and (intent == "confirm" or intent == "Notconfirm"):
#                 return dispatcher.utter_message(response = "utter_requestanswer")
            
#             if utterance[-1] == "utter_requestanswer" and (intent == "confirm" or intent == "Notconfirm"):
#                 return dispatcher.utter_message(response = "utter_requestanswer")
            
#             if utterance[-1] in VERIFY_UTTERANCES and intent == "confirm":
#                 return dispatcher.utter_message(response = "utter_requestanswer")
            
#             if utterance[-1] in VERIFY_UTTERANCES and intent == "Notconfirm":
#                 return dispatcher.utter_message(response = "utter_suggest")
            
#             # if utterance[-1] == "utter_ReplyToAnswer1" and intent == "Notconfirm":
#             #     dispatcher.utter_message(response= "utter_Thanks")
#             #     if "verified" not in intent_list:
#             #         dispatcher.utter_message(response= "utter_askagain1")
#             #     return []
#             if utterance[-1] == "utter_feedback" and intent == "confirm":
#                 dispatcher.utter_message(response = "utter_ReplyToAnswer1")
#                 if "verified" not in intent_list:
#                      dispatcher.utter_message(response= "utter_askagain1")
#                 return []
            
#             if utterance[-1] == "utter_askagain2" and intent == "Notconfirm":
#                 return dispatcher.utter_message(response = "utter_exit")

#             if utterance[-1] == "utter_askagain2" and intent == "confirm":
#                 return dispatcher.utter_message(response = "utter_Notconfirm")

#             # if utterance[-1] == "utter_ReplyToAnswer1" and intent == "confirm":
#             #     return dispatcher.utter_message(response = "utter_freeask")
#             print({"before":utterance})
#             def check_element_after_two_at_end(lst):
#                 try:
#                     if lst[-1] == lst[-4]:
#                         return True
#                 except:
#                     return False
#             # if utterance[-1] == "utter_feedback" and intent_list[-1] == "Notconfirm" and intent_list[-2] == "Notconfirm":
#             if (check_element_after_two_at_end(utterance) and utterance[-1] == "utter_feedback") and intent == "Notconfirm":
#                 print("ok")

#                 dispatcher.utter_message(response = "utter_ReplyToAnswer2A")
#                 dispatcher.utter_message(response = "utter_ReplyToAnswer2B")
#                 if "verified" in intent_list:
#                     return dispatcher.utter_message(response = "utter_finalMsg")

#                 if "verified" not in intent_list:
#                     return dispatcher.utter_message(response = "utter_askagain1")
#                 return[]

#             if utterance[-1] == "utter_feedback" and intent == "Notconfirm":
#                 dispatcher.utter_message(response = "utter_Notconfirm")
#                 return []
            
#             if utterance[-1] == "utter_confirmcapture" and intent == "Notconfirm":
#                 return  dispatcher.utter_message(response = "utter_waitconfirmation")
            
#             for item in ["action_Que_Selection", "action_verify_aadhaar", "action_skip_question"]:
#                 if tracker.last_executed_action_has(name = item, skip = 1) and utterance[-1] == "utter_interrupt" and (intent == "confirm" or intent == "Notconfirm"):
#                     return dispatcher.utter_message(response = "utter_requestanswer")
                
#             if utterance[-1] == "utter_interrupt" and "verified" not in intent_list:
#                 return dispatcher.utter_message(response="utter_requestanswer")
            
#             CAP_confirmATION = ["utter_confirmcapture", "utter_waitconfirmation", "utter_interrupt", "utter_waitconfirmation1"]
#             if not any(element in USE_CASE for element in intent_list):
                
#                 if (utterance[-1] in CAP_confirmATION) and intent == "confirm":
#                     dispatcher.utter_message(response="utter_facecapture")
#                     # a dummy function for video quality check if a = 0 not good quality else good quality
#                     a = np.random.randint(0, 10)
#                     if a == 0:
#                         #TODO
#                     # when face quality is not good
#                         dispatcher.utter_message(response="utter_FvideoQNG")
#                         count += 1
#                         # provide warning related to video issues
#                         return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  

#                     else:
#                         # when quality good will capture face
#                         dispatcher.utter_message(response="utter_fcdone")
#                         # a dummy function for video quality check if a = 0 not good quality else good quality
#                         a = np.random.randint(0, 10)
#                         if a == 0:
#                             #TODO
#                             # when aadhaar card quality not good
#                             dispatcher.utter_message(response="utter_Avideoqng")
#                             count += 1
#                             # provide warning related to video issues
#                             return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  
#                         else:
#                             # when quality of aadhaar card is good and correct Document
#                             condition = True # dummy fuction for check correct document
#                             if condition:
#                                 dispatcher.utter_message(response="utter_acdn")
#                             else:
#                                 #when you providing wrong document
#                                 dispatcher.utter_message(response = "utter_wrongdoc")
#                         # a dummy function for video quality check if a = 0 not good quality else good quality
#                         a = np.random.randint(0, 10)
#                         if a == 0:
#                             #TODO
#                             # when Pan Card video quality is not good
#                             dispatcher.utter_message(response="utter_PvideoQng")
#                             count += 1
#                             # provide warning related to video issues
#                             return dispatcher.utter_message(response = WARNINGS_VIDEO[count-1])  
#                         else:
#                             condition = True # dummy fuction for check correct document
#                             if condition:
#                                 intent_list.append("completly verified")
#                                 try:
#                                     intent_list.remove("verified")
#                                     intent_list.remove("aadhaar_verified")
#                                 except:
#                                     pass
#                                 # when Pan Card quality is good and document is correct
#                                 dispatcher.utter_message(response="utter_doneSC")
#                                 # after completion of KYC proces if user have any Doubts
#                                 dispatcher.utter_message(response = "utter_askagain2")
#                             else:
#                                 #when you providing wrong document
#                                 dispatcher.utter_message(response = "utter_wrongdoc")
#                             return
#             else:
                
#                 if (utterance[-1] in CAP_confirmATION ) and intent == "confirm":
#                     dispatcher.utter_message(response="utter_facecapture")
#                     dispatcher.utter_message(response="utter_updateverified")
#                     intent_list.append("completly verified1")
#                     return []
#                 # try:
#                 #     intent_list.remove("verified")
#                 #     intent_list.remove("aadhaar_verified")
#                 # except:
#                 #     pass
#                 #     return[]
#                 # return []
        
#         if intent == "confirm":
#             return dispatcher.utter_message(response="utter_confirm")

#         if intent == "Notconfirm":
#             print(utterance)
#             return dispatcher.utter_message(response="utter_Notconfirm")


# class TextToSpeech(Action):
#     def name(self) -> Text:
#         return "action_TTS"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         utterance = []
#         event = tracker.events
#         # to find all bot uterrances
#         for evnt in event:
#             try:
#                 if evnt["event"] == "bot":
#                     bot_utter = evnt['metadata']["utter_action"]
#                     utterance.append(bot_utter)
#             except:
#                 pass

#             # speech o/p for the intent
#             speech_output = BOT_UTTERANCES[utterance[-1]]

#             # generating  temporary file to store the speech output
#             with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
#                 audio_file_path = temp_audio.name

#                 # Generate the speech output using gTTS
#                 # tts = gTTS(text=speech_output, lang='en', slow=True)
#                 tts = gTTS(speech_output)
#                 # tts = gTTS(text=speech_output, lang='hi')
#                 tts.save(audio_file_path)

#                 #  get voice o/p
#                 os.system(f"ffplay -nodisp -autoexit {audio_file_path}")