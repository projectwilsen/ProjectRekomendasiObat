import re
import os
import pandas as pd
import pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from rank_bm25 import BM25L

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class LexicalSearch:

    # def __init__(self, corpus_tokenized_path='data/data_with_prepro/corpus_sparse_tokenized_all_data_ordered.pkl'):
    def __init__(self, corpus_tokenized_path='data/data_lama/corpus_sparse_tokenized_all_data_ordered.pkl'):
        self.corpus_tokenized_path = corpus_tokenized_path
        self.stop_words = set(stopwords.words('indonesian'))
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

    def rm_link(self, text):
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def rm_punct2(self, text):
        return re.sub(r'[\"\#\$\%\&\'\(\)\*\+\/\:\;\<\=\>\@\[\\\]\^\_\`\{\|\}\~]', ' ', text)

    def rm_html(self, text):
        return re.sub(r'<[^>]+>', '', text)

    def space_bt_punct(self, text):
        pattern = r'([.,!?-])'
        s = re.sub(pattern, r' \1 ', text)     # add whitespaces between punctuation
        s = re.sub(r'\s{2,}', ' ', s)        # remove double whitespaces
        return s

    def rm_number(self, text):
        return re.sub(r'\d+', '', text)

    def rm_whitespaces(self, text):
        return re.sub(r' +', ' ', text)

    def rm_nonascii(self, text):
        return re.sub(r'[^\x00-\x7f]', r'', text)

    def rm_emoji(self, text):
        emojis = re.compile(
            '['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            u'\U00002702-\U000027B0'
            u'\U000024C2-\U0001F251'
            ']+',
            flags=re.UNICODE
        )
        return emojis.sub(r'', text)

    def spell_correction(self, text):
        return re.sub(r'(.)\1+', r'\1\1', text)

    def clean_text(self, text):
        no_link = self.rm_link(text)
        no_html = self.rm_html(no_link)
        space_punct = self.space_bt_punct(no_html)
        no_punct = self.rm_punct2(space_punct)
        no_number = self.rm_number(no_punct)
        no_whitespaces = self.rm_whitespaces(no_number)
        no_nonasci = self.rm_nonascii(no_whitespaces)
        no_emoji = self.rm_emoji(no_nonasci)
        spell_corrected = self.spell_correction(no_emoji)
        return spell_corrected

    def preprocess_text(self, text):
        tokens_sent = TextBlob(text).sentences
        text_clean = []
        for i in tokens_sent:
            tokens = i.split()
            filtered_tokens = [token for token in tokens if token not in self.stop_words]
            stemmed_tokens = [self.stemmer.stem(token) for token in filtered_tokens]
            cleaned_tokens = [re.sub(r'[^a-zA-Z0-9]', '', token) for token in stemmed_tokens]
            preprocessed_text = ' '.join(cleaned_tokens)
            text_clean.append(preprocessed_text)

        return text_clean

    def __process(self, corpus):

        data = []

        i = 0
        for text in corpus:
            print(i, text[:20])
            data_clean = self.clean_text(text.lower())
            data_clean = self.preprocess_text(data_clean)
            data_clean = ''.join(data_clean)
            data.append(data_clean)
            i += 1

        if len(data) > 1:
          tokenized_corpus = [doc.split(" ") for doc in data]
          tokenized = BM25L(tokenized_corpus)
          with open('corpus_sparse_tokenized_all_data_ordered.pkl', 'wb') as file:
              pickle.dump(tokenized, file)
        else:
          tokenized = data[0].split(" ")

        return tokenized

    def rank(self, corpus, query):

        if os.path.exists(self.corpus_tokenized_path):
            with open(self.corpus_tokenized_path, 'rb') as file:
                tokenized_corpus = pickle.load(file)
        else:
            tokenized_corpus = self.__process(corpus)
        tokenized_query = self.__process([query])

        doc_scores = tokenized_corpus.get_scores(tokenized_query)

        result_dict = {i: doc_scores[i] for i in range(len(doc_scores))}

        sparse_rank = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

        return sparse_rank

    def get_result(self, corpus, query, n:int=10):
        sparse_rank = self.rank(corpus, query)
        corpus_id = list(sparse_rank.keys())
        result = []
        for id in corpus_id[:n]:
            result.append(corpus[id])
        return result
    
# TODO: data_with_prepro nda jalan, kemungkinan ini untuk research yang qe
df = pd.read_csv('data/data_lama/data_halodoc_ordered.csv', sep = ';')

corpus = df['uses'].to_list()
query = 'obat batuk berdahak'
model = LexicalSearch()
# sparse_rank = model.rank(corpus, query)
result = model.get_result(corpus, query)
for i in result:
  print("=====================================")
  print(i)