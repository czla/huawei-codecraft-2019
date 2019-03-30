# import numpy as np

#
# car_path = '../config/map1/car.txt'
# car = open(car_path)
#
# car_lines = car.readlines()
# car_list = []
#
# for line in car_lines:
#     if '#' in line:
#         continue
#     newline = line.replace('(', '').replace(')', '').replace(',', '')
#     num = list(map(int, newline.split(" ")))
#     car_list.append(num)
# car_array = np.array(car_list)
# print(car_array)
#
#
# road_path = '../config/map1/road.txt'
# road = open(road_path)
#
# road_lines = road.readlines()
# road_list = []
#
# for line in road_lines:
#     if '#' in line:
#         continue
#     newline = line.replace('(', '').replace(')', '').replace(',', '')
#     num = list(map(int, newline.split(" ")))
#     road_list.append(num)
# road_array = np.array(road_list)
# print(road_array)
#
#
# cross_path = '../config/map1/cross.txt'
# cross = open(cross_path)
#
# cross_lines = cross.readlines()
# cross_list = []
#
# for line in cross_lines:
#     if '#' in line:
#         continue
#     newline = line.replace('(', '').replace(')', '').replace(',', '')
#     num = list(map(int, newline.split(" ")))
#     cross_list.append(num)
# cross_array = np.array(cross_list)
# print(road_array)
#
# cross_real = []
# with open(cross_path, 'r') as cross:
#     data = cross.readlines()
#
#     for line in data:
#         if '#' in line:
#             continue
#         cross_real.append(int(line.split(',')[0].replace('(', '')))
#
#
# # print(cross_real)
#
# #start_time = car_array.copy()
# for i in range(car_array.shape[0]):
#     delay_chance = np.random.uniform(0, 1)
#     if delay_chance < 0.2:
#         delay_time = np.random.randint(1, 60)
#     elif delay_chance < 0.4:
#         delay_time = np.random.randint(50, 120)
#     elif delay_chance < 0.6:
#         delay_time = np.random.randint(110, 230)
#     else:
#         delay_time = np.random.randint(230, 350)
#     car_array[i, -1] += delay_time
#
# print(car_array[:5])
# car_array = car_array[car_array[:, -1].argsort()] #按照第3列对行排序
#
# print(car_array[:5])
#
# Matrix_slow = -1 * np.ones((len(cross_real), len(cross_real)), dtype=int)
# for i in range(len(cross_real)):
#     Matrix_slow[i][i] = 0
# Matrix_normal = Matrix_slow.copy()
# Matrix_fast = Matrix_slow.copy()
#
# for road in road_array:
#     from_index, to_index = cross_real.index(road[4]), cross_real.index(road[5])
#     Matrix_normal[from_index, to_index] = road[1] / road[3]
#     Matrix_slow[from_index, to_index] = road[1] / road[3] + road[2]
#     Matrix_fast[from_index, to_index] = max(road[1] / road[3] - road[2], 0.5)
#     if road[-1] == 1:
#         Matrix_normal[to_index, from_index] = road[1] / road[3]
#         Matrix_slow[to_index, from_index] = road[1] / road[3] + road[2]
#         Matrix_fast[to_index, from_index] = max(road[1] / road[3] - road[2], 0.5)
#
# print(Matrix_fast)
# # print(Matrix_slow)
# # print(Matrix_normal)
#
import matplotlib.pyplot as plt
answer = []
with open('../config/map1/answer.txt') as f:
    data = f.readlines()

    for line in data:
        if '#' in line:
            continue
        answer.append(line.split(','))

length = [len(i) for i in answer]
print(min(length))
print(max(length))


len_dict = {}
for i in length:
    if i not in len_dict:
        len_dict[i] = 1
    else:
        len_dict[i] += 1


swd = sorted(len_dict.items())
print(swd)