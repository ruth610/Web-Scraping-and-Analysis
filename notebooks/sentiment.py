import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def load_data(filepath):
    """Load dataset with error handling."""
    try:
        df = pd.read_csv(filepath)
        print("✔ Data loaded successfully:", filepath)
        return df
    except FileNotFoundError:
        print("❌ ERROR: File not found:", filepath)
        return pd.DataFrame()
    except Exception as e:
        print("❌ ERROR loading file:", str(e))
        return pd.DataFrame()

def clean_text(text):
    """Basic text cleaning."""
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def compute_sentiment(df):
    """Run VADER sentiment scoring."""
    analyzer = SentimentIntensityAnalyzer()
    df['vader'] = df['review'].apply(lambda t: analyzer.polarity_scores(str(t)))
    df['sentiment_score'] = df['vader'].apply(lambda v: v['compound'])
    df['sentiment_label'] = df['sentiment_score'].apply(
        lambda s: "positive" if s >= 0.05 else ("negative" if s <= -0.05 else "neutral")
    )
    return df

def summarize_sentiment(df):
    """Print insights you can place in your report."""
    print("\n=== SENTIMENT DISTRIBUTION ===")
    print(df['sentiment_label'].value_counts())

    print("\n=== AVERAGE SENTIMENT SCORE ===")
    print(df['sentiment_score'].mean())

    print("\n=== SAMPLE POSITIVE REVIEWS ===")
    print(df[df['sentiment_label'] == 'positive']['review'].head(3).to_string(index=False))

    print("\n=== SAMPLE NEGATIVE REVIEWS ===")
    print(df[df['sentiment_label'] == 'negative']['review'].head(3).to_string(index=False))


def main():
    print("=== Running Final Analysis Pipeline ===")

    # Load cleaned review file
    df = load_data("reviews_clean.csv")

    if df.empty:
        return

    # Ensure required column exists
    if "review" not in df.columns:
        print("❌ ERROR: The dataset must contain a 'review' column.")
        return

    # Clean review text
    df['clean_review'] = df['review'].apply(clean_text)

    # Compute sentiment
    df = compute_sentiment(df)

    # Summaries (for your report)
    summarize_sentiment(df)

    # Save output
    df.to_csv("reviews_with_sentiment.csv", index=False)
    print("\n✔ Saved: reviews_with_sentiment.csv")

if __name__ == "__main__":
    main()
