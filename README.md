# 🎬 IMDB Movie Data Analysis & Dashboard

> A complete data analytics project: explore 1000 movies, find patterns, and present findings in an interactive Streamlit dashboard.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/streamlit-1.x-red.svg)]()
[![Pandas](https://img.shields.io/badge/pandas-2.x-green.svg)]()

---

## 📋 Project Overview

This project demonstrates the **complete data analytics workflow**:

1. **Load** an IMDB-style movie dataset (1000 movies)
2. **Explore** the data — shape, types, missing values
3. **Clean** missing values
4. **Analyze** 10 different questions about ratings, genres, revenue, and trends
5. **Visualize** the findings with 10 different chart types
6. **Present** the results in an interactive Streamlit dashboard

---

## 🗂️ Project Structure

```
imdb_project/
├── README.md                    ← you are here
├── requirements.txt             ← Python libraries needed
├── .gitignore                   ← files Git should ignore
│
├── data/
│   └── imdb_movies.csv          ← 1000 movies dataset
│
├── notebooks/
│   └── imdb_analysis.ipynb      ← complete Jupyter analysis
│
├── app/
│   └── streamlit_app.py         ← interactive dashboard
│
└── docs/
    └── setup_guide.pdf          ← step-by-step setup guide
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/imdb-movie-analysis.git
cd imdb-movie-analysis
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the analysis notebook
```bash
jupyter notebook notebooks/imdb_analysis.ipynb
```

### 6. Run the Streamlit dashboard
```bash
cd app
streamlit run streamlit_app.py
```

Your browser will open at `http://localhost:8501` showing the dashboard.

📖 **For step-by-step instructions with screenshots and explanations of every line of code, open `docs/setup_guide.pdf`.**

---

## 📊 What's Inside

### The Notebook (`imdb_analysis.ipynb`)
- 15 analytical steps from data loading to insights
- Line-by-line explanations of every code cell
- 10 different visualizations
- Final summary with key findings

### The Streamlit App (`streamlit_app.py`)
- 9 interactive visualizations
- Three sidebar filters: year range, genres, minimum votes
- Live metrics that update with filters
- A collapsible raw-data table

### The Dataset (`imdb_movies.csv`)
| Column | Description |
|---|---|
| title | Movie title |
| year | Release year (1990–2024) |
| genre | Action, Drama, Comedy, etc. |
| director | Director name |
| runtime_minutes | Movie length |
| rating | IMDB-style rating (1–10) |
| votes | Number of votes |
| budget_millions | Production budget (millions $) |
| revenue_millions | Total revenue (millions $) |

---

## 🛠️ Technologies Used

- **Python 3.10+** — programming language
- **Pandas** — data manipulation
- **NumPy** — numerical operations
- **Matplotlib** — base plotting
- **Seaborn** — statistical plots
- **Jupyter** — interactive notebooks
- **Streamlit** — interactive dashboard

---

## 📈 Key Findings (from the analysis)

- The **most common genre** is Action, followed by Drama and Comedy
- **Animation** has the highest average rating among genres
- Budget and revenue show a **positive correlation** — bigger budgets tend to make more money
- Movies released after 2010 dominate the dataset

For more findings, run the notebook!

---

## 🎯 Skills Demonstrated

By exploring this project, you can see hands-on use of:

- Loading and exploring real datasets
- Handling missing values
- Filtering and grouping data with Pandas
- Creating diverse visualizations (bar, line, scatter, histogram, heatmap, boxplot, pie)
- Building an interactive web dashboard
- Writing clean, well-commented code

---

## 📝 License

This project is open source. Feel free to fork it, modify it, and use it as the basis for your own portfolio piece.

---

## 🙋 Author

Created as a learning project. Replace this section with your own name, links to your portfolio, GitHub, and LinkedIn before publishing!
