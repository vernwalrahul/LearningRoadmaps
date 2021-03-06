import networkx as nx 
import numpy as np
import argparse 
from math import sqrt

def state_to_numpy(state):
    strlist = state.split()
    val_list = [float(s) for s in strlist]
    return np.array(val_list)

def calc_weight(s, g):
    return sqrt(np.sum((s-g)**2))

def generate_graph(nodes): #nodes -> key, value pair, value => string with joint angles separated by ' '
    G = nx.Graph()
    for key in nodes:
        value = str(nodes[str(key)]) 
        G.add_node(str(key), state = value) 
    return G

def load_output_samples(file_addr):
    nodes = {}
    i = 0
    with open(file_addr, 'r') as file:
        lines  = file.readlines()
        for line in lines:
            line = line.strip('\n')
            nodes[str(i)] = line
            i += 1
    print(nodes)
    return nodes

def connect_knn(G, K):
    for node in G.nodes():
        state = G.node[node]['state']
        conf = state_to_numpy(state)
        G1 = G.copy()

        for k in range(K):
            w = 1000000
            sn = None
            for node1 in G1.nodes():
            	if(node == node1):
            		continue
                state1 = G1.node[node1]['state']
                conf1  = state_to_numpy(state1)
                if(calc_weight(conf, conf1) < w):
                    w = calc_weight(conf, conf1)
                    sn = node1

            # if(check_for_collision(node, sn)==1):
            G.add_edge(node, sn)
            G[node][sn]['weight'] = w
            G1.remove_node(node1)
    return G

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate Sample')
    parser.add_argument('--samplefile',type=str,required=True)
    args = parser.parse_args()

    nodes = load_output_samples(args.samplefile)
    G = generate_graph(nodes)
    G = connect_knn(G, 5)
    nx.write_graphml(G, "output_graph.graphml")