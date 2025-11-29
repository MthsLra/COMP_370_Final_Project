import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os.path

path = os.path.join('../', 'annotated_data', 'annotated_buford.csv')
df = pd.read_csv(path)

df['Topic'] = df['Topic'].astype(str).str.strip()
df['Dialog'] = df['Dialog'].astype(str)

topics = df['Topic'].unique()
top_words_per_topic = {}

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Dialog'])
feature_names = vectorizer.get_feature_names_out()

n_docs, n_features = tfidf_matrix.shape
if n_features == 0:
    raise ValueError("No features extracted !!!")

for topic in topics:
    topic_indices = df.index[df['Topic'] == topic].tolist()
    
    if len(topic_indices) == 0:
        print(f"Warning: Topic '{topic}' has 0 lines — skipping.")
        continue

    topic_rows = tfidf_matrix[topic_indices]

    topic_sum = topic_rows.sum(axis=0)

    if hasattr(topic_sum, "A1"):
        topic_avg = topic_sum.A1 / len(topic_indices)
    else:
        topic_avg = np.asarray(topic_sum).ravel() / len(topic_indices)

    # top 10 terms
    top_indices = topic_avg.argsort()[::-1][:10]
    top_words = [(feature_names[i], float(topic_avg[i])) for i in top_indices]
    top_words_per_topic[topic] = top_words

# printing
for topic, words in top_words_per_topic.items():
    print(f"\nTopic: {topic}")
    for word, score in words:
        print(f"  {word}: {score:.4f}")
