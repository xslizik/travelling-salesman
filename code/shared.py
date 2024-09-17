import math
import random
from tkinter import *
import sys

class Individual:
    def __init__(self, points, distances, path):
        self.path = path
        self.fitness = determineFitness(points, distances, path)

# manifest result
def offset(position) -> int:
    return position * 3

def draw(points, best_path):
    master = Tk()
    w = Canvas(master, width=700, height=700)
    w.pack()
    index = 0
    master.title('Best Path')
    print(f"Best Path {best_path}")
    for i in range(0, len(best_path) - 1):
        w.create_line(offset(points[best_path[i]][0]) + 5, offset(points[best_path[i]][1]) + 5, offset(points[best_path[i+1]][0]) + 5, offset(points[best_path[i+1]][1]) + 5, width="2")
    
    w.create_line(offset(points[best_path[-1]][0]) + 5, offset(points[best_path[-1]][1]) + 5, offset(points[best_path[0]][0]) + 5, offset(points[best_path[0]][1]) + 5)
    for point in points:
        r = 3
        w.create_oval(offset(point[0]), offset(point[1]), offset(point[0]+ r), offset(point[1] + r), fill="red")
        w.create_text((offset(point[0]) + offset(point[0] + r)) / 2, (offset(point[1])+ offset(point[1] + r)) / 2 + 13, 
        fill="black", font="Times 12 bold", text=index)
        index += 1

    mainloop()

# initiate first population and base information
def generateRandomPath(length) -> list:
    return random.sample([i for i in range(0,length)], length) 

def determineFitness(points, distances, path):
    fitness = 0
    for i in range(0, len(path)):
        if i != len(path) - 1: 
            first_key = distanceHash(points, path[i], path[i+1])
            second_key = distanceHash(points, path[i+1], path[i])
        else:
            first_key = distanceHash(points, path[-1], path[0]) 
            second_key = distanceHash(points, path[0], path[-1]) 
        if first_key in distances: 
            fitness += distances[first_key] 
        elif second_key in distances:
            fitness += distances[second_key] 
    
    return (1/fitness)

def distanceHash(points, from_point, to_point) -> str:
    return (str(points[from_point]) + str(points[to_point]))
        
def initDistances(points) -> dict:
    paths = {}
    for i in range(0,len(points)):
        for j in range(i+1, len(points)):   
            x = abs(points[j][0] - points[i][0])
            y = abs(points[j][1] - points[i][1])
            distance = math.sqrt(pow(x,2) + pow(y,2))
            paths.update({distanceHash(points, i, j) : distance})

    return paths

def openFile(file_path):
    points = []
    try:
        with open(file_path) as f:
            for line in f:
                tmp = line.strip().split()
                tmp = [eval(i) for i in tmp]
                points.append(tmp)
            return points
    except IOError:
        print("File does not exist")
        sys.exit()

def initBase(file_path) -> list:
    base = []
    if file_path:
        base.append(openFile(file_path))
    else:
        points = []
        num = 0
        while num <= 1:
            while True:
                try:
                    num = input("number of points: ")
                    num = int(num)
                    break
                except ValueError:
                    print("invalid input")
            
        for _ in range(0, num):
            point = [int(random.random() * 200), int(random.random() * 200)]
            points.append(point)
        base.append(points)

    base.append(initDistances(base[0]))
    return base