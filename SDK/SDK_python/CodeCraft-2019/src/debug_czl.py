import numpy as np

original_time = np.linspace(1, 10, dtype=int)

print(original_time)

start_time = original_time.copy()
for i in range(len(original_time)):
    delay_chance = np.random.uniform(0, 1)
    if delay_chance < 0.2:
        delay_time = np.random.randint(1, 60)
    elif delay_chance < 0.4:
        delay_time = np.random.randint(50, 120)
    elif delay_chance < 0.6:
        delay_time = np.random.randint(110, 230)
    else:
        delay_time = np.random.randint(230, 350)
    start_time[i] += delay_time

print(start_time)
