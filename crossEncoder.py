import sys

from sentence_transformers.cross_encoder import CrossEncoder

# 1. Load a pretrained CrossEncoder model
model = CrossEncoder("cross-encoder/stsb-distilroberta-base")

# We want to compute the similarity between the query sentence...
query = "A man is eating pasta."

# ... and all sentences in the corpus
corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]
sys.exit()
# 2. We rank all sentences in the corpus for the query
ranks = model.rank(query, corpus)

# Print the scores
print("Query: ", query)
for rank in ranks:
    print(f"{rank['score']:.2f}\t{corpus[rank['corpus_id']]}")
"""
Query:  A man is eating pasta.
0.67    A man is eating food.
0.34    A man is eating a piece of bread.
0.08    A man is riding a horse.
0.07    A man is riding a white horse on an enclosed ground.
0.01    The girl is carrying a baby.
0.01    Two men pushed carts through the woods.
0.01    A monkey is playing drums.
0.01    A woman is playing violin.
0.01    A cheetah is running behind its prey.
"""