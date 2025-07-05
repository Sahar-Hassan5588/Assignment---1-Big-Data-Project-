import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

#  Load merged dataset
df = pd.read_csv('matched_posts.csv')


# Filter for high-engagement posts

high_score_df = df[df['Score'] > 10].copy()

print(f"Original dataset size: {df.shape[0]}")
print(f"High-engagement subset size: {high_score_df.shape[0]}")


features = ['Score', 'AnswerCount', 'ViewCount', 'PostLength', 'TagCount']
X = high_score_df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Elbow Method for best k

distortions = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    distortions.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K, distortions, 'bx-')
plt.xlabel('Number of clusters k')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k')
plt.show()

#  Apply K-Means clustering

optimal_k = 5  # Replace with your chosen k
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
high_score_df['Cluster'] = kmeans.fit_predict(X_scaled)
# plot
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
high_score_df['PCA1'] = X_pca[:, 0]
high_score_df['PCA2'] = X_pca[:, 1]

plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=high_score_df,
    x='PCA1', y='PCA2',
    hue='Cluster',
    palette='Set2',
    s=70,
    alpha=0.8
)
plt.title(f'Clusters of High-Engagement Posts (Score > 10, k={optimal_k})')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()

# Save the clustered to CSV
output_file = 'high_score_clustered.csv'
high_score_df.to_csv(output_file, index=False)

print(f"Clustered results written to: {output_file}")
