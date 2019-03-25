import pandas
import numpy as np
cross = open('../config/cross.txt')
car = open('../config/car.txt')
road = open('../config/road.txt')

cross_lines = cross.readlines()
car_lines = car.readlines()
road_lines = road.readlines()

cross_list= []
car_list = []
road_list = []

for line in cross_lines:
    if '#' in line:
        continue
    newline = line.replace('(','').replace(')','').replace(',','')
    num = list(map(int,newline.split(" ")))
    cross_list.append(num)
cross_array = np.array(cross_list)
#print(cross_array)

for line in car_lines:
    if '#' in line:
        continue
    newline = line.replace('(','').replace(')','').replace(',','')
    num = list(map(int,newline.split(" ")))
    car_list.append(num)
car_array = np.array(car_list)
#print(car_array)

for line in road_lines:
    if '#' in line:
        continue
    newline = line.replace('(','').replace(')','').replace(',','')
    num = list(map(int,newline.split(" ")))
    road_list.append(num)
road_array = np.array(road_list)
#print(road_array)

max = car_array[0,2]
for i in range(1,car_array.shape[0]):
    if max < car_array[i,2]:
        max = car_array[i,2]
#print(max)
#print(car_array)
        
node = []
for i in range(1,max+1):
    node.append(i)
#print(node)  

node_list = []
for i in range(0,road_array.shape[0]):
    info = [road_array[i,4],road_array[i,5],road_array[i,1]]
    node_info = tuple(info)
    node_list.append(node_info)
    if road_array[i,6] == 1:
        info1 = [road_array[i,5],road_array[i,4],road_array[i,1]]
        node_info1 = tuple(info1)
        node_list.append(node_info1)
#print(node_list)


#最短
INF_val = 9999

class Dijkstra_Path():
    def __init__(self, node_map):
        self.node_map = node_map
        self.node_length = len(node_map)
        self.used_node_list = []
        self.collected_node_dict = {}

    def __call__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        self._init_dijkstra()
        return self._format_path()

    def _init_dijkstra(self):
        ## Add from_node to used_node_list
        self.used_node_list.append(self.from_node)
        for index1 in range(self.node_length):
            self.collected_node_dict[index1] = [INF_val, -1]

        self.collected_node_dict[self.from_node] = [0, -1]  # from_node don't have pre_node
        for index1, weight_val in enumerate(self.node_map[self.from_node]):
            if weight_val:
                self.collected_node_dict[index1] = [weight_val, self.from_node]  # [weight_val, pre_node]

        self._foreach_dijkstra()

    def _foreach_dijkstra(self):
        while (len(self.used_node_list) < self.node_length - 1):
            min_key = -1
            min_val = INF_val
            for key, val in self.collected_node_dict.items():  # 遍历已有权值节点
                if val[0] < min_val and key not in self.used_node_list:
                    min_key = key
                    min_val = val[0]

                    ## 把最小的值加入到used_node_list
            if min_key != -1:
                self.used_node_list.append(min_key)

            for index1, weight_val in enumerate(self.node_map[min_key]):
                ## 对刚加入到used_node_list中的节点的相邻点进行遍历比较
                if weight_val > 0 and self.collected_node_dict[index1][0] > weight_val + min_val:
                    self.collected_node_dict[index1][0] = weight_val + min_val  # update weight_val
                    self.collected_node_dict[index1][1] = min_key

    def _format_path(self):
        node_list = []
        temp_node = self.to_node
        node_list.append((temp_node, self.collected_node_dict[temp_node][0]))
        while self.collected_node_dict[temp_node][1] != -1:
            temp_node = self.collected_node_dict[temp_node][1]
            node_list.append((temp_node, self.collected_node_dict[temp_node][0]))
        node_list.reverse()
        return node_list


def set_node_map(node_map, node, node_list):
    for x, y, val in node_list:
        node_map[node.index(x)][node.index(y)] = node_map[node.index(y)][node.index(x)] = val


## init node_map to 0
node_map = [[0 for val in range(len(node))] for val in range(len(node))]

## set node_map
route = []
set_node_map(node_map, node, node_list)
for m in range(0,car_array.shape[0]):
    ## select one node to obj node, e.g. A --> D(node[0] --> node[3])
    from_node = node.index(car_array[m,1])
    to_node = node.index(car_array[m,2])
    dijkstrapath = Dijkstra_Path(node_map)
    path = dijkstrapath(from_node, to_node)
    answer = [car_array[m,i] for i in {0,1}]
    for i in range(0,len(path)):
        a = path[i][0]
        answer.append(a)
    answer.append(car_array[m,2])
    route.append(answer)

def get_road_from_two_cross(cross_id1,cross_id2):    
    for i in range(road_array.shape[0]):
        if (cross_id1 == road_array[i,4] and cross_id2 == road_array[i,5]):
            return road_array[i,0]
        elif road_array[i,6]:#duplex
            if (cross_id2 == road_array[i,4] and cross_id1 == road_array[i,5]):
                return road_array[i,0]

route_road = []
j = 0
for i in route:
    route_i_road = [i[0]]  #car id
    
    # plant time
    route_i_road.append(car_array[j,4])
    #add car route
    route_i_road.append([get_road_from_two_cross(i[j],i[j+1]) for j in range(1,len(i)-1)])
    route_road.append(route_i_road)
    j += 1

answer_path = '../config/answer.txt'

with open(answer_path, 'w') as f:
    f.write('#(carId,StartTime,RoadId...)\n')
    for i in range(len(route_road)):
        #f.write('(')
        f.write('('+str(route_road[i]).replace('[','').replace(']','').replace("'",""))
        f.write(')\n')
