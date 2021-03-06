import logging
import sys

#logging.basicConfig(level=logging.DEBUG,
#                    filename='../logs/CodeCraft-2019.log',
#                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                    datefmt='%Y-%m-%d %H:%M:%S',
#                    filemode='a')


def main():
#    if len(sys.argv) != 5:
#        logging.info('please input args: car_path, road_path, cross_path, answerPath')
#        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    #import pandas
    import numpy as np
    cross = open(cross_path)
    car = open(car_path)
    road = open(road_path)

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
            
    data_index = []
    for i in range(1,max+1):
        data_index.append(i)
    #print(1 in data_index)
    #print(data_index)    

        
    Matrix = np.zeros([max+1,max+1])
    for i in range(0,max+1):
        Matrix[0,i] = i
    for i in range(0,max+1):
        Matrix[i,0] = i
    #print(Matrix)

    #Matrix[行，列] = [终点，起点]
    w_c = 0.2
    for i in range(1,max+1):
        for j in range(1,max+1):
            for m in range(0,road_array.shape[0]):
                if Matrix[i,0] == road_array[m,4] and Matrix[0,j] == road_array[m,5]:
                    Matrix[i,j] = float(road_array[m,1]/road_array[m,2] - w_c * road_array[m,3])
                    if road_array[m,6] == 1:
                        Matrix[j,i] = float(road_array[m,1]/road_array[m,2]- w_c * road_array[m,3])#是否写负
    #print(Matrix)

    data_weight = np.zeros([max,max])
    for i in range(0,max):
        for j in range(0,max):
            data_weight[i,j] = Matrix[i+1,j+1]
            if i != j and int(data_weight[i,j]) == 0:
                data_weight[i,j] = -1
    data_weight[max-1,max-1] = -1
    #print(data_weight)

    #最短路径
    def priority_queue(data, d0):  # 自建优先队列格式
        state = 1
        for i in range(len(data)):
            if d0[1] < data[i][1]:
                data.insert(i, d0)
                state = 0
                break
        if state:
            data.append(d0)
        return data


    def dijkstra_search(data, data_index, index):
        parent = {}  # 字典映射，更新前级节点
        queue = []  # 优先队列
        queue_out = [[data_index[index], data[index][index], 0]] # 输出队列

        while len(queue_out) < len(data_index):
            root_node = data_index.index(queue_out[-1][0])  # 当前最优节点
            # print(root_node)
            for i in range(len(data_index)):  # 遍历所有的可能性
                if data[root_node][i] != -1:  # 检查是否可直连，是
                    if data_index[i] not in [x[0] for x in queue_out]:
                        queue = priority_queue(queue,
                                               [data_index[i], data[root_node][i] + queue_out[-1][1], queue_out[-1][0]])
            # print(queue)    # 检查优先队列的情况 [['C', 1], ['B', 5]]

            for i in range(len(queue)):  # 0,1
                # print(queue[i][0])
                if queue[i][0] not in [x[0] for x in queue_out]:
                    parent[queue[i][0]] = queue[i][-1]
                    queue_out.append(queue[i])
                    del queue[i]
                    break

            # print(queue)
            # print('queue_out',queue_out)
        return queue_out, parent        
    
    route = []
    for m in range(0,car_array.shape[0]):
        d1, d2 = dijkstra_search(data_weight, data_index, int(car_array[m,1]-1)) # 出发点
        #print(d1)
        #print(d2)

        target = car_array[m,2]
        for i in d1:
            if i[0] == target:
                pass
                #print('路径最短距离为：', i[1])

        key = target
        d3 = [target]
        
        while key in d2.keys():
            d3.insert(0, d2[key])
            key = d2[key]
        #print(d3)
        route.append(d3)
    #print(route)
        #route = []
        #route.extend(d3)

    def get_road_from_two_cross(cross_id1,cross_id2):    
        for i in range(road_array.shape[0]):
            if not road_array[i, 6]:
                if (cross_id1 == road_array[i,4] and cross_id2 == road_array[i,5]):
                    return int(str(road_array[i,0])+'0')
            else:#duplex
                if (cross_id1 == road_array[i,4] and cross_id2 == road_array[i,5]):
                    return int(str(road_array[i,0])+'0')
                elif (cross_id2 == road_array[i,4] and cross_id1 == road_array[i,5]):
                    return int(str(road_array[i,0])+'1')
    
    #plt.hist(car_data['planTime'])
    
    route_road = []
    j = 0
    for i in route:
        route_i_road = [int(car_array[j,0])]  #car id
        delay_chance = np.random.uniform(0, 1)
        if delay_chance < 0.2:
            route_i_road.append(int(car_array[j,4]) + np.random.randint(1,100))
        elif delay_chance < 0.4:
            route_i_road.append(int(car_array[j,4]) + np.random.randint(100,200))
        elif delay_chance < 0.6:
            route_i_road.append(int(car_array[j,4]) + np.random.randint(300,400))

#        elif delay_chance < 0.8:
#            route_i_road.append(int(car_array[j,4]) + np.random.randint(400,500))
        else:
            route_i_road.append(int(car_array[j,4]) + np.random.randint(400,550))

        # plant time
        #route_i_road.append(int(car_array[j,4]))
        #add car route
        route_i_road.append([get_road_from_two_cross(i[j],i[j+1]) for j in range(len(i)-1)])
        route_road.append(route_i_road)
        j += 1

    #answer_path = 'answer.txt'
    #print(route_road)
    with open(answer_path, 'w') as f:
        f.write('#(carId,StartTime,RoadId...)\n')
        for i in range(len(route_road)):
            #f.write('(')
            f.write('('+str(route_road[i]).replace('[','').replace(']','').replace("'",""))
            f.write(')\n')

    #print('Done')  

#    logging.info("car_path is %s" % (car_path))
#    logging.info("road_path is %s" % (road_path))
#    logging.info("cross_path is %s" % (cross_path))
#    logging.info("answer_path is %s" % (answer_path))

# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
