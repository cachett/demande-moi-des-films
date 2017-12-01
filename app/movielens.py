# Take care of importing the movie database and the training data set

import csv
import numpy as np

class Movie:

    def __init__(self, movie_id, title, release_date, genres):
        self.id = int(movie_id)
        self.title = title
        self.release_date = release_date
        self.unknown = 0
        self.action = 0
        self.adventure = 0
        self.animation = 0
        self.children = 0
        self.comedy = 0
        self.crime = 0
        self.documentary = 0
        self.drama = 0
        self.fantasy = 0
        self.film_noir = 0
        self.horror = 0
        self.musical = 0
        self.mystery = 0
        self.romance = 0
        self.sci_fi = 0
        self.thriller = 0
        self.war = 0
        self.western = 0
        self.init_genres(genres)

    def init_genres(self, genres):
        for genre in genres.split('|'):
            if genre == "Action":
                self.action = 1
            if genre == "Adventure":
                self.adventure = 1
            if genre == "Animation":
                self.animation = 1
            if genre == "Children":
                self.children = 1
            if genre == "Comedy":
                self.comedy = 1
            if genre == "Crime":
                self.crime = 1
            if genre == "Documentary":
                self.documentary = 1
            if genre == "Drama":
                self.drama = 1
            if genre == "Fantasy":
                self.fantasy = 1
            if genre == "Film-Noir":
                self.film_noir = 1
            if genre == "Horror":
                self.horror = 1
            if genre == "Musical":
                self.musical = 1
            if genre == "Mystery":
                self.mystery = 1
            if genre == "Romance":
                self.romance = 1
            if genre == "Sci-Fi":
                self.sci_fi = 1
            if genre == "Thriller":
                self.thriller = 1
            if genre == "War":
                self.war = 1
            if genre == "Western":
                self.western = 1

    def __str__(self):
        return self.title

    def __lt__(self, other):
        return self.id < other.id

    def get_genre(self):
        genre = np.zeros(18)
        if self.action == 1 :
            genre[0] = 1
        if self.adventure == 1 :
            genre[1] = 1
        if self.animation == 1 :
            genre[2] = 1
        if self.action == 1 :
            genre[3] = 1
        if self.action == 1 :
            genre[4] = 1
        if self.action == 1 :
            genre[5] = 1
        if self.action == 1 :
            genre[6] = 1
        if self.action == 1 :
            genre[7] = 1
        if self.action == 1 :
            genre[8] = 1
        if self.action == 1 :
            genre[9] = 1
        if self.action == 1 :
            genre[10] = 1
        if self.musical == 1 :
            genre[11] = 1
        if self.mystery == 1 :
            genre[12] = 1
        if self.romance == 1 :
            genre[13] = 1
        if self.sci_fi == 1 :
            genre[14] = 1
        if self.thriller == 1 :
            genre[15] = 1
        if self.war == 1 :
            genre[16] = 1
        if self.western == 1 :
            genre[17] = 1
        return genre

class Rating:

    def __init__(self, movie_id, user_id, score):
        self.movie = int(movie_id)
        self.user = int(user_id)
        self.score = float(score)


class SimplifiedRating:

    def __init__(self, movie_id, user_id, is_appreciated):
        self.movie = int(movie_id)
        self.user = int(user_id)
        self.is_appreciated = True if is_appreciated == 'True' else False


class MovieLens:

    def __init__(self):
        self.movies = self.load_movies()
        self.ratings = self.load_ratings()
        self.simplified_ratings = self.load_simplified_ratings()

    # Load movies from movie set and create manageable objects
    @staticmethod
    def load_movies():
        movies = dict()
        with open('./ml-latest-small/movies-clean.csv', 'rt') as moviesFile:
            raw_movies = csv.reader(moviesFile, delimiter=',')
            is_first = True
            for movie in raw_movies:
                if is_first:
                    is_first = False
                    continue
                movies[int(movie[0])] = Movie(movie[0], movie[1], movie[2], movie[3])
            return movies

    # Load ratings from ratings set and create manageable objects
    @staticmethod
    def load_ratings():
        ratings = []
        with open('./ml-latest-small/ratings.csv', 'rt') as ratingsFile:
            raw_ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in raw_ratings:
                if is_first:
                    is_first = False
                    continue
                ratings.append(Rating(rating[1], rating[0], rating[2]))

        return ratings

    # Load ratings from ratings set, simplify their notation and create manageable objects
    @staticmethod
    def load_simplified_ratings():
        ratings = []
        with open('./ml-latest-small/ratings-popular-simplified.csv', 'rt') as ratingsFile:
            raw_ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in raw_ratings:
                if is_first:
                    is_first = False
                    continue
                ratings.append(SimplifiedRating(rating[1], rating[0], rating[2]))

        return ratings
