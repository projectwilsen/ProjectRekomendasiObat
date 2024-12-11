import re
import string
import os
import numpy as np
import pandas as pd
import torch
from torch import clamp
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import glob
from natsort import natsorted
import time

class SemanticSearch:

    def __init__(self, corpus_embeddings_path='data/data_lama/corpus_dense_embeddings_all_data_ordered.npy'):
        self.corpus_embeddings_path = corpus_embeddings_path
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def load_pretrained(self, from_pretrained:str="sentence-transformers/all-mpnet-base-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(from_pretrained)
        self.model = AutoModel.from_pretrained(from_pretrained)
        self.model.to(self.device)

    def encode(self, corpus, max_length):
        tokens = {'input_ids': [], 'attention_mask': []}

        for sentence in corpus:
            new_tokens = self.tokenizer.encode_plus(sentence, max_length=max_length, truncation=True,
                                                   padding='max_length', return_tensors='pt')
            tokens['input_ids'].append(new_tokens['input_ids'][0])
            tokens['attention_mask'].append(new_tokens['attention_mask'][0])

        # Move tensors to GPU
        tokens['input_ids'] = torch.stack(tokens['input_ids']).to(self.device)
        tokens['attention_mask'] = torch.stack(tokens['attention_mask']).to(self.device)

        # Run the model on GPU
        with torch.no_grad():
            outputs = self.model(**tokens)

        embeddings = outputs.last_hidden_state

        attention_mask = tokens['attention_mask']

        mask = attention_mask.unsqueeze(-1).expand(embeddings.shape).float()

        masked_embeddings = embeddings * mask

        summed = torch.sum(masked_embeddings, 1)
        summed_mask = torch.clamp(mask.sum(1), min=1e-9)
        mean_pooled = summed / summed_mask

        # Convert from PyTorch tensor to numpy array
        mean_pooled = mean_pooled.detach().cpu().numpy()

        return mean_pooled

    def process(self, *corpora):
        print('Encoding process using', self.device)
        for max_length, corpus in zip([25, 50, 75, 100, 128], corpora):
            print(f"Starting to embed corpus with {max_length} max length word")

            if len(corpus) > 1:
                max_size = 100
                smaller_batch = [corpus[i:i + max_size] for i in range(0, len(corpus), max_size)]
                print(len(corpus), 'in corpus with', max_length, ' max length word separated into', len(smaller_batch),
                      'smaller batch')

                i = 1
                for batch in smaller_batch:
                    mean_pooled = self.encode(batch, max_length)
                    np.save(f'temp/temp_{i}_{max_length}.npy', mean_pooled)
                    print(f"Finish embed corpus with {max_length} max length word, batch {i}")
                    i += 1
                    time.sleep(30)

                corpus = []
                for e in natsorted(glob.glob("temp/*.npy")):
                    print(e)
                    corpus.append(np.load(e))
                    mean_pooled = np.vstack(corpus)
                    print('Success corpus append')
                    os.remove(e)
                np.save(f'small_batch/corpus_dense_embeddings_{max_length}.npy', mean_pooled)
                print(f"Finish embed corpus with {max_length} length of word")

                time.sleep(60)

            else:
                max_length = len(corpus[0].split(" "))
                mean_pooled = self.encode(corpus, max_length)
                print("Finish embed query")


        if len(corpora) > 1:
            corpus = []
            for e in natsorted(glob.glob("small_batch/*.npy")):
                print(e)
                corpus.append(np.load(e))
                mean_pooled = np.vstack(corpus)
                print('Success corpus append')
            np.save('corpus_dense_embeddings_all_data_ordered.npy', mean_pooled)

        return mean_pooled

    def rank(self, corpus, query):

        if os.path.exists(self.corpus_embeddings_path):
            corpus_embeddings = np.load(self.corpus_embeddings_path)
        else:
            corpus_embeddings = self.process(corpus)
        query_embeddings = self.process([query])

        rank = cosine_similarity(query_embeddings,corpus_embeddings)
        rank_dict = {i: rank[0, i] for i in range(len(rank[0]))}

        dense_rank = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))

        return dense_rank

    def get_result(self, corpus, query, n:int=10):
        dense_rank = self.rank(corpus, query)
        corpus_id = list(dense_rank.keys())
        result = []
        for id in corpus_id[:n]:
            result.append(corpus[id])
        return result
    

df = pd.read_csv('data/data_lama/data_halodoc_ordered.csv', sep = ';')
corpus = df['uses'].to_list()
query = 'obat batuk berdahak'
model = SemanticSearch()
model.load_pretrained()
# dense_rank = model.rank(corpus, query)
result = model.get_result(corpus, query)
for i in result:
  print("=====================================")
  print(i)