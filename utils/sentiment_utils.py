from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_text_sentiment(text):
    """Analyze a single piece of text."""
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return {"sentiment": sentiment, "scores": scores, "compound": compound}


def analyze_sentiment_from_history(chat_history):
    """
    Analyze sentiment from full conversation history.
    Returns aggregated stats and overall mood.
    """
    user_messages = [
        m["content"] for m in chat_history
        if m["role"] == "user"
    ]

    if not user_messages:
        return {
            "overall": "N/A",
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "summary": "No messages yet"
        }

    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    compounds = []

    for text in user_messages:
        result = analyze_text_sentiment(text)
        counts[result["sentiment"]] += 1
        compounds.append(result["compound"])

    avg_compound = sum(compounds) / len(compounds)
    dominant = max(counts, key=counts.get)

    # Build a human-readable summary
    total = len(user_messages)
    pos_pct = int(counts["Positive"] / total * 100)
    neg_pct = int(counts["Negative"] / total * 100)

    if avg_compound >= 0.2:
        summary = f"You seem engaged and confident — {pos_pct}% of messages are positive."
    elif avg_compound >= 0.05:
        summary = f"Generally positive learning mood across {total} messages."
    elif avg_compound <= -0.2:
        summary = f"Some frustration detected — {neg_pct}% of messages are negative. Keep going!"
    elif avg_compound <= -0.05:
        summary = "Mixed feelings — normal when learning challenging topics."
    else:
        summary = "Neutral, focused learning tone across your sessions."

    return {
        "overall": dominant,
        "positive": counts["Positive"],
        "negative": counts["Negative"],
        "neutral": counts["Neutral"],
        "avg_compound": round(avg_compound, 3),
        "summary": summary,
        "total_analyzed": total
    }
