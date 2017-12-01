# Handle action around a specific user: manage its movies, its questions, etc.
import numpy as np
from app.movielens import Rating

class User:

    def __init__(self, sender_id):
        self.id = sender_id
        # Variables used to follow at what step is the user
        self.latest_movie_asked = None
        self.questions_before_recommendation = 5
        # Variables used for the first algorithm

        #self.good_ratings = []
        self.bad_ratings = []
        self.neutral_ratings = []
        # Variables used for the second algorithm
        self.ratings = dict()
        self.good_ratings = []
        self.rates = [] # servira pour l'utilisateur courant
        for i in range(10):
            self.ratings[i] = np.array([])


    def has_been_asked_a_question(self):
        return self.latest_movie_asked is not None

    #pour algo 1
    def answer_yes(self):
        self.good_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    def answer_no(self):
        self.bad_ratings.append(self.latest_movie_asked)
        self.questions_before_recommendation -= 1

    #pour algo 2
    def answer_0(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 0) )
        self.questions_before_recommendation -= 1
    def answer_1(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 1) )
        self.questions_before_recommendation -= 1
    def answer_2(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 2) )
        self.questions_before_recommendation -= 1
    def answer_3(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 3) )
        self.questions_before_recommendation -= 1
    def answer_4(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 4) )
        self.questions_before_recommendation -= 1
    def answer_5(self):
        self.rates.append( Rating(self.latest_movie_asked.id, self.id, 5) )
        self.questions_before_recommendation -= 1

    def answer_neutral(self):
        pass

    def should_make_recommendation(self):
        return self.questions_before_recommendation is 0

    def set_pending_question(self, movie):
        self.latest_movie_asked = movie

    def reset_remaining_questions_number(self):
        self.questions_before_recommendation = 5
        self.latest_movie_asked = None

    def process_message(self, message):
        # If nothing is asked to the user, do nothing
        if self.latest_movie_asked is None:
            return

        # Clean space excess and set to lowercase
        clean_message = message.lower().strip()

        if "0" in clean_message:
            self.answer_0()
        elif "1" in clean_message:
            self.answer_1()
        elif "2" in clean_message:
            self.answer_2()
        elif "3" in clean_message:
            self.answer_3()
        elif "4" in clean_message:
            self.answer_4()
        elif "5" in clean_message:
            self.answer_5()
        else:
            self.answer_neutral()
