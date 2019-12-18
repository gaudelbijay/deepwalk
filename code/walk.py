import random
import multiprocessing as mp
import itertools

class DeepWalk():
    def __init__(self,graph):
        self.G = graph
        # self.nodes = list(self.G.nodes())
    def random_walk(self,walk_length,start=None):
        if start:
            walk = [start]
        
        else:
            walk=[random.choice(list(self.G.nodes()))]
        
        while len(walk)<walk_length:
            cur = walk[-1]
            cur_nbrs = list(self.G.neighbors(cur))
            if len(cur_nbrs)>0:
                walk.append(random.choice(cur_nbrs))
            else:
                break

        return walk

    def random_walk_corpus(self,walk_length,num_walk):
        walks = []
        nodes = list(self.G.nodes())
        for _ in range(num_walk):
            random.shuffle(nodes)
            for v in nodes:
                walks.append(self.random_walk(walk_length=walk_length,start=v))   
        return walks

    def parallelize_random_walk_corpus(self,walk_length,num_walk):
        # result = []
        pool = mp.Pool(mp.cpu_count())
        result = [pool.apply(self.random_walk_corpus,args=(walk_length,num)) for num in self.divide_load_per_cup(num_walk)]
        walks = list(itertools.chain(*result))
        return walks

    def divide_load_per_cup(self,num_walks):
        self.workers = mp.cpu_count()

        if num_walks%self.workers==0:
            return [num_walks//self.workers]*self.workers
        else:
            return [num_walks//self.workers]*self.workers+[num_walks%self.workers]