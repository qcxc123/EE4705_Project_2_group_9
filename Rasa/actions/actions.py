# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

import json
import random


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subj = tracker.get_slot("quiz_subject")  # check subject

        f = open('data/'+str(subj)+'.json')  # open data
        data = json.load(f)
        i = random.randint(0, len(data)-1)  # choose random question number
        qn = data[i]['question']  # get the question

        # put all the answers in a list to shuffle
        ans_list = []

        # there are (len-2) distractors. Only science dataset has additional "support" key
        end = len(data[i])-1 if str(subj) != "science" else len(data[i])-2
        for j in range(1, end):
            ans_list.append(data[i]['distractor'+str(j)])
        ans_list.append(data[i]['correct_answer'])  # append correct ans at the end of list

        # shuffle answer list
        shuffle_idx = list(range(len(ans_list)))  # list of indices
        random.shuffle(shuffle_idx)  # shuffle indices
        ans_list = [ans_list[j] for j in shuffle_idx]  # use indices to shuffle ans_list
        corr_ans = shuffle_idx.index(len(ans_list)-1) + 1  # get index of correct ans

        f.close()  # close data file

        # prepare message to print
        message = "Here is your question:\n" + qn
        for k in range(len(ans_list)):
            message = message + "\n" + str(k+1) + "." + ans_list[k]
        message = message + "\nPlease input a number as your answer."

        dispatcher.utter_message(text=message)

        return [SlotSet(key = "question_number", value = i), SlotSet(key = "corr_ans", value = corr_ans)]


class ActionCheckAnswer(Action):

    def name(self) -> Text:
        return "action_check_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subj = tracker.get_slot("quiz_subject")  # check subject

        f = open('data/'+str(subj)+'.json')  # open data
        data = json.load(f)

        # check question number, user answer, and correct answer
        i = int(tracker.get_slot("question_number"))
        corr_ans = int(tracker.get_slot("corr_ans"))
        user_ans = int(tracker.get_slot("user_ans"))
        f.close()

        # get correct answer
        corr_text = data[i]['correct_answer']

        # get explanation if available
        explanation=""
        if str(subj)=='science':
            explanation = data[i]['support']

        # get current score progress
        user_score = int(tracker.get_slot("user_score"))
        max_score = int(tracker.get_slot("max_score"))

        # check answer, inform user, and update score
        if user_ans == corr_ans:
            message = "Well done!"
            user_score += 1
        else:
            message = "That's not right. The correct answer is " + str(corr_ans)+ ". " + corr_text

        # add explanation in available
        if explanation != "":
            message = message + "\nHere's an excerpt about this:\n" + explanation

        max_score += 1  # update max score

        dispatcher.utter_message(text=message)

        return [SlotSet(key = "user_ans", value = None), SlotSet(key = "user_score", value = user_score), SlotSet(key = "max_score", value = max_score)]


class ActionCheckScore(Action):

    def name(self) -> Text:
        return "action_check_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subj = tracker.get_slot("quiz_subject")  # check subject

        user_score = int(tracker.get_slot("user_score"))
        max_score = int(tracker.get_slot("max_score"))

        message = "Your current score for " + str(subj) + " is " + str(user_score) + "/" + str(max_score)
        if user_score > 0.8*max_score:
            message = message + "\nWell done so far!"
        elif user_score > 0.5*max_score:
            message = message + "\nNot bad at all!"
        else:
            message = message + "\nYou could do better!"
        dispatcher.utter_message(text=message)

        return []


class ActionQuitSubject(Action):
    def name(self) -> Text:
        return "action_quit_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subj = tracker.get_slot("quiz_subject")  # check subject

        user_score = int(tracker.get_slot("user_score"))
        max_score = int(tracker.get_slot("max_score"))

        message = "Your final score for " + str(subj) + " is " + str(user_score) + "/" + str(max_score)
        if user_score > 0.8*max_score:
            message = message + "\nWell done! Keep up the good work!"
        elif user_score > 0.5*max_score:
            message = message + "\nNot bad, if you study more you'll do even better!"
        else:
            message = message + "\nDo more revision and come back soon!"
        dispatcher.utter_message(text=message)

        return [AllSlotsReset()]


class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]