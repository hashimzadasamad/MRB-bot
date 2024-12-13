import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

class MovieRecommendationSystem:
    def __init__(self, data_file):
        self.movies_data = pd.read_csv(data_file)
        self.selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'vote_average']
        self.vectorizer = TfidfVectorizer()
        self.similarity = None

    def preprocess_data(self):
        for feature in self.selected_features:
            self.movies_data[feature] = self.movies_data[feature].fillna('')
        combined_features = (self.movies_data['genres'] + ' ' + self.movies_data['keywords'] + ' ' +
                             self.movies_data['tagline'] + ' ' + self.movies_data['cast'] + ' ' +
                             self.movies_data['director'] + ' ' + self.movies_data['vote_average'].astype(str))
        self.feature_vectors = self.vectorizer.fit_transform(combined_features)
        self.similarity = cosine_similarity(self.feature_vectors)

    def recommend_movies(self, movie_name):
        result = ""
        list_of_all_titles = self.movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        if not find_close_match:
            return None
        close_match = find_close_match[0]
        index_of_the_movie = self.movies_data[self.movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(self.similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommended_movies = []
        for i, movie in enumerate(sorted_similar_movies):
            if i < 14:
                index = movie[0]
                title_from_index = self.movies_data[self.movies_data.index == index]['title'].values[0]
                vote_average_from_index = self.movies_data[self.movies_data.index == index]['vote_average'].values[0]
                recommended_movies.append((title_from_index, vote_average_from_index))
                result += f"{i+1}. {title_from_index} - Vote Average: {vote_average_from_index}\n"

        self.plot_vote_averages(recommended_movies)
        return result

    def plot_vote_averages(self, recommended_movies):
        titles = [movie[0] for movie in recommended_movies]
        vote_averages = [movie[1] for movie in recommended_movies]
        print(titles)


        plt.figure(figsize=(10, 6))
        plt.barh(titles, vote_averages, color='skyblue')
        plt.xlabel('Vote Average')
        plt.title('Vote Averages of Recommended Movies')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('vote_averages.png')
        plt.close()


def main():
    data_file = "movies.csv"
    recommender = MovieRecommendationSystem(data_file)
    recommender.preprocess_data()
    movie_name = input('Enter your favourite movie name: ')
    recommender.recommend_movies(movie_name)

if __name__ == "__main__":
    main()
