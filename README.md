# 🚧 TwitterDataAnalyzer

**Real-time detection of road traffic accidents — location, severity, and injury details — mined directly from social media, in production research sponsored by the NIH.**

This project is the engineering implementation behind the peer-reviewed paper *["Exploring the roles of social media data to identify the locations and severity of road traffic accidents"](https://ieeexplore.ieee.org/)* (IEEE Journal of Biomedical and Health Informatics), co-authored during my time as a Software Engineer at The University of Texas at Dallas.

> The core idea: phone-in accident reports are slow and often vague about severity and exact location. People post about accidents on Twitter *before* it hits the news — this pipeline listens continuously, figures out which tweets are real accidents (vs. "I left my keys by accident"), groups the ones talking about the same crash, summarizes them, geolocates them down to street level, and estimates how severe the accident is — all within minutes of it happening.

---

## 📊 Results at a glance

| Metric | Result |
|---|---|
| Tweets processed | **100,000+**, collected continuously across 5 cities |
| Daily accident-related tweet volume | ~42,000/day (up to 17,000/day in Dallas alone) |
| Best street-level geolocation accuracy | **86.9%** (Houston, via Google Geocoder) |
| Best city-level geolocation accuracy | **97.0%** (Houston) |
| Severity classification accuracy (SVM) | **86.9%** |
| Ground-truth validation | Cross-checked against **1,300+ official Dallas Police Department accident reports** — 63% match rate |
| Research output | **2 peer-reviewed IEEE papers** |

---

## 🧠 How it works

The system runs a 6-stage NLP pipeline, operating in two modes:

- **Active mode** — continuously polls the Twitter Search API every 2 minutes for accident-related keywords and geo-bounded regions, and surfaces new incidents as they're detected.
- **Passive mode** — exposes a REST API that lets an external system (e.g. a 911 dispatch tool) trigger a targeted search for tweets near a specific time and location, when it already has a lead on an incident.

```
Twitter API → Filtration (query-based) → Classification (BERT / NB / SVM / HAN)
     → Clustering (semantic + temporal + spatial) → Summarization (word-graph)
     → Location Extraction (Semantic Role Labeling + Google Geocoder)
     → Severity Detection (verb-argument extraction + ML classifiers)
     → Visualization (Elasticsearch / Kibana) + Public API
```

**1. Collection** — `Twitter_Searcher.py` polls the Twitter Search API on a schedule (via `tweepy`), pulling ~100 new tweets containing "accident" every 2 minutes across multiple cities, deduplicating against existing MongoDB records before storing.

**2. Classification** — Distinguishes genuine accident reports ("*Ghastly accident on I-45, 2 dead*") from unrelated use of the word ("*I left my wallet in the office by accident*") using a fine-tuned **BERT** classifier, benchmarked against Naive Bayes, SVM, and Hierarchical Attention Network (HAN) models.

**3. Clustering** — Groups tweets describing the *same* accident using an incremental online clustering approach across three dimensions: semantic similarity (word2vec), temporal proximity (LRU-based cluster eviction), and spatial proximity — no fixed number of clusters required.

**4. Summarization** — Collapses a cluster of near-duplicate tweets into a single, human-readable abstractive summary using a word-graph + bigram traversal approach, scored against a tri-gram language model trained on the COCA corpus (via KenLM).

**5. Geolocation** — Extracts accident locations from free text using **Semantic Role Labeling (AllenNLP)** to isolate `ARG-LOC` phrases (e.g. "*between Austin and Gatineau*"), cross-referenced with tweet/user metadata and Google's Geocoder, resolving down to street level where possible.

**6. Severity Detection** — Identifies casualty/injury language via a seeded, iteratively-expanded verb list ("*injure*", "*die*", "*kill*"...) matched through SRL argument extraction, then classifies severity (Severe / Non-Severe / Non-Accident) with ML models.

Processed data is indexed into **Elasticsearch** and visualized in **Kibana**, and served through a public API for downstream consumption.

<p align="center">
  <img src="https://user-images.githubusercontent.com/52136572/169713702-0ff5c44e-2bb1-4b67-89aa-a1e772bfec37.png" width="700" alt="Pipeline architecture diagram">
</p>

<p align="center"><em>Geolocated accident data as visualized in Kibana:</em></p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/52136572/170064388-272ad843-78a8-499b-a352-fdc4b97e832c.png" width="700" alt="Kibana geolocation visualization">
</p>

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data collection | Python, Tweepy, Twitter Search API |
| Storage | MongoDB, Elasticsearch |
| NLP / ML | BERT, AllenNLP (Semantic Role Labeling), Naive Bayes, SVM, HAN, word2vec, KenLM |
| Geolocation | Google Geocoder, Nominatim |
| Visualization | Kibana |
| Messaging | Apache Kafka (inter-module communication) |
| Infra | Ran on a Dell R740xd — 40 cores / 96GB RAM, processing tweets from 5 cities across the US and Nigeria |

---

## 📂 Repo structure

| File | Purpose |
|---|---|
| `Twitter_Searcher.py` | Main entry point — active-mode collection, deduplication, and MongoDB/Elasticsearch storage |
| `Old_Twitter_Searcher.py` | Historical tweet collection using `tweepy` + `GetOldTweets3` for a fixed date range |
| `Old_Twitter_Searcher_using_twitter_api.py` | Variant using the official Twitter API for historical pulls |
| `Find_tweets_within_incident_radius.py` | Passive-mode search — pulls tweets within a geographic radius of a reported incident |
| `Organize_tweets_and_incidents.py` | Clusters and structures raw tweets into incident records |
| `get_min_number_of_twitter_requests.py` | Utility for minimizing API call volume against rate limits |
| `tweets.json` / `tweets.csv` | Sample collected output |
| `cliff.json` / `cliff_Dallas.json` | CLIFF-CLAVIN geoparser output for text-based location extraction |
| `reported_incidents_v2.json` / `output.json` | Processed incident records |

---

## 📄 Publications

This project produced the following peer-reviewed research:

- **Salam, S., Kim, D., Islam, M. S., Ahmed, F., Khan, L., & Nwariaku, O.** — *"Exploring the roles of social media data to identify the locations and severity of road traffic accidents"* — IEEE Journal of Biomedical and Health Informatics.
- A second paper published at the **IEEE Blockchain and Cryptocurrency** conference.

---

## 🚀 Running it

1. Install dependencies: `tweepy`, `pymongo`, `elasticsearch`, `geopy`, `schedule`
2. Add Twitter API credentials (`apiKey`, `apiKey_Secret`, `accessToken`, `accessToken_Secret`) and your Elasticsearch host to `Twitter_Searcher.py`
3. Start a local MongoDB instance
4. Run `python Twitter_Searcher.py` to kick off active-mode collection for the configured cities, or wire up `Find_tweets_within_incident_radius.py` for passive/on-demand lookups

> ⚠️ This project predates the shutdown of Twitter's free Search API v1.1 tier used here (`tweepy.API`), so live collection requires an active elevated/paid API tier to run today.

---

## 🌍 Why this matters

The WHO estimates road traffic accidents kill over 39,000 people a year in Nigeria alone, with the highest mortality rates in regions where emergency response infrastructure is weakest. Faster, more accurate situational awareness — location, severity, injury count — means faster triage and resource allocation for the agencies trying to save lives. That's the problem this project set out to help solve.
