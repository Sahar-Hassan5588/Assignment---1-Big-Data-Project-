
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load the clustered high-score posts
df = pd.read_csv('high_score_clustered.csv')
print(df.columns)
df['Cluster'] = df['Cluster'].astype(int)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

df['Year'] = df['Date'].dt.year

# Number of posts per cluster per year
posts_per_cluster = df.groupby(['Year', 'Cluster']).size().reset_index(name='PostCount')
plt.figure(figsize=(10, 6))
sns.lineplot(data=posts_per_cluster, x='Year', y='PostCount', hue='Cluster', marker='o', palette='tab10')
plt.title('Number of Posts per Cluster Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Posts')
plt.legend(title='Cluster', loc='upper left')
plt.tight_layout()
plt.savefig('posts_per_cluster_over_time.png', dpi=300)
print("Saved: posts_per_cluster_over_time.png")
plt.show()

# Average Score per cluster per year (Trend)

score_trend = df.groupby(['Year', 'Cluster'])['Score'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=score_trend, x='Year', y='Score', hue='Cluster', marker='o', palette='tab10')
plt.title('Average Score per Cluster Over Time')
plt.xlabel('Year')
plt.ylabel('Average Score')
plt.legend(title='Cluster', loc='upper left')
plt.tight_layout()
plt.savefig('avg_score_per_cluster_over_time.png', dpi=300)
print("Saved: avg_score_per_cluster_over_time.png")
plt.show()
