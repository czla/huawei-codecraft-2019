import logging
import sys
import os
import pandas as pd
import networkx as nx

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

    #---------------- to read input file---------------------#
    car_data = pd.read_csv(car_path, sep = ',')
    car_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
    car_data['id'] = car_data['id'].str.split('(').str[1]
    car_data['planTime'] = car_data['planTime'].str.split(')').str[0]
    print(car_data.head())
    
    cross_data = pd.read_csv(cross_path, sep = ',')
    cross_data.columns = ['id','roadIdU','roadIdR','roadIdD','roadIdL']
    cross_data['id'] = cross_data['id'].str.split('(').str[1]
    cross_data['roadIdL'] = cross_data['roadIdL'].str.split(')').str[0]
    print(cross_data.head())
    
    road_data = pd.read_csv(road_path, sep = ',')
    road_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
    road_data['id'] = road_data['id'].str.split('(').str[1]
    road_data['isDuplex'] = road_data['isDuplex'].str.split(')').str[0]
    print(road_data.head())
    
    #----------------generate_graph-------------------------#
    D = nx.DiGraph()

    D.add_nodes_from([int(x) for x in list(cross_data['id'])])
    
    road = []
    for i in range(road_data.shape[0]):
        #attribute = {}
        #attribute['length']=road_data.iloc[i,1]
        #attribute['speed']=road_data.iloc[i,2]
        #attribute['channel']=road_data.iloc[i,3]
        #road_index = ()
        road.append((road_data.iloc[i,4],road_data.iloc[i,5],road_data.iloc[i,1]))
        if road_data.iloc[i,6]:
                road.append((road_data.iloc[i,5],road_data.iloc[i,4],road_data.iloc[i,1]))
    
    D.add_weighted_edges_from(road)
    
    #nx.draw_networkx(D, node_size=30, pos=nx.spring_layout(D), arrows=True, with_labels=True)
    
    #----------------assign_route-----------------------------#
    route = []
    path = dict(nx.all_pairs_shortest_path(D))
    
    # get shortest route
    for i in range(car_data.shape[0]):
        route_i = [car_data.iloc[i,0]]
        #route_i.append(nx.shortest_path(D,car_data.iloc[i,1],car_data.iloc[i,2]))
        route_i.append(path[car_data.iloc[i,1]][car_data.iloc[i,2]])
        route.append(route_i)
    #    
    #print(route[:5])
    
    def get_road_from_two_cross(cross_id1,cross_id2):    
        for i in range(road_data.shape[0]):
            if (cross_id1 == road_data.iloc[i,4] and cross_id2 == road_data.iloc[i,5]):
                return road_data.iloc[i,0]
            elif road_data.iloc[i,6]:#duplex
                if (cross_id2 == road_data.iloc[i,4] and cross_id1 == road_data.iloc[i,5]):
                    return road_data.iloc[i,0]
    
    #plt.hist(car_data['planTime'])
    
    route_road = []
    j = 0
    for i in route:
        route_i_road = [int(i[0])]  #car id
        
        # plant time
        route_i_road.append(int(car_data.iloc[j,4]))
        #add car route
        route_i_road.append([get_road_from_two_cross(i[-1][j],i[-1][j+1]) for j in range(len(i[-1])-1)])
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