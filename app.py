from flask import Flask, render_template, request
from textblob import TextBlob
import textstat
import nltk

# Ensure NLTK corpora are downloaded at runtime
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

def analyze_essay(text):
    blob = TextBlob(text)

    # Word and sentence counts
    word_count = len(blob.words)
    sentence_count = len(blob.sentences)

    # Sentiment analysis
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)

    # Readability score (Flesch Reading Ease)
    readability = round(textstat.flesch_reading_ease(text), 2)

    # Grade level
    grade_level = textstat.text_standard(text)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "readability": readability,
        "grade_level": grade_level
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        essay_text = request.form["essay"]
        result = analyze_essay(essay_text)
        return render_template("index.html", result=result, essay=essay_text)
    return render_template("index.html", result=None, essay="")

if __name__ == "__main__":
    app.run(debug=True)
