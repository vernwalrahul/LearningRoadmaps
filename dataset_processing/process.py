import os
import argparse
import networkx as nx
import math        
import numpy as np
from itertools import islice     

k = 10

#return k shortest path
def k_shortest_paths(G, source, target, weight=None):
    global k
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def remove_invalid_edges(G1, binary_vec):
    to_remove = []
    
    for i, edge in enumerate(G1.edges()):
        if(not binary_vec[i]):
            u,v = edge
            to_remove.append((u, v))

    for r in to_remove:
        G1.remove_edge(r[0], r[1])        
    return G1        

def process_it(G, directory):
    G1 = G.copy()
    start = np.loadtxt(directory+"/start_node.txt")
    goal = np.loadtxt(directory+"/goal_node.txt")
    binary_vec = np.loadtxt(directory+"/binary_vec.txt")

    # G1 = remove_invalid_edges(G1, binary_vec)

    for i in range(50):
        src = str(int(start[i]))
        gl = str(int(goal[i]))
        paths = []
        try:
            paths = k_shortest_paths(G1, src, gl)
            print("no(paths) = ", len(paths))        
        except Exception as e:
            print(e)    

def list_all_dir(data_dir):
    task_dirs = os.listdir(data_dir)

    list_dir = []
    for task_dir in task_dirs:
        env_dirs = os.listdir(data_dir+"/"+task_dir)
        for env_dir in env_dirs:
            list_dir.append(data_dir +"/"+ task_dir +"/"+ env_dir)
    return list_dir        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate environments')
    parser.add_argument('--graphfile',type=str,required=True)
    parser.add_argument('--datadir',type=str,required=True)
    args = parser.parse_args()

    G = nx.read_graphml(args.graphfile)
    data_dir = args.datadir

    directories = list_all_dir(data_dir)
    print(directories)

    for directory in directories:
        process_it(G, directory)