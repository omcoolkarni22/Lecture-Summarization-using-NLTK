from flask import Flask, render_template, url_for, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import readtime
import spacy  # python -m spacy download en
nlp = spacy.load('en')


app = Flask(__name__, template_folder='templates')


def nltk_summarizer(raw_text):
    stopWords = set(stopwords.words("english"))
    word_frequencies = {}
    for word in nltk.word_tokenize(raw_text):
        if word not in stopWords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_list = nltk.sent_tokenize(raw_text)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary


@app.route('/')
def Home():
    return render_template(template_name_or_list='index.html', summary=None)


@app.route('/summarized', methods=['GET', 'POST'])
def summarized():
    if request.method == "POST":
        raw_text = request.form['raw_text']
        summary = nltk_summarizer(raw_text)
        raw_time = readtime.of_text(raw_text)
        time = readtime.of_text(summary)
        return render_template('index.html', summary=summary, raw_text=raw_text, time=time, raw_time=raw_time)


if __name__ == "__main__":
    app.run(debug=True)

