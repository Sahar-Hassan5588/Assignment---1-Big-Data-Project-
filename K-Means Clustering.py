import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans

# Load data
df = pd.read_csv('matched_posts.csv')

print("Columns in data:", df.columns.tolist())

# exclude 'severity' 
features = ['Score', 'AnswerCount', 'ViewCount', 'PostLength', 'TagCount']

# Encode Matched_Type into numeric 
le = LabelEncoder()
df['matched_type_num'] = le.fit_transform(df['Matched_Type'])

# Add encoded matched_type_num to features
features.append('matched_type_num')

print("Using features:", features)

# Extract features for clustering
X = df[features].fillna(0)  # Fill any NaNs with zero

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Run KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Save results
df.to_csv('matched_posts_clustered_no_severity.csv', index=False)

print("✅ Clustering complete, results saved to 'matched_posts_clustered_no_severity.csv'")
