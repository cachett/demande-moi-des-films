# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice
import numpy as np
from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()



    # To process ratings, users associated to ratings are created and every rating is then stored in its user

    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        #movie = choice(list(self.movies.values())).title choice c'est choix aléatoire en python
        similarities = Recommendation.compute_all_similarities(self, user)
        indices = similarities.argsort()[-5:][::-1]
        bestUsers = np.array(list(self.test_users.values()))[indices]
        all_possible_movie = np.append(bestUsers[0].good_ratings, bestUsers[1].good_ratings)
        for i in range(3):
            all_possible_movie = np.append(all_possible_movie, bestUsers[i+2].good_ratings)

        all_possible_movie_doublon = np.array([])
        movie_bin = np.array([])

        for movies in all_possible_movie:
            if movies in movie_bin:
                all_possible_movie_doublon = np.append(all_possible_movie_doublon, [movies])
            else:
                movie_bin = np.append(movie_bin, [movies])
        all_possible_movie_doublon = np.unique(all_possible_movie_doublon)

        movie = ""
        for movi in all_possible_movie_doublon:
            movie += movi.title + ", "
        return "Vos recommandations : " + ", ".join([movie])

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        allmovies = np.array([])
        for movie in user_a.good_ratings:
            allmovies= np.append(allmovies, [movie.id])
        for movie in user_a.bad_ratings:
            allmovies= np.append(allmovies, [movie.id])
        for movie in user_a.neutral_ratings:
            allmovies= np.append(allmovies, [movie.id])
        for movie in user_b.good_ratings:
            allmovies= np.append(allmovies, [movie.id])
        for movie in user_b.bad_ratings:
            allmovies= np.append(allmovies, [movie.id])
        for movie in user_b.neutral_ratings:
            allmovies= np.append(allmovies, [movie.id])

        allmovies = np.unique(allmovies)

        #VectA
        vectA = np.zeros(len(allmovies))
        for f in user_a.good_ratings:
            vectA[np.where(allmovies == f.id)]= 1 # where retourne la liste des index ou c'est vrai
        for f in user_a.bad_ratings:
            vectA[np.where(allmovies == f.id)]= -1

        #VectB
        vectB = np.zeros(len(allmovies))
        for f in user_b.good_ratings:
            vectB[np.where(allmovies == f.id)]= 1 # where retourne la liste des index ou c'est vrai
        for f in user_b.bad_ratings:
            vectB[np.where(allmovies == f.id)]= -1


        return np.dot(vectA, vectB)/(Recommendation.get_user_norm(user_a)*Recommendation.get_user_norm(user_b))

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        similarities = np.array([])
        for user_test in self.test_users.values():
            l = Recommendation.get_similarity(user, user_test)
            similarities = np.append(similarities, [l])
        return similarities

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(user):
        return np.sqrt(len(user.good_ratings)) + np.sqrt(len(user.bad_ratings))

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
