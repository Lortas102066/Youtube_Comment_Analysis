from textblob import TextBlob
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from collections import Counter
import re

# YouTube API initialization
youtube = build('youtube', 'v3', developerKey='AIzaSyAcwUcxHIH8qb5lkJUgaUMnH65djGnTAoY')
video_id = 'j2m6jNMcfoM'  # Replace with your video ID

def get_video_comments(video_id, max_results=100):
    # Fetch comments from YouTube
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=max_results
    ).execute()

    comments = []
    for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

def analyze_sentiment(text_content):
    """Analyze the sentiment of the text"""
    blob = TextBlob(text_content)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def word_frequency(comments):
    """Calculate the frequency of words used in comments"""
    words = []
    for comment in comments:
        # Remove non-alphabetic characters and split into words
        words += re.findall(r'\b\w+\b', comment.lower())
    return Counter(words)


# Fetch comments
comments = get_video_comments(video_id)

# Analyze sentiments and calculate overall average
total_polarity = 0
total_subjectivity = 0
for comment in comments:
    polarity, subjectivity = analyze_sentiment(comment)
    total_polarity += polarity
    total_subjectivity += subjectivity

average_polarity = total_polarity / len(comments)
average_subjectivity = total_subjectivity / len(comments)

# Word frequency analysis
freq = word_frequency(comments)
most_common_words = freq.most_common(10)  # Adjust the number to show more or fewer common words

# Output the summary
print(f"Average Sentiment Polarity: {average_polarity:.2f}")
print(f"Average Sentiment Subjectivity: {average_subjectivity:.2f}")
print("Most common words in comments:")
for word, count in most_common_words:
    print(f"{word}: {count}")

# Visualization of sentiment (same as previous examples)
sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
for comment in comments:
    polarity, _ = analyze_sentiment(comment)
    if polarity > 0:
        sentiment_counts['positive'] += 1
    elif polarity == 0:
        sentiment_counts['neutral'] += 1
    else:
        sentiment_counts['negative'] += 1

labels = ['Positive', 'Neutral', 'Negative']
sizes = [sentiment_counts['positive'], sentiment_counts['neutral'], sentiment_counts['negative']]
colors = ['green', 'gray', 'red']
explode = (0.1, 0, 0)  # Emphasize Positive
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('Sentiment Analysis of YouTube Comments')
plt.show()
