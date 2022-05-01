from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.metrics import silhouette_score
from matplotlib import pyplot
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn import datasets 
import os

def load_playlist_pkl(path):
    pkl_files = os.listdir(path)
    feature_df = pd.DataFrame()
    for i in pkl_files:
        if i.endswith('.pkl'):
            df = pd.read_pickle(path+ '/' + i)
            feature_df = pd.concat([feature_df, df])
    return feature_df        




def apply_scaler(X):
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)
    display(X.head())
    display(X_scaled_df.head())
    return X_scaled_df, scaler

def apply_kmeans(X_scaled_df, n):
    kmeans = KMeans(n_clusters=n, random_state=1234, n_init = 20, max_iter = 500)
    kmeans.fit(X_scaled_df)
    return kmeans

def predict_kmeans(X_scaled_df, X, centroids):
    # assign a cluster to each example
    labels = centroids.predict(X_scaled_df)
    # retrieve unique clusters
    clusters = np.unique(labels)
    # create scatter plot for samples from each cluster
    return labels, clusters

def plot_clusters(centroids, X, labels):
    for cluster in centroids:
        # get row indexes for samples with this cluster
        row_ix = np.where(labels == cluster)
        # create scatter of these samples
        pyplot.scatter(X.to_numpy()[row_ix, 1], X.to_numpy()[row_ix, 2])
        # show the plot
        display(pyplot.show())


def elbowing(path):
    K = range(2, 21)
    inertia = []
    X_hat = load_pkl(path)
    for k in K:
        print("Training a K-Means model with {} clusters! ".format(k))
        print()
        kmeans = KMeans(n_clusters=k,
                        random_state=1234)
        kmeans.fit(X_hat)
        inertia.append(kmeans.inertia_)


    plt.figure(figsize=(16,8))
    plt.plot(K, inertia, 'bx-')
    plt.xlabel('k')
    plt.ylabel('inertia')
    plt.xticks(np.arange(min(K), max(K)+1, 1.0))
    plt.title('Elbow Method showing the optimal k')
    return

def silhouetting(path):
    X_hat = load_pkl(path)
    K = range(2, 20)
    silhouette = []

    for k in K:
        kmeans = KMeans(n_clusters=k,
                        random_state=1234)
        kmeans.fit(X_hat)


        silhouette.append(silhouette_score(X_hat, kmeans.predict(X_hat)))


    plt.figure(figsize=(16,8))
    plt.plot(K, silhouette, 'bx-')
    plt.xlabel('k')
    plt.ylabel('silhouette score')
    plt.xticks(np.arange(min(K), max(K)+1, 1.0))
    plt.title('Silhouette Method showing the optimal k')
    return

def yellowbricking(path, n):
    X_hat = load_pkl(path)
    model = KMeans(n, random_state=42)
    visualizer = SilhouetteVisualizer(model, colors='yellowbrick')
    visualizer.fit(X_hat)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    return

def save_pkl(model, filename = 'filename.pickle'): 
    with open(filename, "wb") as f:
        pickle.dump(model, f)

def load_pkl(filename = 'filename.pickle'): 
    try: 
        with open(filename, "rb") as f: 
            return pickle.load(f) 
        
    except FileNotFoundError: 
        print('File not found!')
        return
        
        
def kmeans_missing(path, n_clusters, max_iter=10):
    """Perform K-Means clustering on data with missing values.

    Args:
      X: An [n_samples, n_features] array of data to cluster.
      n_clusters: Number of clusters to form.
      max_iter: Maximum number of EM iterations to perform.

    Returns:
      labels: An [n_samples] vector of integer labels.
      centroids: An [n_clusters, n_features] array of cluster centroids.
      X_hat: Copy of X with the missing values filled in.
    """
    X = load_pkl(path)
    # Initialize missing values to their column means
    missing = ~np.isfinite(X)
    mu = np.nanmean(X, 0, keepdims=1)
    X_hat = np.where(missing, mu, X)

    for i in range(max_iter):
        if i > 0:
            # initialize KMeans with the previous set of centroids. this is much
            # faster and makes it easier to check convergence (since labels
            # won't be permuted on every iteration), but might be more prone to
            # getting stuck in local minima.
            cls = KMeans(n_clusters, init=prev_centroids)
        else:
            # do multiple random initializations in parallel
            cls = KMeans(n_clusters)

        # perform clustering on the filled-in data
        labels = cls.fit_predict(X_hat)
        centroids = cls.cluster_centers_

        # fill in the missing values based on their cluster centroids
        X_hat[missing] = centroids[labels][missing]

        # when the labels have stopped changing then we have converged
        if i > 0 and np.all(labels == prev_labels):
            break

        prev_labels = labels
        prev_centroids = cls.cluster_centers_

    return labels, centroids, X_hat, n_clusters, max_iter
