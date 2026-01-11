from sklearn.metrics.pairwise import rbf_kernel 
from sklearn.cluster import KMeans
from sklearn.base import BaseEstimator, TransformerMixin
class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10,  gamma=0.1, random_state=None):
        self.n_clusters=n_clusters
        self.gamma=gamma
        self.random_state=random_state

    def fit(self, X, y=None, sample_weight=None):
        self.Kmeans_=KMeans(self.n_clusters, n_init=10, 
                           random_state=self.random_state)
        self.Kmeans_.fit(X, sample_weight=sample_weight)
        return self

    def transform(self,X):
        return rbf_kernel(X, self.Kmeans_.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, name=None):
        return [f"Cluster {i} similarity" for i in range(self.n_clusters)]
