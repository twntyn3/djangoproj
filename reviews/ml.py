import joblib
from pathlib import Path
from functools import lru_cache
import re

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"
VEC_PATH = ML_DIR / "vectorizer.joblib"
MODEL_PATH = ML_DIR / "svm_model.joblib"

# --- Simple word-level booster rules ---
POSITIVE_WORDS = {
    "nice", "nice one", "good", "great", "awesome", "excellent",
    "love", "amazing", "cool", "wonderful", "fantastic"
}

NEGATIVE_WORDS = {
    "shit", "terrible", "awful", "bad", "boring",
    "hate", "worst", "disappointing", "sucks"
}


def apply_rules(text: str):
    """Fast rule-based sentiment boost before ML model."""
    t = text.lower().strip()

    # Direct full-phrase match
    if t in POSITIVE_WORDS:
        return 1
    if t in NEGATIVE_WORDS:
        return 0

    # Word contains any positive keyword
    for w in POSITIVE_WORDS:
        if w in t:
            return 1

    # Word contains any negative keyword
    for w in NEGATIVE_WORDS:
        if w in t:
            return 0

    return None  # No rule match → use ML


@lru_cache(maxsize=1)
def get_vectorizer():
    if not VEC_PATH.exists() or not MODEL_PATH.exists():
        train_tiny_model()
    return joblib.load(VEC_PATH)


@lru_cache(maxsize=1)
def get_model():
    if not VEC_PATH.exists() or not MODEL_PATH.exists():
        train_tiny_model()
    return joblib.load(MODEL_PATH)


def predict_sentiment(text: str) -> bool:
    # 1) Rule-based shortcut (always correct on simple cases)
    rule = apply_rules(text)
    if rule is not None:
        return bool(rule)

    # 2) ML model for all other cases
    vec = get_vectorizer().transform([text])
    pred = get_model().predict(vec)[0]
    return bool(pred)


def train_tiny_model():
    """Train small but good TF-IDF + SVM model."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import make_pipeline
    ML_DIR.mkdir(exist_ok=True)

    texts = [
        # Positive
        "I loved this movie, it was fantastic and heartwarming",
        "What a masterpiece! Brilliant acting and story",
        "Absolutely wonderful film, highly recommend it",
        "Great direction and superb soundtrack",
        "It made me smile the whole time, amazing",
        "An excellent experience, powerful and moving",
        "This was a great movie, really enjoyed it",
        "Nice film, very pleasant and fun",
        "I really liked this movie",
        "Such a fun and engaging film",
        "This movie was great, I will watch it again",
        "Beautiful story and great cinematography",

        # Negative
        "Terrible movie, I hated every minute",
        "Awful acting and a boring script",
        "Worst film ever, complete waste of time",
        "Disappointing and poorly made",
        "I regret watching this, not good",
        "Bad pacing and horrible dialogues",
        "This movie sucked",
        "Really bad movie, wouldn't recommend",
        "It was boring and predictable",
        "One of the worst films I've ever seen",
        "Complete trash, hated it",
        "Terrible plot and bad acting",
    ]

    y = [
        1,1,1,1,1,1,1,1,1,1,1,1,
        0,0,0,0,0,0,0,0,0,0,0,0,
    ]

    vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1)
    model = LinearSVC()

    pipe = make_pipeline(vectorizer, model)
    pipe.fit(texts, y)

    joblib.dump(pipe.named_steps["tfidfvectorizer"], VEC_PATH)
    joblib.dump(pipe.named_steps["linearsvc"], MODEL_PATH)
