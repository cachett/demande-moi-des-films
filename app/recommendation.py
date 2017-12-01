# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice
import numpy as np
from app.User import User
from sklearn.cluster import KMeans

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
        self.movies = movielens.movies #dictionnaire id movie -> Movie

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Tableau contenant les genres de chaques films dans la BD
        self.tab_genres = np.array([])
        for movie in self.movies.values():
            self.tab_genres = np.append(self.tab_genres, movie.get_genre())
        self.tab_genres = np.reshape(self.tab_genres, (-1,18))

        #Initialisation de l'algo de clustering et entrainement
        self.kmeans = KMeans(init='k-means++', n_clusters=10, n_init=10).fit(self.tab_genres);

        # Launch the process of ratings
        self.process_ratings_to_users()


    # To process ratings, users associated to ratings are created and every rating is then stored in its user

    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            score = rating.score
            cluster = self.kmeans.predict(np.array([movie.get_genre()]))[0]
            user.ratings[cluster] = np.append(user.ratings[cluster], [score])
            if (score>=4):
                user.good_ratings.append(movie)


    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        #on remplit ratings pour le user courant
        for rating in user.rates:
            movie = self.movies[rating.movie]
            score = rating.score
            cluster = self.kmeans.predict(np.array([movie.get_genre()]))[0]
            user.ratings[cluster] = np.append(user.ratings[cluster], [score])

        #calcul des similarités suivant les vecteur de notes de cluster et choisi les users proches
        similarities = Recommendation.compute_all_similarities(self, user)
        print(similarities)
        indices = similarities.argsort()[-6:][::-1] #prend les indices des 5 plus grandes valeurs de similarité et inverse l'ordre
        #Récupération des utilisateurs les plus proches
        bestUsers = np.array(list(self.test_users.values()))[indices] #on prend les 5 users correspondants à ces indices
        best_movies = Recommendation.get_best_movies_from_users(bestUsers, user.asked_movies)


        #Affichage
        movie_str = ""
        for movie in best_movies:
            if movie not in user.asked_movies:
                movie_str += movie.title + ", "
        movie_str = movie_str[:-2]
        return "Vos recommandations : "  + movie_str

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        a = Recommendation.get_normalised_cluster_notations(user_a)
        b = Recommendation.get_normalised_cluster_notations(user_b)
        norm_a = Recommendation.get_user_norm(a)
        norm_b = Recommendation.get_user_norm(b)
        return np.dot(a, b)/(norm_a * norm_b)

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        similarities = np.array([])
        for user_test in self.test_users.values():

            l = Recommendation.get_similarity(user, user_test)
            similarities = np.append(similarities, [l])
        return similarities

    @staticmethod
    def get_best_movies_from_users(users, asked_movies):
        #Return the 3 bests movie, sorted by frequency
        best_movies = np.array([])
        candidate_movies_hash = dict()

        for user in users:
            for movie in user.good_ratings:
                if movie in candidate_movies_hash.keys():
                    candidate_movies_hash[movie] +=1
                else:
                    candidate_movies_hash[movie] = 1

        sorted_movies = sorted(candidate_movies_hash.items(), key=lambda x: x[1]) #films triés par fréquence d'apparition dans les best users

        #prend 3 meilleurs films qui ne sont pas déja demandés
        best_movies = []
        i=1
        while (len(best_movies)<4):
            movie = sorted_movies[-i][0]
            if movie not in asked_movies:
                best_movies.append(movie)
            i+=1

        return best_movies

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(vecteur):
        summ = 0
        for val in vecteur:
            summ += val*val
        return np.sqrt(summ)

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        #moyenne des notes des clusters
        mean_cluster_score = np.array([None,None,None,None,None,None,None,None,None,None]);
        for key, value in user.ratings.items():
            if len(value) != 0:
                mean_cluster_score[key] = np.mean(value)


        #moyenne des notations pour ceux qui vote trop haut ou trop bas
        mean_rate = 0
        counter = 0
        for value in mean_cluster_score:
            if value is not None:
                mean_rate +=value
                counter += 1
        mean_rate = mean_rate/counter

        # Creation du vecteur de notation normalisée de l'utilisateur
        for i in range(len(mean_cluster_score)):
            value = mean_cluster_score[i]
            if value is not None:
                mean_cluster_score[i] -= mean_rate
            else:
                mean_cluster_score[i] = 0
        return mean_cluster_score
