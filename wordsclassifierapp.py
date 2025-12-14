import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline, AutoTokenizer

# Load Models  models load pannanum
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model_name)
aspect_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Load tokenizer for truncation
tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)

# Aspect Labels aspect values detect panna
labels = ["Price", "Shipping", "Customer Service", "Ease of Use"]

st.title("Customer Feedback Sentiment Analyzer")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    
    if "reviews.text" not in df.columns:
        st.error("CSV must contain a column named 'reviews.text'")
    elif "reviews.date" not in df.columns:
        st.warning("No 'reviews.date' column found → time-series chart will be skipped.")
        has_date = False
    else:
        has_date = True

    st.success("CSV Loaded Successfully!")

    review_data = df["reviews.text"].dropna().astype(str)

    # === NEW: Prepare date column (if exists) ===
    if has_date:
        review_dates = pd.to_datetime(df["reviews.date"], errors='coerce')
        
        if "name" in df.columns:
            product_name = df["name"].iloc[0]
            st.subheader(f"Product: {product_name}")

    sentiments = []
    sentiment_scores = []   # for time-series (0 = Neg, 0.5 = Neutral, 1 = Pos)
    subjects = []

    with st.spinner("Analyzing reviews, please wait..."):
        for review in review_data:
            # Truncate review to max 512 tokens
            tokens = tokenizer.encode(review, max_length=512, truncation=True)
            truncated_review = tokenizer.decode(tokens, skip_special_tokens=True)

            # Sentiment Analysis
            sentiment_result = sentiment_classifier(truncated_review)[0]
            sentiment_label = sentiment_result['label']

            if sentiment_label == "NEGATIVE":
                sentiment_label = "Negative"
                sentiment_scores.append(0)
            elif sentiment_label == "POSITIVE":
                sentiment_label = "Positive"
                sentiment_scores.append(1)
            else:
                sentiment_label = "Neutral"
                sentiment_scores.append(0.5)

            sentiments.append(sentiment_label)

            # Aspect Detection
            aspect_result = aspect_classifier(truncated_review, labels, multi_label=True)
            top_aspect = aspect_result["labels"][0]
            subjects.append(top_aspect)

    # Build result dataframe
    result_df = pd.DataFrame({
        "Review": review_data,
        "Sentiment": sentiments,
        "Subject": subjects
    })

    # Add date & score only if date column exists
    if has_date:
        result_df["Date"] = review_dates
        result_df["Sentiment Score"] = sentiment_scores
        result_df = result_df.sort_values(by="Date").reset_index(drop=True)

    st.subheader("Predicted Results")
    st.dataframe(result_df)

  
    if has_date and not result_df["Date"].isna().all():
        st.subheader("Sentiment Trend Over Time")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(result_df["Date"], result_df["Sentiment Score"], 
                 marker="o", linestyle="-", color="#1f77b4")
        ax3.set_xlabel("Review Date")
        ax3.set_ylabel("Sentiment Score\n(0 = Negative, 0.5 = Neutral, 1 = Positive)")
        ax3.set_title("Sentiment Trend Over Time")
        ax3.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig3)

   
    st.subheader("Sentiment Distribution")
    sentiment_counts = result_df["Sentiment"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=90)
    ax1.axis('equal')
    ax1.set_title("Sentiment Split")
    st.pyplot(fig1)


    st.subheader("Aspect Category Count")
    aspect_counts = result_df["Subject"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(aspect_counts.index, aspect_counts, color="#ff7f0e")
    ax2.set_xlabel("Aspect")
    ax2.set_ylabel("Count")
    ax2.set_title("Aspect Distribution")
    st.pyplot(fig2)

   
    csv_download = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Results CSV",
        data=csv_download,
        file_name="analyzed_reviews.csv",
        mime="text/csv"
    )
