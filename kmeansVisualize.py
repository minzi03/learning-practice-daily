import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.lines import Line2D
from scipy.spatial import ConvexHull
from scipy import interpolate

# Load and prepare data
df = pd.read_csv('Pokemon.csv')
types = df['Type 1'].isin(['Grass', 'Fire', 'Water'])
drop_cols = ['Type 1', 'Type 2', 'Generation', 'Legendary', '#']
df = df[types].drop(columns=drop_cols)

# Function to perform KMeans clustering and add cluster-related columns
def perform_kmeans(df, n_clusters, columns):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(df[columns])
    centroids = kmeans.cluster_centers_
    df['cen_x'] = df['cluster'].map({i: centroids[i][0] for i in range(n_clusters)})
    df['cen_y'] = df['cluster'].map({i: centroids[i][1] for i in range(n_clusters)})
    colors = ['#DF2020', '#81DF20', '#2095DF']
    df['c'] = df['cluster'].map({i: colors[i] for i in range(n_clusters)})
    return df, centroids, colors

# Function to plot data with clusters
def plot_clusters(df, centroids, colors, columns, plot_type='2d', size='small', interpolate_hull=False):
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.scatter(df[columns[0]], df[columns[1]], c=df['c'], alpha=0.6, s=10 if size == 'small' else df['Speed'])

    # Plot centroids
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='^', c=colors, s=70)

    # Plot convex hulls if required
    if interpolate_hull:
        for i in df['cluster'].unique():
            points = df[df['cluster'] == i][columns].values
            hull = ConvexHull(points)
            x_hull = np.append(points[hull.vertices, 0], points[hull.vertices, 0][0])
            y_hull = np.append(points[hull.vertices, 1], points[hull.vertices, 1][0])
            dist = np.sqrt((x_hull[:-1] - x_hull[1:]) ** 2 + (y_hull[:-1] - y_hull[1:]) ** 2)
            dist_along = np.concatenate(([0], dist.cumsum()))
            spline, _ = interpolate.splprep([x_hull, y_hull], u=dist_along, s=0)
            interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
            interp_x, interp_y = interpolate.splev(interp_d, spline)
            plt.fill(interp_x, interp_y, '--', c=colors[i], alpha=0.2)

    # Title and labels
    plt.title('Pokemon Stats\n', loc='left', fontsize=22)
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.xlim(0, 200)
    plt.ylim(0, 200)

    # Create legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'Cluster {i+1}',
                              markerfacecolor=colors[i], markersize=5) for i in range(len(colors))]
    legend_elements += [Line2D([0], [0], marker='^', color='w', label=f'Centroid - C{i+1}',
                               markerfacecolor=colors[i], markersize=10) for i in range(len(colors))]
    plt.legend(handles=legend_elements, loc='upper right', ncol=2)
    plt.show()

# Perform KMeans clustering and plot
df, centroids, colors = perform_kmeans(df, n_clusters=3, columns=['Attack', 'Defense'])
plot_clusters(df, centroids, colors, ['Attack', 'Defense'], interpolate_hull=True)