"""
═══════════════════════════════════════════════════════════════════════════
🎬 IMDB MOVIE DASHBOARD — STREAMLIT APP
═══════════════════════════════════════════════════════════════════════════

This file is a Streamlit web app that displays our movie data analysis
visualizations in a clean dashboard format.

HOW TO RUN THIS FILE:
  1. Open a terminal in this folder
  2. Type:  streamlit run streamlit_app.py
  3. Your browser will open automatically with the dashboard

Every line below is commented for beginners.
═══════════════════════════════════════════════════════════════════════════
"""

# ─────────────────────────────────────────────────────────
# SECTION 1: IMPORT THE LIBRARIES WE NEED
# ─────────────────────────────────────────────────────────

# streamlit — the library that builds the web app
# We always call it 'st' as a convention
import streamlit as st

# pandas — for working with our movie data (the CSV file)
import pandas as pd

# matplotlib — for making charts
import matplotlib.pyplot as plt

# seaborn — sits on top of matplotlib for prettier charts
import seaborn as sns

# numpy — for any number-crunching
import numpy as np


# ─────────────────────────────────────────────────────────
# SECTION 2: PAGE CONFIGURATION (set this BEFORE anything else)
# ─────────────────────────────────────────────────────────

# st.set_page_config customises the browser tab and overall layout
# This MUST be the first Streamlit command in the file
st.set_page_config(
    page_title="IMDB Movie Dashboard",   # title shown in the browser tab
    page_icon="🎬",                       # emoji icon in the tab
    layout="wide",                        # use the full width of the screen
    initial_sidebar_state="expanded",     # show the sidebar by default
)


# ─────────────────────────────────────────────────────────
# SECTION 3: LOAD THE DATA (with caching for speed)
# ─────────────────────────────────────────────────────────

# @st.cache_data tells Streamlit: "remember the result of this function"
# Without it, Streamlit would re-read the CSV every time the user interacts
# with the app, which is slow. With it, the data loads only ONCE.
@st.cache_data
def load_data():
    """Read the movie CSV and do the cleaning we did in the notebook."""
    # Read the CSV file. The path is relative to where streamlit run was started.
    df = pd.read_csv("../data/imdb_movies.csv")

    # Fill missing values — same as in the notebook
    df["runtime_minutes"] = df["runtime_minutes"].fillna(df["runtime_minutes"].median())
    df["budget_millions"] = df["budget_millions"].fillna(df["budget_millions"].median())

    # Return the cleaned DataFrame
    return df


# Call the function — Streamlit will load the data when the app starts
df = load_data()


# ─────────────────────────────────────────────────────────
# SECTION 4: PAGE TITLE & INTRODUCTION
# ─────────────────────────────────────────────────────────

# st.title — big heading at the top of the page
st.title("🎬 IMDB Movie Data Dashboard")

# st.markdown — write any text, supports formatting like **bold** and *italic*
st.markdown(
    "An interactive dashboard exploring 1000 movies — ratings, genres, "
    "revenue trends, and more. Use the **sidebar filters on the left** "
    "to drill into specific years and genres."
)

# Horizontal divider line
st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 5: SIDEBAR FILTERS (lets the user pick what to see)
# ─────────────────────────────────────────────────────────

# st.sidebar puts widgets in the left sidebar instead of the main page
st.sidebar.header("🔍 Filters")
st.sidebar.markdown("Adjust these to filter the data displayed on the right.")

# ── Filter 1: Year range slider ──
# st.slider creates a slider widget
# Arguments: label, min value, max value, default value (a tuple for range)
year_min = int(df["year"].min())
year_max = int(df["year"].max())

year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),       # default: full range
    step=1,
)

# ── Filter 2: Multi-select for genres ──
# st.multiselect lets the user pick multiple values from a list
all_genres = sorted(df["genre"].unique())

selected_genres = st.sidebar.multiselect(
    "Genres",
    options=all_genres,
    default=all_genres,               # default: all genres selected
)

# ── Filter 3: Minimum number of votes ──
# st.number_input lets the user type a number
min_votes = st.sidebar.number_input(
    "Minimum votes",
    min_value=0,
    max_value=int(df["votes"].max()),
    value=0,
    step=1000,
    help="Only show movies with at least this many votes",
)

# A simple help text at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tip: filters apply to ALL charts on the page. "
    "Click the 'X' in any filter widget to reset it."
)


