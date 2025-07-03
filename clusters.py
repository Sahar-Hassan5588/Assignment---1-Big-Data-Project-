import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# Load your CSV file
file_path = '/Users/saharhassan/matched_posts.csv'
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Convert tags from string to list
df['Tags'] = df['Tags'].apply(lambda x: re.findall(r'\|([a-zA-Z0-9\-_.#]+)\|', '|' + str(x) + '|'))

# ---- STEP 1: Top Tags (optional insight) ----
all_tags = [tag for sublist in df['Tags'] for tag in sublist]
tag_counts = Counter(all_tags)
print("Top 10 Tags:")
print(tag_counts.most_common(10))

# ---- STEP 2: Define Bug Clusters (with OTHER included) ----
def classify_bug_cluster(tags):
    clusters = []
    if any(tag in tags for tag in ['nullpointerexception', 'null', 'undefined']):
        clusters.append('NULL_DEREFERENCE')
    if any(tag in tags for tag in ['memory-leak', 'memory', 'dispose', 'garbage-collection']):
        clusters.append('RESOURCE_LEAK')
    if any(tag in tags for tag in ['multithreading', 'race-condition', 'deadlock', 'semaphore', 'mutex']):
        clusters.append('THREAD_SAFETY_VIOLATION')
    if any(tag in tags for tag in ['exception', 'error-handling']):
        clusters.append('GENERAL_EXCEPTION')
    if not clusters:
        clusters.append('OTHER')
    return clusters

# ---- STEP 3: Apply Cluster Classification ----
df['Bug_Clusters'] = df['Tags'].apply(classify_bug_cluster)

# ---- STEP 4: Explode for multi-label support ----
df_exploded = df.explode('Bug_Clusters')

# ---- STEP 5: Post Counts by Cluster ----
cluster_counts = df_exploded['Bug_Clusters'].value_counts()
print("\nPost Counts by Bug Cluster:")
print(cluster_counts)

# ---- STEP 6: Average Scores by Cluster ----
avg_score = df_exploded.groupby('Bug_Clusters')['Score'].mean().sort_values(ascending=False)
print("\nAverage Score by Bug Cluster:")
print(avg_score)

# ---- STEP 7: Visualise Post Counts ----
plt.figure(figsize=(8, 5))
sns.barplot(x=cluster_counts.index, y=cluster_counts.values, palette="muted")
plt.title("Number of Posts per Bug Cluster")
plt.ylabel("Post Count")
plt.xlabel("Bug Cluster")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- STEP 8: Visualise Average Scores ----
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_score.index, y=avg_score.values, palette="viridis")
plt.title("Average Score per Bug Cluster")
plt.ylabel("Average Score")
plt.xlabel("Bug Cluster")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- STEP 9: Analyse "OTHER" Posts ----
df_other = df_exploded[df_exploded['Bug_Clusters'] == 'OTHER']
other_tags = [tag for tags in df_other['Tags'] for tag in tags]
other_tag_counts = Counter(other_tags)

print("\nTop 20 Tags in 'OTHER' Posts:")
print(other_tag_counts.most_common(20))

# Optional: Save posts labeled as "OTHER" for manual review
df_other.to_csv('/Users/saharhassan/other_cluster_posts.csv', index=False)
print("Saved: other_cluster_posts.csv")

# ---- STEP 10: Export Summary Table ----
summary_df = df_exploded.groupby('Bug_Clusters').agg({
    'Score': ['count', 'mean', 'max']
})
summary_df.columns = ['Post_Count', 'Avg_Score', 'Max_Score']
summary_df = summary_df.sort_values('Post_Count', ascending=False)
summary_df.to_csv('/Users/saharhassan/cluster_summary_clean.csv')
print("Saved: cluster_summary_clean.csv")
