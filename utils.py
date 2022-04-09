# probably use this for handy functions
import os
import csv
import json

# put in a csv

# append to files


def create_file(name):
    if not os.path.exists("data/"):
        os.mkdir("data")
    file = open(f"data/{name}.csv", "w", newline="")
    return file


def create_json_file():
    if not os.path.exists("qlearn/"):
        os.mkdir("qlearn")
    file = open("qlearn/q_vals.json", "w", newline="")
    return file


def load_from_json():
    file = open("qlearn/q_vals.json", "r", newline="")
    json_qvals = json.loads(file.read())
    return json_qvals
# csv_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
# csv_writer.writerow([])
