from .embedding_recommender import EmbeddingRecommender

class RecommenderProvider:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EmbeddingRecommender()
        return cls._instance
