import heapq
import networkx as nx

# F e uma floresta em G, R esta contido em E e F inteceção R e um conjunto vazio
def all_mst(graph, F, R):
    
    t, z = an_mst(graph, F, R)
    print("\n\n", z, t)

    return t if z <= 8 else None 
    
# retorna uma (F,R)-admissivel mst t*
def an_mst(graph, F, R):
    
    heap = []
    trees = [[i] for i in graph.nodes()]
    node_tree = [i - 1 for i in graph.nodes()]
    mst_num_edges = 0
    mst_weigth = 0
    mst = {}

    for edge in graph.edges():

        weigth = graph.get_edge_data(*edge)['weigth']

        if not contains_edge(R, (weigth, edge)):

            heapq.heappush(heap, (weigth, edge))

            if contains_edge(F, (weigth, edge)):
                
                index_a = node_tree[edge[0]-1]
                index_b = node_tree[edge[1]-1]
                
                if index_b < index_a:

                    index_a, index_b = index_b, index_a
                
                
                for i in trees[index_b]:
                    node_tree[i-1] = index_a
                
                trees[index_a].extend(trees[index_b])
                trees[index_b] = []
                
                mst_weigth += weigth
                mst_num_edges+=1
                mst[edge[0]] = {edge[1]: {'weigth': weigth}}
                mst[edge[1]] = {edge[0]: {'weigth': weigth}}
                 
    while mst_num_edges < graph.number_of_nodes() - 1 and len(heap) >  0:
        
        weigth, (nodeA, nodeB) = heapq.heappop(heap)
        print(">>", weigth, (nodeA, nodeB))

        if node_tree[nodeA-1] != node_tree[nodeB-1]:

            index_a = node_tree[nodeA-1]
            index_b = node_tree[nodeB-1]
            
            if index_b < index_a:

                index_a, index_b = index_b, index_a
            
            
            for i in trees[index_b]:
                node_tree[i-1] = index_a
            
            trees[index_a].extend(trees[index_b])
            trees[index_b] = []
            
            mst_weigth += weigth
            mst_num_edges+=1
            mst[nodeA] = {nodeB: {'weigth': weigth}}
            mst[nodeB] = {nodeA: {'weigth': weigth}}
            
    return mst, mst_weigth

def contains_edge(set, edge):

    for i in set:
        if i[1][0] == edge[1][0] and i[1][1] == edge[1][1]:
            return True
    
    return False


def main():
    
    graph = nx.Graph({
        1: { 2: {'weigth': 2},
             3: {'weigth': 1}
           },
        2: { 1: {'weigth': 2},
             3: {'weigth': 3},
             4: {'weigth': 1}
           },
        3: { 1: {'weigth': 1},
             2: {'weigth': 3},
             4: {'weigth': 2},
             5: {'weigth': 2}
           },
        4: { 2: {'weigth': 1},
             3: {'weigth': 2},
             5: {'weigth': 1},
             6: {'weigth': 3}
           },
        5: { 3: {'weigth': 2},
             4: {'weigth': 1},
             6: {'weigth': 3}
           },
        6: { 4: {'weigth': 3},
             5: {'weigth': 3}
           }
    })

    F = []
    R = []
    msts = []

    mst = all_mst(graph, F, R)
    
    if mst is not None:
                
        msts.append(mst)
        mst = nx.Graph(mst)

        for edge in mst.edges():
            
            weigth = graph.get_edge_data(*edge)['weigth']
            
            if not contains_edge(R, (weigth, edge)) and not contains_edge(F, (weigth, edge)):
                
                R.append((weigth, edge))
                print("\n (1)", F, R) 

                
                mst = all_mst(graph, F, R)
                
                if mst is not None:
                    
                    msts.append(mst)
                    print(msts)
                
                else:

                    R.remove((weigth, edge))
                    F.append((weigth, edge))

                    print("\n (1)", F, R)


                    mst = all_mst(graph, F, R)
                
                    if mst is not None:
                        
                        msts.append(mst)

    for mst in msts:
        print("\n\n\n", mst)
if __name__ == "__main__":
    main()