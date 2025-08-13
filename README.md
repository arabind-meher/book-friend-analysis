# Book Friend — Analysis

This repository contains the **data processing, NLP, and recommendation workflow** for the Book Friend project.  
The pipeline begins with **raw data in MongoDB**, followed by **data cleaning, feature engineering, sentiment analysis, and review summarization**.  
The processed and enriched data is then used for **recommendation generation** and stored in **PostgreSQL** for further use.

---

## 📊 Workflow Diagram

```
MongoDB 
   ↓
Data Cleaning & Feature Engineering
   ↓
Sentiment Analysis
   ↓
Review Summarization
   ↓
Recommendation System
   ↓
PostgreSQL
```

---

## 📂 Repository Structure

```
book-friend-analysis/
├─ analysis/                  
│  ├─ 01_metadata.ipynb             # Explore and inspect book metadata from MongoDB
│  ├─ 02_reviews.ipynb              # Analyze and clean review data
│  ├─ 03_sentiment_analysis.ipynb   # Assign sentiment scores to reviews
│  ├─ 04_review_summarizer.ipynb    # Summarize book reviews
│  ├─ 05_migrate.ipynb              # Prepare and migrate final data to PostgreSQL
│  └─ 06_recommendation.ipynb       # Build and test recommendation logic
│
├─ core/
│  ├─ __init__.py
│  └─ config.py                     # Central configuration (e.g., DB URIs, constants)
│
├─ db/
│  ├─ sql/
│  │  └─ 001_schema.sql             # SQL schema for PostgreSQL tables
│  ├─ __init__.py
│  ├─ mongo.py                      # MongoDB connection and queries
│  └─ postgres.py                   # PostgreSQL connection and data insertion
│
├─ models/
│  ├─ __init__.py
│  └─ users.py                      # User-related data handling
│
├─ nlp/
│  ├─ __init__.py
│  ├─ review_summarizer.py          # Functions for review summarization
│  └─ sentiment_analysis.py         # Functions for sentiment scoring
│
├─ main.py                          # Entry point for orchestrating workflows
├─ pyproject.toml                   # Project dependencies and metadata
└─ requirements.txt                 # Alternative dependency list
```

---

## 🔄 Data Flow

1. **Extract** — Retrieve raw book metadata and review data directly from **MongoDB** collections.

2. **Transform** — Apply data cleaning, enrichment, and feature engineering:
   - Remove duplicates, normalize text, and handle missing values.
   - Perform **NLP-based sentiment analysis** on reviews to assign a positive sentiment score.
   - Generate concise **review summaries** using transformer-based models.
   - Build additional features for use in the recommendation engine.

3. **Load** — Insert the fully processed and feature-enriched datasets into **PostgreSQL** using the schema defined in `db/sql/001_schema.sql`.

---

## 📊 NLP Components

### **1. Sentiment Analysis**
- **Implementation**: `nlp/sentiment_analysis.py`
- **Model**: [siebert/sentiment-roberta-large-english](https://huggingface.co/siebert/sentiment-roberta-large-english) from Hugging Face Transformers.
- **Features**:
  - Processes reviews with tokenization and handles long text by chunking with a stride.
  - Produces a probability score `P(positive)` ∈ [0, 1] for each review.
  - Computes mean sentiment per book or user’s reviews.
  - Uses `torch.autocast` for mixed precision inference on GPU.
  - Outputs can be normalized with `MinMaxScaler` for integration into recommendation scoring.

**Usage example**:
```python
from nlp.sentiment_analysis import SentimentModel

model = SentimentModel(device=0)
scores = model.get_scores(["Great book!", "Not my taste."])
mean_sentiment = model.mean_score(scores)
```

### **2. Review Summarization**
- **Implementation**: `nlp/review_summarizer.py`
- **Model**: Default [t5-small](https://huggingface.co/t5-small) summarization pipeline from Hugging Face (configurable).
- **Features**:
  - Joins multiple reviews and trims to a safe word limit (~250 words) for summarization.
  - Cleans summaries (lowercasing, removing extra spaces, fixing punctuation, stripping reviewer names).
  - Supports single or batch summarization (`summarize_one` / `summarize_many`).
  - Batch processing for GPU acceleration.

**Usage example**:
```python
from nlp.review_summarizer import ReviewSummarizer

summarizer = ReviewSummarizer(model_name="t5-small", device=0)
summary = summarizer.summarize_one(["I loved the plot.", "Characters were amazing!"])
```

### **3. Recommendation System (NLP Integration)**
- **Location**: `analysis/06_recommendation.ipynb`
- **Approach**:
  - Content-based recommendation uses textual features from book metadata and user reviews.
  - **Sentiment scores** are used to boost items with higher positive sentiment.
  - **Summaries** provide concise context for each recommendation, making results more interpretable.
  - Candidate ranking may combine content similarity (e.g., TF-IDF cosine similarity) with sentiment-based re-ranking.

---

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/arabind-meher/book-friend-analysis.git
   cd book-friend-analysis
   ```

2. **Install dependencies**
   - Using `uv`:
     ```bash
     uv sync
     ```
   - Or with pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure environment**
   Create a `.env` file in the repo root:
   ```env
   MONGODB_URI=mongodb://localhost:27017
   MONGO_DB_NAME=book_friend
   POSTGRES_URI=postgresql://user:password@localhost:5432/book_friend
   ```

---

## 🛠 Usage

- **Run interactively**:  
  Open the notebooks in `analysis/` and execute them sequentially in the following order:
  1. `01_metadata.ipynb`
  2. `02_reviews.ipynb`
  3. `03_sentiment_analysis.ipynb`
  4. `04_review_summarizer.ipynb`
  5. `05_migrate.ipynb`
  6. `06_recommendation.ipynb`

Each notebook builds on the outputs of the previous one, so they should be run in sequence for the full pipeline.

---

## 📦 Technologies

- **Databases**: MongoDB (source), PostgreSQL (destination)
- **Data Processing**: pandas, numpy
- **NLP & ML**: scikit-learn, Hugging Face Transformers, NLTK, spaCy
- **Visualization**: matplotlib, seaborn
- **Development**: Jupyter Notebook

---

## 📄 License

This project is for academic purposes only.