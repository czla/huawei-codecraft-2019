# import time
import numpy as np
import logging
import sys

#logging.basicConfig(level=logging.DEBUG,
#                    filename='../logs/CodeCraft-2019.log',
#                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                    datefmt='%Y-%m-%d %H:%M:%S',
#                    filemode='a')


def main():

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    # car_path = '../config/map1/car.txt'
    # road_path = '../config/map1/road.txt'
    # cross_path = '../config/map1/cross.txt'
    # answer_path = '../config/map1/answer.txt'


    # cross = open(cross_path)
    car = open(car_path)
    road = open(road_path)

    # cross_lines = cross.readlines()
    car_lines = car.readlines()
    road_lines = road.readlines()

    # cross_list= []
    car_list = []
    road_list = []

    # for line in cross_lines:
    #     if '#' in line:
    #         continue
    #     newline = line.replace('(','').replace(')','').replace(',','')
    #     num = list(map(int,newline.split(" ")))
    #     cross_list.append(num)
    # cross_array = np.array(cross_list)
    # #print(cross_array)

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

    cross_real = []
    with open(cross_path, 'r') as cross:
        data = cross.readlines()

        for line in data:
            if '#' in line:
                continue
            cross_real.append(int(line.split(',')[0].replace('(', '')))


    matrix_slow = -1 * np.ones((len(cross_real), len(cross_real)), dtype=float)
    for i in range(len(cross_real)):
        matrix_slow[i][i] = 0
    matrix_normal = matrix_slow.copy()
    matrix_fast = matrix_slow.copy()

    for road in road_array:
        from_index, to_index = cross_real.index(road[4]), cross_real.index(road[5])
        matrix_normal[from_index, to_index] = road[1] / road[3]
        matrix_slow[from_index, to_index] = road[1] / road[3] + road[2]
        weight_fast = road[1] / road[3] - road[2]
        if weight_fast <= 0:
            weight_fast = 0.5
        matrix_fast[from_index, to_index] = weight_fast
        if road[-1] == 1:
            matrix_normal[to_index, from_index] = road[1] / road[3]
            matrix_slow[to_index, from_index] = road[1] / road[3] + road[2]
            matrix_fast[to_index, from_index] = weight_fast


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

# def update_graph(data_weight):


    route = []
    for m in range(car_array.shape[0]):
        is_again_flag = False
        for  repeat_index, pre_car in enumerate(car_array[:m, :3]):
            if car_array[m][1] == pre_car[1] and car_array[m][2] == pre_car[2]:
                if abs(car_array[m][3] - car_array[repeat_index][3]) < 4:
                    is_again_flag = True
                    break

        if is_again_flag:
            # route.append(car_array[m, 2])
            route.append(route[repeat_index])

        else:
            if car_array[m,3] <= 8:
                d1, d2 = dijkstra_search(matrix_slow, cross_real, cross_real.index(car_array[m,1])) # 出发点
            elif car_array[m,3] <= 12:
                d1, d2 = dijkstra_search(matrix_normal, cross_real, cross_real.index(car_array[m, 1]))  # 出发点
            else:
                d1, d2 = dijkstra_search(matrix_fast, cross_real, cross_real.index(car_array[m, 1]))  # 出发点
            #print(d1)
            #print(d2)

            target = car_array[m,2]     # target cross id
            # for i in d1:
            #     if i[0] == target:
            #         pass
            #         #print('路径最短距离为：', i[1])

            key = target
            d3 = [target]

            while key in d2.keys():
                d3.insert(0, d2[key])
                key = d2[key]
            #print(d3)
            route.append(d3)
            print('car %d'%(m+1))
        #print(route)
            #route = []
        #route.extend(d3)

    def get_road_from_two_cross(cross_id1,cross_id2):
        for i in range(road_array.shape[0]):
            if cross_id1 == road_array[i,4] and cross_id2 == road_array[i,5]:
                return road_array[i,0]
            elif road_array[i,6]:#duplex
                if cross_id2 == road_array[i,4] and cross_id1 == road_array[i,5]:
                    return road_array[i,0]

    # plt.hist(car_data['planTime'])

    # print('plan route done!')
    route_road = []
    j = 0
    for i in route:
        route_i_road = [int(car_array[j, 0])]  # car id
        if len(i) <= 15 and car_array[j, 3] > 10:
            delay_time = np.random.randint(0, 600)
        elif len(i) <= 16:
            delay_time = np.random.randint(500, 1500)
        elif len(i) <= 18:
            delay_time = np.random.randint(1400, 2400)
        elif len(i) <= 26:
            delay_time = np.random.randint(2300, 4100)
        elif car_array[j, 3] < 5:
            delay_time = np.random.randint(4800, 5200)
        else:
            delay_time = np.random.randint(4000, 4800)
        #
        # else:
        #     delay_chance = np.random.uniform(0, 1)
        #     if delay_chance < 0.2:
        #         delay_time = np.random.randint(1000, 1600)
        #     elif delay_chance < 0.4:
        #         delay_time = np.random.randint(1600, 2200)
        #     elif delay_chance < 0.6:
        #         delay_time = np.random.randint(2200, 2700)
        #     #elif delay_chance < 0.8:
        #      #   delay_time = np.random.randint(12000, 950)
        #     else:
        #         delay_time = np.random.randint(2700, 3500)

        route_i_road.append(int(car_array[j, 4]) * 5 + delay_time)
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
    #start = time.time()
    main()
    #end = time.time()
    #print('runtime: %f'%end - start)

