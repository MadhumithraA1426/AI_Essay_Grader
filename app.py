from flask import Flask, render_template, request
from textblob import TextBlob
import textstat
import nltk

# Auto-download required corpora if missing (important for Render & new setups)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

def analyze_essay(text):
    blob = TextBlob(text)

    # Basic metrics
    word_count = len(blob.words)
    sentence_count = len(blob.sentences)

    # Correct grammar/spelling
    corrected_text = str(blob.correct())

    # Count spelling errors (words changed)
    spelling_errors = sum(1 for word in blob.words if word.lower() not in corrected_text.lower())

    # Readability score
    readability = textstat.flesch_reading_ease(text)

    # Sentiment (polarity: -1 to 1, subjectivity: 0 to 1)
    sentiment = blob.sentiment

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "corrected_text": corrected_text,
        "spelling_errors": spelling_errors,
        "readability": readability,
        "sentiment": {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        }
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    essay_text = ""
    if request.method == "POST":
        essay_text = request.form["essay"]
        result = analyze_essay(essay_text)
    return render_template("index.html", result=result, essay_text=essay_text)

if __name__ == "__main__":
    app.run(debug=True)
