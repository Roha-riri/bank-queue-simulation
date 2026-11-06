import math
import random
import simpy

ARRIVAL_RATE = 0.8      # customers per minute
SERVICE_RATE = 1 / 3    # one teller serves 1 customer per 3 minutes
NUM_TELLERS = 5         # change to 3, 4 or 5
SIM_TIME = 100000       # minutes
WARM_UP = 1000          # minutes
SEED = 42

waiting_times = []
queue_lengths = []
busy_time = 0
served = 0


def customer(env, tellers):
    global busy_time, served
    arrival = env.now
    with tellers.request() as req:
        yield req
        wait = env.now - arrival
        service = random.expovariate(SERVICE_RATE)
        yield env.timeout(service)
    if arrival >= WARM_UP:
        waiting_times.append(wait)
        busy_time += service
        served += 1


def arrivals(env, tellers):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))
        env.process(customer(env, tellers))


def monitor(env, tellers):
    while True:
        if env.now >= WARM_UP:
            queue_lengths.append(len(tellers.queue))
        yield env.timeout(1)


random.seed(SEED)
env = simpy.Environment()
tellers = simpy.Resource(env, capacity=NUM_TELLERS)
env.process(arrivals(env, tellers))
env.process(monitor(env, tellers))
env.run(until=SIM_TIME)

# Simulation results
time = SIM_TIME - WARM_UP
sim_Wq = sum(waiting_times) / len(waiting_times)
sim_Lq = sum(queue_lengths) / len(queue_lengths)
sim_util = busy_time / (NUM_TELLERS * time)
sim_throughput = served / time * 60

# Theory (Erlang C)
c = NUM_TELLERS
a = ARRIVAL_RATE / SERVICE_RATE
rho = a / c

sum_part = 0
for k in range(c):
    sum_part += a ** k / math.factorial(k)
last_part = a ** c / math.factorial(c) / (1 - rho)
P_wait = last_part / (sum_part + last_part)

th_Wq = P_wait / (c * SERVICE_RATE - ARRIVAL_RATE)
th_Lq = ARRIVAL_RATE * th_Wq

print("Number of tellers:", c)
print("Waiting time Wq (min):  simulation", round(sim_Wq, 3), " theory", round(th_Wq, 3))
print("Queue length Lq:        simulation", round(sim_Lq, 3), " theory", round(th_Lq, 3))
print("Utilization:            simulation", round(sim_util, 3), " theory", round(rho, 3))
print("Throughput (cust/hour): simulation", round(sim_throughput, 1), " theory", ARRIVAL_RATE * 60)