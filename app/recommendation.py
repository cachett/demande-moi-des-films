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
        # vecteur de notation normalisé
        self.user_cluster_matrix = np.array([])

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
        #Vecteur normalisés pour les user test
        for user_test in self.test_users.values():
            self.user_cluster_matrix = np.append(self.user_cluster_matrix, Recommendation.get_normalised_cluster_notations(user_test))

        #on remplit ratings pour le user courant
        for rating in user.rates:
            movie = self.movies[rating.movie]
            score = rating.score
            cluster = self.kmeans.predict(np.array([movie.get_genre()]))[0]
            user.ratings[cluster] = np.append(user.ratings[cluster], [score])



        #movie = choice(list(self.movies.values())).title choice c'est choix aléatoire en python
        similarities = Recommendation.compute_all_similarities(self, user)
        print(similarities)
        indices = similarities.argsort()[-5:][::-1] #prend les indices des 5 plus grandes valeurs de similarité et inverse l'ordre
        bestUsers = np.array(list(self.test_users.values()))[indices] #on prend les 5 users correspondants à ces indices
        all_possible_movie = Recommendation.get_best_movies_from_users(bestUsers)
        all_possible_movie_doublon = np.array([])
        movie_bin = np.array([])
        print(all_possible_movie)

        #Ne garde que les films qui on été aimé par au moins deux autres Users proches
        for movies in all_possible_movie:
            if movies in movie_bin:
                all_possible_movie_doublon = np.append(all_possible_movie_doublon, [movies])
            else:
                movie_bin = np.append(movie_bin, [movies])
        all_possible_movie_doublon = np.unique(all_possible_movie_doublon)


        #Affichage
        movie = ""
        for movi in all_possible_movie_doublon:
            movie += movi.title + ", "
        return "Vos recommandations : " + ", ".join([movie])

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        a = Recommendation.get_normalised_cluster_notations(user_a)
        b = Recommendation.get_normalised_cluster_notations(user_b)
        norm_a = Recommendation.get_user_norm(a)
        norm_b = Recommendation.get_user_norm(b)
        print(norm_a)
        print(norm_b)
        return np.dot(a, b)/(norm_a * norm_b)
    # @staticmethod
    # def get_similarity(user_a, user_b):
    #     allmovies = np.array([])
    #     for movie in user_a.good_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #     for movie in user_a.bad_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #     for movie in user_a.neutral_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #     for movie in user_b.good_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #     for movie in user_b.bad_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #     for movie in user_b.neutral_ratings:
    #         allmovies= np.append(allmovies, [movie.id])
    #
    #     allmovies = np.unique(allmovies)
    #
    #     #VectA
    #     vectA = np.zeros(len(allmovies))
    #     for f in user_a.good_ratings:
    #         vectA[np.where(allmovies == f.id)]= 1 # where retourne la liste des index ou c'est vrai
    #     for f in user_a.bad_ratings:
    #         vectA[np.where(allmovies == f.id)]= -1
    #
    #     #VectB
    #     vectB = np.zeros(len(allmovies))
    #     for f in user_b.good_ratings:
    #         vectB[np.where(allmovies == f.id)]= 1 # where retourne la liste des index ou c'est vrai
    #     for f in user_b.bad_ratings:
    #         vectB[np.where(allmovies == f.id)]= -1
    #
    #
    #     return np.dot(vectA, vectB)/(Recommendation.get_user_norm(user_a)*Recommendation.get_user_norm(user_b))

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        similarities = np.array([])
        for user_test in self.test_users.values():

            l = Recommendation.get_similarity(user, user_test)
            similarities = np.append(similarities, [l])
        return similarities

    @staticmethod
    def get_best_movies_from_users(users):
        best_movies = np.array([])
        for user in users:
            best_movies = np.append(best_movies, user.good_ratings)
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
