import logging
import sys
import pandas as pd
import numpy as np
#from collections import defaultdict

logging.basicConfig(level=logging.DEBUG,
                    filename='../../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))
    
#    road_path = '../config/road.txt'
#    car_path = '../config/car.txt'
#    #cross_path = '../config/cross.txt'
#    answer_path = '../config/answer.txt'
    
    #---------------- to read input file---------------------#
    car_data = pd.read_csv(car_path, sep = ',')
    car_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
    car_data['id'] = car_data['id'].str.split('(').str[1]
    car_data['planTime'] = car_data['planTime'].str.split(')').str[0]
    #print(car_data.head())
        
    road_data = pd.read_csv(road_path, sep = ',')
    road_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
    road_data['id'] = road_data['id'].str.split('(').str[1]
    road_data['isDuplex'] = road_data['isDuplex'].str.split(')').str[0]
    #print(road_data.head())

    class Graph():
        def __init__(self):
            """
            self.edges is a dict of all possible next nodes
            e.g. {'X': ['A', 'B', 'C', 'E'], ...}
            self.weights has all the weights between two nodes,
            with the two nodes as a tuple as the key
            e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
            """
            self.edges = {}
            self.weights = {}
        
        def add_edge(self, from_node, to_node, weight):
            # Note: assumes edges are bi-directional
            if from_node in self.edges:
                self.edges[from_node].append(to_node)
            else:
                self.edges[from_node] = [to_node]

            #self.edges[to_node].append(from_node)
            self.weights[(from_node, to_node)] = weight
            #self.weights[(to_node, from_node)] = weight
    
    graph = Graph()
    
    road = []
    for i in range(road_data.shape[0]):
        road.append((str(road_data.iloc[i,4]),str(road_data.iloc[i,5]),road_data.iloc[i,1]))
        if road_data.iloc[i,6]:
                road.append((str(road_data.iloc[i,5]),str(road_data.iloc[i,4]),road_data.iloc[i,1]))

    for edge in road:
        graph.add_edge(*edge)
    
#    edgess = graph.edges
#    weights = graph.weights
    
    
    def dijsktra(graph, initial, end):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]
    
            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path
    
    #print(dijsktra(graph, '1', '34'))
    
    def get_road_from_two_cross(cross_id1,cross_id2):    
        for i in range(road_data.shape[0]):
            if (cross_id1 == road_data.iloc[i,4] and cross_id2 == road_data.iloc[i,5]):
                return road_data.iloc[i,0]
            elif road_data.iloc[i,6]:#duplex
                if (cross_id2 == road_data.iloc[i,4] and cross_id1 == road_data.iloc[i,5]):
                    return road_data.iloc[i,0]
    
    route = []
    # get shortest route
    for i in range(car_data.shape[0]):
        route_i = [car_data.iloc[i,0]]
        #route_i.append(nx.shortest_path(D,car_data.iloc[i,1],car_data.iloc[i,2]))
        route_i.append(dijsktra(graph,str(car_data.iloc[i,1]),str(car_data.iloc[i,2])))
        route.append(route_i)
    
    route_road = []
    j = 0
    for i in route:
        route_i_road = [int(i[0])]  #car id
        
        # plant time
        delay_chance = np.random.uniform(0, 1)
        if delay_chance > 0.5:
            route_i_road.append(int(car_data.iloc[j,4]) + 1)
        else:
            route_i_road.append(int(car_data.iloc[j,4]))
        #add car route
        route_i_road.append([get_road_from_two_cross(int(i[-1][j]),int(i[-1][j+1])) for j in range(len(i[-1])-1)])
        route_road.append(route_i_road)
        j += 1
    
    with open(answer_path, 'w') as f:
        f.write('#(carId,StartTime,RoadId...)\n')
        for i in range(len(route_road)):
            #f.write('(')
            f.write('('+str(route_road[i]).replace('[','').replace(']','').replace("'",""))
            f.write(')\n')

    # process
    
    # to write output file


if __name__ == "__main__":
    main()