# ─────────────────────────────────────────────────────────
# SECTION 6: APPLY THE FILTERS TO THE DATA
# ─────────────────────────────────────────────────────────

# Start from the full DataFrame and keep narrowing it down with conditions
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["genre"].isin(selected_genres)) &
    (df["votes"] >= min_votes)
]

# If the filters left nothing, warn the user and stop
if len(filtered_df) == 0:
    st.warning("⚠️ No movies match your filters. Try widening them.")
    st.stop()       # halt execution — nothing below will run


# ─────────────────────────────────────────────────────────
# SECTION 7: KEY METRICS ROW (the "scorecard" at the top)
# ─────────────────────────────────────────────────────────

# st.columns(N) creates N equal-width columns side by side
col1, col2, col3, col4 = st.columns(4)

# st.metric is a special widget for showing a big number with a label
with col1:
    st.metric(
        label="📽️ Total Movies",
        value=f"{len(filtered_df):,}",       # format with commas
    )

with col2:
    avg_rating = filtered_df["rating"].mean()
    st.metric(
        label="⭐ Average Rating",
        value=f"{avg_rating:.2f}",
    )

with col3:
    total_revenue = filtered_df["revenue_millions"].sum()
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}M",
    )

with col4:
    total_votes = filtered_df["votes"].sum()
    st.metric(
        label="🗳️ Total Votes",
        value=f"{total_votes:,}",
    )

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 8: VISUALIZATION 1 — TOP 10 HIGHEST RATED MOVIES
# ─────────────────────────────────────────────────────────

st.header("🏆 Top 10 Highest-Rated Movies")
st.markdown("Movies with at least 10,000 votes, sorted by rating.")

# Filter once more for votes threshold (the chart's own requirement)
popular = filtered_df[filtered_df["votes"] >= 10000]

if len(popular) > 0:
    top_10 = popular.sort_values("rating", ascending=False).head(10)

    # Create the matplotlib figure
    # fig is the whole chart area; ax is the actual plot inside it
    fig, ax = plt.subplots(figsize=(10, 6))

    # Horizontal bar chart
    ax.barh(top_10["title"], top_10["rating"],
            color="steelblue", edgecolor="navy")
    ax.invert_yaxis()        # #1 on top
    ax.set_xlabel("Rating (out of 10)")
    ax.set_ylabel("Movie Title")
    ax.set_title("Top 10 Highest-Rated Movies")

    # Annotate each bar
    for i, v in enumerate(top_10["rating"]):
        ax.text(v + 0.05, i, f"{v:.1f}", va="center", fontweight="bold")

    plt.tight_layout()
    # st.pyplot displays the matplotlib chart in the Streamlit app
    st.pyplot(fig)
    plt.close(fig)           # free memory
else:
    st.info("No movies in your filter have 10,000+ votes.")

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 9: VISUALIZATIONS 2 & 3 — SIDE BY SIDE
# ─────────────────────────────────────────────────────────

st.header("🎭 Genre Analysis")

# Two columns — one chart in each
left_col, right_col = st.columns(2)

