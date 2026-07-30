# 🚧 TwitterDataAnalyzer

**Real-time detection of road traffic accidents — location, severity, and injury details — mined directly from social media.**

This project collects tweets in real time, filters out the ones that aren't actually about a crash, groups tweets describing the same accident, and extracts the location and severity of the incident. It's the engineering implementation behind a peer-reviewed paper, *["Exploring the roles of social media data to identify the locations and severity of road traffic accidents"](https://ieeexplore.ieee.org/)* (IEEE Journal of Biomedical and Health Informatics), built as a research project sponsored by the NIH.

<p align="center">
  <img src="https://user-images.githubusercontent.com/52136572/169713702-0ff5c44e-2bb1-4b67-89aa-a1e772bfec37.png" width="650" alt="Pipeline architecture diagram">
</p>

<p align="center"><em>Geolocated accident data visualized in Kibana:</em></p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/52136572/170064388-272ad843-78a8-499b-a352-fdc4b97e832c.png" width="650" alt="Kibana geolocation visualization">
</p>

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

---

## 🛠️ Built With

- **Python** · **Tweepy** — real-time & historical tweet collection via the Twitter API
- **BERT** · **AllenNLP (Semantic Role Labeling)** — accident classification and location/severity extraction from text
- **MongoDB** — storage and deduplication
- **Elasticsearch** · **Kibana** — indexing and geospatial visualization
- **Google Geocoder** — text-to-location resolution
- **Apache Kafka** — communication between pipeline modules

---

## 🌍 Why This Matters

Phone-in accident reports are slow and often vague about severity and exact location — but people post about crashes on social media before it ever reaches the news. The WHO estimates road traffic accidents kill tens of thousands of people a year in regions with the least developed emergency response infrastructure. Faster, more accurate situational awareness means faster triage and better-allocated resources for the agencies trying to save lives — that's the problem this project set out to help solve.
