from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

vertices = [
    [1, "31.93658, 34.78899", 0],
    [2, "31.92992, 34.781", 3],
    [3, "31.94135, 34.80062", 4],
    [4, "31.93891, 34.81156", 6],
    [5, "31.94809, 34.80152", 6],
    [6, "31.95056, 34.78422", 6],
    [7, "31.92449, 34.7977", 4],
    [8, "31.92587, 34.81443", 8],
    [9, "31.93522, 34.78764", 1],
    [10, "31.94487, 34.81996", 8],
    [11, "31.93995, 34.82773", 8],
    [12, "31.95211, 34.7846", 6],
    [13, "31.95903, 34.80198", 9],
    [14, "31.93609, 34.77833", 3],
    [15, "31.95175, 34.82562", 8],
    [16, "31.9543, 34.81442", 7]
]

start_vertex = 1

profits = [

]

map_vertex = list(range(1, len(vertices) + 1))

edges = []

driver = webdriver.Firefox()
driver.get("https://www.google.com/maps/dir/?hl=en")

elem = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[4]/button")
elem.click()

for i in range(len(vertices)):
    for j in range(i+1,len(vertices)):
        elem = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")
        elem.clear()
        elem.send_keys(vertices[i][1])

        elem = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input")
        elem.clear()
        elem.send_keys(vertices[j][1])
        elem.send_keys(Keys.ENTER)

        k = 0
        delay = 1
        while True:
            time.sleep(delay)
            try:
                elem = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[3]/div[1]/div[2]")
                distance = elem.text

                if distance[-2:] == "km":
                    distance = int(float(distance[:-2])*1000)
                else:
                    distance = int(distance[:-2])

                edges.append((i, j, distance))
                print(f"from {vertices[i][0]} to {vertices[j][0]} is {distance} meters")
                print(f"{len(edges)}/{int(len(vertices)*(len(vertices)-1)/2)}")
                break
            except:     
                if k >= 10:
                    input("refresh and complete captcha")
                k += delay

driver.close()

result = {
    "Profits": [],
    "VertexMap": [],
    "Edges": []
}

for i in range(len(vertices)):
    if vertices[i][0] == start_vertex:
        result["Profits"].insert(0, vertices[i][2])
        result["VertexMap"].insert(0, vertices[i][0])
        continue
    result["Profits"].append(vertices[i][2])
    result["VertexMap"].append(vertices[i][0])

result["Edges"] = edges

with open("graph.json", "w") as f:
    json.dump(result, f)