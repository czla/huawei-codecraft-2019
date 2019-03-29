import numpy as np

car_array = np.ones((5, 5))

print(car_array)

#start_time = car_array.copy()
for i in range(car_array.shape[0]):
    delay_chance = np.random.uniform(0, 1)
    if delay_chance < 0.2:
        delay_time = np.random.randint(1, 60)
    elif delay_chance < 0.4:
        delay_time = np.random.randint(50, 120)
    elif delay_chance < 0.6:
        delay_time = np.random.randint(110, 230)
    else:
        delay_time = np.random.randint(230, 350)
    car_array[i, -1] += delay_time

print(car_array)
car_array = car_array[car_array[:, -1].argsort()] #按照第3列对行排序

print(car_array)

Matrix_slow = -1 * np.ones((car_array.shape[0], car_array.shape[0]), dtype=int)
Matrix_normal = Matrix_slow.copy()
Matrix_fast = Matrix_slow.copy()

print(Matrix_fast)
print(Matrix_slow)
print(Matrix_normal)