# ── Left chart: Movies per genre ──
with left_col:
    st.subheader("Movies per Genre")
    genre_counts = filtered_df["genre"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = sns.color_palette("viridis", n_colors=len(genre_counts))
    ax.bar(genre_counts.index, genre_counts.values,
           color=colors, edgecolor="black")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Number of Movies")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ── Right chart: Average rating per genre ──
with right_col:
    st.subheader("Average Rating per Genre")
    avg_rating = filtered_df.groupby("genre")["rating"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = sns.color_palette("RdYlGn", n_colors=len(avg_rating))
    ax.bar(avg_rating.index, avg_rating.values,
           color=colors, edgecolor="black")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Rating")
    ax.set_ylim(0, 10)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 10: VISUALIZATION 4 — MOVIES PER YEAR (LINE CHART)
# ─────────────────────────────────────────────────────────

st.header("📅 Movies Released Per Year")
st.markdown("How movie production has changed over time.")

movies_per_year = filtered_df["year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(movies_per_year.index, movies_per_year.values,
        marker="o", linewidth=2, markersize=6,
        color="steelblue", markerfacecolor="orange", markeredgecolor="navy")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Movies")
ax.set_title("Movies Released Each Year")
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 11: VISUALIZATION 5 — RATING DISTRIBUTION (HISTOGRAM)
# ─────────────────────────────────────────────────────────

st.header("📊 Rating Distribution")
st.markdown("What's the typical rating? Is the data skewed?")

fig, ax = plt.subplots(figsize=(11, 5))
ax.hist(filtered_df["rating"], bins=20,
        color="coral", edgecolor="black", alpha=0.85)

mean_r = filtered_df["rating"].mean()
median_r = filtered_df["rating"].median()

ax.axvline(mean_r, color="red", linestyle="--", linewidth=2,
           label=f"Mean = {mean_r:.2f}")
ax.axvline(median_r, color="blue", linestyle=":", linewidth=2,
           label=f"Median = {median_r:.2f}")
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Movies")
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 12: VISUALIZATIONS 6 & 7 — BUDGET vs REVENUE + CORRELATION
# ─────────────────────────────────────────────────────────

st.header("💰 Financial Analysis")

left_col, right_col = st.columns(2)

# ── Budget vs Revenue scatter ──
with left_col:
    st.subheader("Budget vs Revenue")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(filtered_df["budget_millions"], filtered_df["revenue_millions"],
               alpha=0.5, s=40, color="teal", edgecolor="navy")

    # Reference line: break-even (revenue = budget)
    max_val = max(filtered_df["budget_millions"].max(),
                  filtered_df["revenue_millions"].max())
    ax.plot([0, max_val], [0, max_val], "r--", linewidth=1.5,
            label="Break-even line")
    ax.set_xlabel("Budget (Million $)")
    ax.set_ylabel("Revenue (Million $)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    corr = filtered_df["budget_millions"].corr(filtered_df["revenue_millions"])
    st.caption(f"Correlation between budget and revenue: **{corr:.3f}**")

# ── Correlation heatmap ──
with right_col:
    st.subheader("Correlation Heatmap")
    numeric_cols = ["year", "runtime_minutes", "rating", "votes",
                    "budget_millions", "revenue_millions"]
    corr_matrix = filtered_df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f",
                cmap="coolwarm", center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5, ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 13: VISUALIZATION 8 — RATING BY GENRE (BOXPLOT)
# ─────────────────────────────────────────────────────────

st.header("📦 Rating Spread by Genre")
st.markdown("Boxplots show the median, range, and outliers for each genre.")

# Order genres by median rating
genre_order = filtered_df.groupby("genre")["rating"].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=filtered_df, x="genre", y="rating",
            order=genre_order, palette="Set2", ax=ax)
ax.set_xlabel("Genre")
ax.set_ylabel("Rating")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 14: VISUALIZATION 9 — REVENUE BY GENRE (PIE CHART)
# ─────────────────────────────────────────────────────────

st.header("🥧 Revenue Share by Genre")

revenue_by_genre = filtered_df.groupby("genre")["revenue_millions"].sum().sort_values(ascending=False)

# Two columns: pie chart left, table right
pie_col, table_col = st.columns([2, 1])

with pie_col:
    fig, ax = plt.subplots(figsize=(8, 8))
    colors_pie = sns.color_palette("Set3", n_colors=len(revenue_by_genre))
    ax.pie(revenue_by_genre.values,
           labels=revenue_by_genre.index,
           autopct="%1.1f%%",
           colors=colors_pie,
           startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 2})
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with table_col:
    st.subheader("Revenue by Genre")
    revenue_df = revenue_by_genre.reset_index()
    revenue_df.columns = ["Genre", "Revenue (M$)"]
    revenue_df["Revenue (M$)"] = revenue_df["Revenue (M$)"].round(1)
    # st.dataframe displays a sortable, scrollable table
    st.dataframe(revenue_df, use_container_width=True, hide_index=True)

st.divider()


# ─────────────────────────────────────────────────────────
# SECTION 15: RAW DATA EXPLORER (collapsible)
# ─────────────────────────────────────────────────────────

# st.expander creates a collapsible section — clean way to hide bulky content
with st.expander("🔍 Show the raw data (click to expand)"):
    st.markdown(f"Showing {len(filtered_df)} movies based on your filters.")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────
# SECTION 16: FOOTER
# ─────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "Built with ❤️ using **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn**. "
    "Data: Synthetic IMDB-style movie dataset (1000 movies)."
)
