import unittest
import pandas as pd
from main import MovieRecommendationSystem
import os

class TestMovieRecommendationSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.test_data_file = 'test_movies.csv'
        data = {
            'index': [0, 1, 2],
            'title': ['Movie A', 'Movie B', 'Movie C'],
            'genres': ['Action|Adventure', 'Drama|Romance', 'Comedy|Drama'],
            'keywords': ['hero|fight', 'love|tragedy', 'funny|sad'],
            'tagline': ['Exciting movie', 'Heartwarming story', 'Life is funny'],
            'cast': ['Actor A|Actor B', 'Actor C|Actor D', 'Actor E|Actor F'],
            'director': ['Director A', 'Director B', 'Director C'],
            'vote_average': [8.0, 7.5, 7.0]
        }
        df = pd.DataFrame(data)
        df.to_csv(cls.test_data_file, index=False)

    @classmethod
    def tearDownClass(cls):
        # Remove the test data file after tests
        if os.path.exists(cls.test_data_file):
            os.remove(cls.test_data_file)

    def setUp(self):
        self.recommender = MovieRecommendationSystem(self.test_data_file)
        self.recommender.preprocess_data()

    def test_preprocess_data(self):

        self.assertIsNotNone(self.recommender.similarity)
        self.assertEqual(self.recommender.feature_vectors.shape[0], 3)

    def test_recommend_movies(self):

        recommendations = self.recommender.recommend_movies('Movie A')
        self.assertIsNotNone(recommendations)
        self.assertIn('Movie B', recommendations)
        self.assertIn('Movie C', recommendations)

    def test_plot_vote_averages(self):

        recommended_movies = [('Movie A', 8.0), ('Movie B', 7.5), ('Movie C', 7.0)]
        self.recommender.plot_vote_averages(recommended_movies)
        self.assertTrue(os.path.exists('vote_averages.png'))
        if os.path.exists('vote_averages.png'):
            os.remove('vote_averages.png')

if __name__ == '__main__':
    unittest.main()
