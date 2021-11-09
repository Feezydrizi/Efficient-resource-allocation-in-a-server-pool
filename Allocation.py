# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:40:35 2020

@author: STRIX
"""

import numpy as np
from matplotlib import pyplot as plt


def generate_population(N_population, memory_usage, energy_consumption, initial_capacity):

    n_users = len(memory_usage)
    n_servers = len(energy_consumption)
    population = []
    maximum_energy_consumption = np.max(energy_consumption)
    maximum_usage = np.max(memory_usage)
    
    for tried_allocation in range(N_population):
        
        user_allocation = np.array([-1 for user in range(n_users)])        
        remaining_capacity = np.array(initial_capacity)
        
        if(tried_allocation == 0):
            sorted_servers = np.argsort(energy_consumption)
            sorted_users = list(np.argsort(memory_usage))            
            sorted_users = np.array(sorted_users)
        elif(tried_allocation == 1):
            sorted_servers = np.argsort(energy_consumption)
            sorted_users = list(np.argsort(memory_usage))  
            sorted_users.reverse()
            sorted_users = np.array(sorted_users)
        elif(tried_allocation == 2):
            sorted_servers = list(np.argsort(initial_capacity))
            sorted_users = list(np.argsort(memory_usage))            
            sorted_users = np.array(sorted_users)
            sorted_servers = np.array(sorted_servers)
        elif(tried_allocation == 3):
            sorted_servers = list(np.argsort(initial_capacity))
            sorted_users = list(np.argsort(memory_usage))     
            sorted_users.reverse()
            sorted_users = np.array(sorted_users)
            sorted_servers = np.array(sorted_servers)
        elif(tried_allocation == 4):
            sorted_servers = list(np.argsort(initial_capacity))
            sorted_users = list(np.argsort(memory_usage))     
            sorted_servers.reverse()
            sorted_users = np.array(sorted_users)
            sorted_servers = np.array(sorted_servers)    
        elif(tried_allocation == 5):
            sorted_servers = list(np.argsort(initial_capacity))
            sorted_users = list(np.argsort(memory_usage))     
            sorted_servers.reverse()
            sorted_users.reverse()
            sorted_users = np.array(sorted_users)
            sorted_servers = np.array(sorted_servers)  
        else:
            sorted_servers = [i for i in range(n_servers)]
            sorted_users = [i for i in range(n_users)]
            np.random.shuffle(sorted_servers)
            np.random.shuffle(sorted_users)
        objective_value = 0
        for user in sorted_users:
            for server in sorted_servers:
                if(memory_usage[user] <= remaining_capacity[server]):            
                        user_allocation[user] = server                        
                        remaining_capacity[server] -= memory_usage[user]
                        objective_value += (maximum_usage-memory_usage[user]+1) * (maximum_energy_consumption-energy_consumption[server]+1)            
                        break  
        population.append((objective_value, user_allocation))
    return population
min_energy_per_mb = 1.63 / 8192 # 1.63W for a 8GB DDR4 RAM
max_energy_per_mb = 6 / 4096 #6W per 4GB DDR1
min_memory_usage = 128 #in MB
max_memory_usage = 4192
min_memory_capacity = 32*1024 #In MB
max_memory_capacity = 256*1024 
step = 8*1024 #RAM can only add up by 8GB
possible_memories = [memory for memory in range(min_memory_capacity, max_memory_capacity+1024, step)]
n_servers = 100
n_users = 10000

user_allocation = np.array([-1 for user in range(n_users)])
server_load = [[] for server in range(n_servers)]

np.random.seed(1)
memory_usage = np.random.randint(min_memory_usage, max_memory_usage, n_users)
energy_consumption = (max_energy_per_mb - min_energy_per_mb) * np.random.rand(n_servers) + min_energy_per_mb
initial_capacity = np.random.choice(possible_memories, n_servers)


remaining_capacity = np.array(initial_capacity)
sorted_servers = np.argsort(energy_consumption)
sorted_users = list(np.argsort(memory_usage))
#sorted_users.reverse()
sorted_users = np.array(sorted_users)
maximum_energy_consumption = np.max(energy_consumption)
maximum_usage = np.max(memory_usage)

objective_value = 0
for user in sorted_users:
    for server in sorted_servers:
        if(memory_usage[user] <= remaining_capacity[server]):            
                user_allocation[user] = server
                server_load[server].append(user)
                remaining_capacity[server] -= memory_usage[user]
                objective_value += (maximum_usage-memory_usage[user]+1) * (maximum_energy_consumption-energy_consumption[server]+1)            
                break
population = generate_population(100, memory_usage, energy_consumption, initial_capacity)
if(len(user_allocation[user_allocation==-1])==0):
    print("All users were allocated !")
else:
    print(str(len(user_allocation[user_allocation==-1]))+" users were not allocated !")
    print("Minimum left user usage = "+str(np.min(memory_usage[user_allocation==-1]))+"MB")
print("Maximum remaining capacity = "+str(np.max(remaining_capacity))+"MB")
print("Overall remaining capacity = "+str(np.sum(remaining_capacity))+"MB")
print("Energy consumption = "+str(objective_value)+" W")

plt.figure(1)
plt.title("Remaining memory per server (MB)")
plt.bar(np.linspace(0,n_servers-1,n_servers), remaining_capacity)
plt.figure(2)
plt.title("Number of users allocated per server")
plt.bar(np.linspace(0,n_servers-1,n_servers), [len(users) for users in server_load])
plt.figure(3)
plt.bar(np.linspace(0,n_servers-1,n_servers), initial_capacity)
plt.figure(4)
plt.bar(np.linspace(0,n_servers-1,n_servers), (initial_capacity-remaining_capacity)*energy_consumption)
