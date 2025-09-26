""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

from functools import reduce

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    count = 0
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []
    for p in range(n):
         x = random.uniform(-1,1)
         y = random.uniform(-1,1)
         if x**2 + y**2 <= 1:
            count = count + 1
            x_inside.append(x)
            y_inside.append(y)
         else:
            x_outside.append(x)
            y_outside.append(y)

    print(f"the number of points is :{n}, the approximation of pi is {count/n*4}")
    plt.figure(figsize=(6,6))
    plt.scatter(x_inside, y_inside, color='red', s=1)
    plt.scatter(x_outside, y_outside, color='blue', s=1)
    plt.title(f"Monte Carlo π Approximation (n={n})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-1, 1)  
    plt.ylim(-1, 1)  
   
    plt.savefig(f"monte_carlo_pi_{n}.png")
    plt.close()
    return count/n*4

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    
    points = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    squared_sums = list(map(lambda p: reduce(lambda acc, x: acc + x**2, p, 0), points))
    inside_points = list(filter(lambda s: s <= 1, squared_sums))

    volume = 2**d
    return (len(inside_points) / n) * volume

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    return m.pi**(d/2) / m.gamma(d/2 + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    results = []

    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, n, d) for _ in range(np)]
        for f in futures:
            results.append(f.result())
    
    return sum(results)/np

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    n_s = int(n/np)
    results = []

    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, n_s, d) for _ in range(np)]
        for f in futures:
            results.append(f.result())
    return sum(results)/np

    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"approximation volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"approximation volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    average = 0
    for y in range (10):
        average += sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}, average of the functions’ outputs: {average/10}")
    print("What is parallel time?")
    start = pc()
    result = sphere_volume_parallel1(n,d)
    stop = pc()
    print(f"Ex3: parallel time of {d} and {n}: {stop-start}, average of the functions’ outputs: {result}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start = pc()
    result_2 = sphere_volume_parallel2(n,d)
    stop = pc()
    print(f"Ex4: parallel time of {d} and {n}: {stop-start}, average of the functions’ outputs: {result_2}")

    
    

if __name__ == '__main__':
	main()
