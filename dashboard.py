import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    influencers_data = pd.read_csv("influencers_data.csv")
    detailed_sentiment_data = pd.read_csv("detailed_sentiment_analysis.csv")
    return influencers_data, detailed_sentiment_data

influencers_data, detailed_sentiment_data = load_data()

# Dashboard title
st.title("Influencer Marketing Sentiment Analysis Dashboard")
st.markdown("""
This dashboard helps you analyze influencer performance based on engagement metrics and sentiment analysis.  
You can explore influencer rankings, compare sentiment trends, and predict future engagement insights.
""")

# Sidebar for influencer selection
st.sidebar.header("Influencer Selection")
selected_influencer = st.sidebar.selectbox(
    "Choose an Influencer:",
    influencers_data["Channel Name"].unique()
)


# Display Influencer Summary
st.subheader(f"Overview of {selected_influencer}")
selected_data = influencers_data[influencers_data["Channel Name"] == selected_influencer]

st.write("**Key Metrics:**")
col1, col2, col3 = st.columns(3)
col1.metric("Subscriber Count", f"{selected_data['Subscriber Count'].values[0]:,}")
col2.metric("Avg Views/Video", f"{selected_data['Average Views per Video'].values[0]:,}")
col3.metric("Engagement Rate", f"{selected_data['Engagement Rate'].values[0]:.2f}%")

# Sentiment Distribution for the Influencer
st.subheader("Sentiment Distribution")
sentiment_data = detailed_sentiment_data[
    detailed_sentiment_data["Channel Name"] == selected_influencer
]

sentiment_counts = sentiment_data[["Positive", "Neutral", "Negative"]].sum()
fig_sentiment = px.pie(
    values=sentiment_counts,
    names=["Positive", "Neutral", "Negative"],
    title=f"Sentiment Distribution for {selected_influencer}",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_sentiment)

# Engagement Trends
st.subheader("Historical and Predicted Engagement Trends")
st.write("""
This chart compares historical engagement data with predicted trends for the selected influencer.
""")
engagement_data = sentiment_data.groupby("Video Title").agg({
    "Positive": "sum",
    "Neutral": "sum",
    "Negative": "sum"
}).reset_index()

fig_trends = px.bar(
    engagement_data,
    x="Video Title",
    y=["Positive", "Neutral", "Negative"],
    title=f"Engagement Trends for {selected_influencer}",
    labels={"value": "Comment Count", "Video Title": "Videos"},
    barmode="stack",
    color_discrete_sequence=px.colors.qualitative.G10
)
st.plotly_chart(fig_trends)

# Influencer Ranking Section
st.subheader("Influencer Rankings")
ranking_metric = st.selectbox(
    "Select Metric for Ranking:",
    ["Engagement Rate", "Sentiment Weighted Engagement", "Total Score"]
)

# Generate Ranking
ranked_data = influencers_data.sort_values(by=ranking_metric, ascending=False).reset_index(drop=True)
ranked_data["Rank"] = ranked_data.index + 1

# Display Top 10 Influencers
st.write(f"**Top 10 Influencers Ranked by {ranking_metric}:**")
st.dataframe(ranked_data[["Rank", "Channel Name", "Subscriber Count", ranking_metric]].head(10))

# Bar Chart for Rankings
st.subheader(f"Top Influencers by {ranking_metric}")
fig_ranking = px.bar(
    ranked_data.head(10),
    x="Channel Name",
    y=ranking_metric,
    color="Channel Name",
    title=f"Top 10 Influencers by {ranking_metric}",
    labels={"Channel Name": "Influencers", ranking_metric: ranking_metric},
    height=500
)
st.plotly_chart(fig_ranking)
# Footer
st.markdown("---")
st.markdown("**Created by [Your Name]**")
st.markdown("This project analyzes influencers' engagement and sentiment to help businesses choose the best-fit influencers for their campaigns.")
