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

def load_playlist_pkl():
    path = 'library_spotify'
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
    print()
    display(X_scaled_df.head())
    return X_scaled_df, scaler

def apply_kmeans(X_scaled_df, n):
    kmeans = KMeans(n_clusters=n, random_state=1234)
    kmeans.fit(X_scaled_df)
    return kmeans

def predict_kmeans(X_scaled_df):
    # assign a cluster to each example
    labels = kmeans.predict(X_scaled_df)
    # retrieve unique clusters
    clusters = np.unique(labels)
    # create scatter plot for samples from each cluster
    for cluster in clusters:
        # get row indexes for samples with this cluster
        row_ix = np.where(labels == cluster)
        # create scatter of these samples
        pyplot.scatter(X.to_numpy()[row_ix, 1], X.to_numpy()[row_ix, 2])
        # show the plot
    pyplot.show()
    return labels, clusters

def elbowing(X_scaled_df):
    K = range(2, 21)
    inertia = []

    for k in K:
        print("Training a K-Means model with {} clusters! ".format(k))
        print()
        kmeans = KMeans(n_clusters=k,
                        random_state=1234)
        kmeans.fit(X_scaled_df)
        inertia.append(kmeans.inertia_)


    plt.figure(figsize=(16,8))
    plt.plot(K, inertia, 'bx-')
    plt.xlabel('k')
    plt.ylabel('inertia')
    plt.xticks(np.arange(min(K), max(K)+1, 1.0))
    plt.title('Elbow Method showing the optimal k')
    return

def silhouetting(X_scaled_df):
    K = range(2, 20)
    silhouette = []

    for k in K:
        kmeans = KMeans(n_clusters=k,
                        random_state=1234)
        kmeans.fit(X_scaled_df)


        silhouette.append(silhouette_score(X_scaled_df, kmeans.predict(X_scaled_df)))


    plt.figure(figsize=(16,8))
    plt.plot(K, silhouette, 'bx-')
    plt.xlabel('k')
    plt.ylabel('silhouette score')
    plt.xticks(np.arange(min(K), max(K)+1, 1.0))
    plt.title('Silhouette Method showing the optimal k')
    return

def yellowbricking(X_scaled_df, n):
    model = KMeans(n, random_state=42)
    visualizer = SilhouetteVisualizer(model, colors='yellowbrick')
    visualizer.fit(X_scaled_df)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    return