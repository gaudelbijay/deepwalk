import networkx as nx
from walk import DeepWalk
from skipgram import SkipGram
from gensim.models import Word2Vec

def main():
    graph = nx.read_edgelist('./data/Wiki_edgelist.txt',create_using=nx.DiGraph(),nodetype=None,data=[('weight',int)])

    walk_ob = DeepWalk(graph)
    random_walk = walk_ob.parallelize_random_walk_corpus(walk_length=10,num_walk=100)
    # model = SkipGram(sentences=random_walk)
    # result=model.word2vec()
    result = Word2Vec(random_walk,size=5,window=10,workers=4,sg=1,hs=1)
    _embeddings = {}
    if result is None:
        print('model is not trained')
    else:
        for word in graph.nodes():
            _embeddings[word]=result.wv[word]

    print(_embeddings)


if __name__ == '__main__':
    main()