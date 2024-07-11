import numpy as np
import unicodedata
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

class NaiveBayesLanguageIdentifier:
    def __init__(self, n=20):
        self.n = n
        self.vocab = set()
        self.class_word_counts = defaultdict(self.default_dict_factory)
        self.class_counts = defaultdict(int)
        self.stop_words = defaultdict(set)
        self.tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, n))

    def default_dict_factory(self):
        return defaultdict(int)
    
    def _normalize_text(self, text):
        normalized_text = unicodedata.normalize('NFKD', text).encode('utf-8','ignore').decode('utf-8')
        return normalized_text
    
    def _clean_text(self, text):
        cleaned_text = text.lower()
        cleaned_text = ''.join([char for char in cleaned_text if char.isalpha() or char == ' '])
        return cleaned_text
    
    def _remove_stopwords(self, text, language):
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words[language]]
        return ' '.join(filtered_words)
    
    def _extract_ngrams(self, text):
        ngrams = []
        text = ' ' + text + ' '
        for i in range(len(text) - self.n + 1):
            ngrams.append(text[i:i+self.n])
        return ngrams
    
    def _load_stop_words(self, languages):
        for language in languages:
            try:
                with open(f'stopwords/{language}.txt', 'r', encoding='utf8') as f:
                    self.stop_words[language] = set(f.read().splitlines())
            except FileNotFoundError:
                continue
    
    def load_data(self, file_path):
        df = pd.read_csv(file_path, encoding='utf-8', dtype={'column1': 'string', 'column2': 'string'})
        text_data = df['sentence'].tolist()
        labels = df['lan_code'].tolist()
        return text_data, labels
    
    def train(self, text_data, labels, progress_bar=None):
        self._load_stop_words(set(labels))
        for doc, label in zip(text_data, labels):
            normalized_doc = self._normalize_text(doc)
            cleaned_doc = self._clean_text(normalized_doc)
            no_stopwords_doc = self._remove_stopwords(cleaned_doc, label)
            ngrams = self._extract_ngrams(no_stopwords_doc)
            self.class_counts[label] += 1
            for ngram in ngrams:
                self.class_word_counts[label][ngram] += 1
                self.vocab.add(ngram)
            if progress_bar:
                progress_bar.update(1)
        self._compute_tfidf(text_data, labels)
    
    def _compute_tfidf(self, text_data, labels):
        all_texts = [' '.join(self._extract_ngrams(self._clean_text(self._normalize_text(text)))) for text in text_data]
        self.tfidf_vectorizer.fit(all_texts)
        self.class_tfidf_scores = {}
        for label in set(labels):
            label_texts = [' '.join(self._extract_ngrams(self._clean_text(self._normalize_text(text)))) for text, l in zip(text_data, labels) if l == label]
            tfidf_matrix = self.tfidf_vectorizer.transform(label_texts)
            self.class_tfidf_scores[label] = np.sum(tfidf_matrix, axis=0)
    
    def _calculate_log_likelihood(self, text, label):
        log_likelihood = 0.0
        ngrams = self._extract_ngrams(text)
        for ngram in ngrams:
            word_count = self.class_word_counts[label].get(ngram, 0) + 1 
            total_words = sum(self.class_word_counts[label].values()) + len(self.vocab)
            log_likelihood += np.log(word_count / total_words)
        return log_likelihood
    
    def predict(self, text):
        normalized_text = self._normalize_text(text)
        cleaned_text = self._clean_text(normalized_text)
        no_stopwords_text = self._remove_stopwords(cleaned_text, "")
        ngrams_text = ' '.join(self._extract_ngrams(no_stopwords_text))
        tfidf_scores = self.tfidf_vectorizer.transform([ngrams_text])
        best_label = None
        max_log_prob = float('-inf')
        for label in self.class_counts.keys():
            log_prior = np.log(self.class_counts[label] / sum(self.class_counts.values()))
            log_likelihood = self._calculate_log_likelihood(cleaned_text, label)
            log_posterior = log_prior + log_likelihood + np.sum(tfidf_scores.multiply(self.class_tfidf_scores[label]))
            if log_posterior > max_log_prob:
                max_log_prob = log_posterior
                best_label = label
        return best_label
