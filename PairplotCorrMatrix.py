import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load clustered dataset

high_score_df = pd.read_csv('high_score_clustered.csv')
high_score_df['Cluster'] = high_score_df['Cluster'].astype(int)
features = ['Score', 'ViewCount', 'AnswerCount', 'PostLength', 'TagCount']

pairplot = sns.pairplot(
    high_score_df[features + ['Cluster']],
    hue='Cluster',
    palette='Set2'
)
pairplot.fig.suptitle('Pairplot of Key Features Coloured by Cluster', y=1.02)
# Save the pairplot
pairplot.savefig('pairplot_clusters.png', dpi=300)
print("Pairplot saved as 'pairplot_clusters.png'")
plt.show()


#correlation matrix heatmap
corr_matrix = high_score_df[features].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Matrix of High-Engagement Posts Features')
# Save the heatmap
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
print("Correlation matrix saved as 'correlation_matrix.png'")

plt.show()
