from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

input_json = None
with open("input.json", "r") as f:
    input_json = json.load(f)
vertices = input_json["vertices"]

start_vertex = input_json["start_vertex"]
edges = []

driver = webdriver.Firefox()
driver.get("https://www.google.com/maps/dir/?hl=en")

elem = driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[4]/button")
elem.click()

for i in range(len(vertices)):
    for j in range(len(vertices)):
        if i == j:
            break
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
                print(f"{len(edges)}/{int((len(vertices)*(len(vertices)-1)/2))}")
                break
            except Exception:
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