from semantic_search import SemanticSearch
from lexical_search import LexicalSearch
import pandas as pd

import pandas as pd

def reciprocal_rank_fusion(semantic_rank, lexical_rank, k):

  for rank, (key, value) in enumerate(semantic_rank.items()):
    score = 1 / (rank + 60)
    semantic_rank[key] = {"value": value, "score": score}

  for rank, (key, value) in enumerate(lexical_rank.items()):
    score = 1 / (rank + 60)
    lexical_rank[key] = {"value": value, "score": score}

  summed_scores_dict = {}

  for key in set(semantic_rank.keys()) | set(lexical_rank.keys()):
      score1 = semantic_rank.get(key, {'score': 0})['score']
      score2 = lexical_rank.get(key, {'score': 0})['score']

      summed_score = score1 + score2

      summed_scores_dict[key] = {'score': summed_score}

  reciprocal_rank_fusion = dict(sorted(summed_scores_dict.items(), key=lambda item: item[1]['score'], reverse=True))

  return reciprocal_rank_fusion

df = pd.read_csv('data/data_lama/data_halodoc_ordered.csv', sep = ';')
corpus = df['uses'].to_list()
query = "obat batuk berdahak"
lexical_model = LexicalSearch()
lexical_rank = lexical_model.rank(corpus, query)
semantic_model = SemanticSearch()
semantic_model.load_pretrained()
semantic_rank = semantic_model.rank(corpus, query)
fusion_rank = reciprocal_rank_fusion(semantic_rank, lexical_rank, 60)

corpus_id = list(fusion_rank.keys())
for id in corpus_id[:10]:
  print(corpus[id])
  print("=====================================================")

