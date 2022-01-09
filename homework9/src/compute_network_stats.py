import networkx as nx
import os
import os.path as osp
import argparse
import json



def json_to_dict(in_file):

    with open(in_file,'r') as f:
        data=json.load(f)
    return data

'''build graph of network'''
def build_graph(net):
    G = nx.Graph()

    for pony1 in net:
        for pony2 in net[pony1]:
            G.add_edge(pony1,pony2,weight= net[pony1][pony2])

    return G

'''The top three most connected characters by # of edges'''
def top_degree3(G):
    
    node_degrees = [(v,G.degree(v)) for v in G.nodes()]
    node_degrees.sort(key=lambda x: x[1], reverse=True)
    top3 = [char for (char,deg) in node_degrees[:3]]
    return top3


'''The top three most connected characters by sum of the weight of edges'''
def top_weight3(G,characters):
    
    weights={}
    for char in characters:
        weights[char]=0
        for edge in G.edges(char):
            weights[char] += G[edge[0]][edge[1]]["weight"]
    
    weight_list = list(weights.items())
    weight_list.sort(key= lambda x:x[1], reverse=True)
    top3 = [char for (char,w) in weight_list[:3]]
    return top3
    

    


'''The top three most central characters by betweenness'''
def top_between3(G):
    between_d=nx.algorithms.centrality.betweenness_centrality(G)
    betweeness_list = list(between_d.items())
    betweeness_list.sort(key= lambda x:x[1], reverse=True)
    top3 = [char for (char,w) in betweeness_list[:3]]
    return top3


def to_json(out_file,in_dict):
    dir_name,file_name = osp.split(out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass

    with open(out_file,'w') as f:
            json.dump(in_dict,f,indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--in_json')
    parser.add_argument('-o','--out_json')

    args = parser.parse_args()
    
    net = json_to_dict(args.in_json)
    chars=net.keys()
    graph=build_graph(net)
    
    top_deg3 = top_degree3(graph)
    top_w3 = top_weight3(graph,chars)
    top_b3 = top_between3(graph)
    
    d_to_output={"most_connected_by_num": top_deg3,"most_connected_by_weight": top_w3,"most_central_by_betweenness": top_b3}

    to_json(args.out_json,d_to_output)

if __name__=="__main__":
    main()
