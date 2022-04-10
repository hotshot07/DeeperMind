# probably use this for handy functions
import os
import csv
import json

#put in a csv

#append to files
def create_file(name):
    if not os.path.exists("plot_data/"):
        os.mkdir("plot_data")
    file = open(f"plot_data/{name}.csv", "w", newline="")
    return file

def write_to_file(file, name, wins, ties, losses):
    csv_writer = csv.writer(file)
    csv_writer.writerow([name]+ [wins] + [ties] + [losses])

def write_col_names(file):
    csv_writer = csv.writer(file)
    csv_writer.writerow(['name']+ ['wins'] + ['ties'] + ['losses'])
# def create_json_file():
#     if not os.path.exists("qlearn/"):
#         os.mkdir("qlearn")
#     file = open("qlearn/q_vals.json", "w", newline="")
#     return file


# def load_from_json():
#     file = open("qlearn/q_vals.json", "r", newline="")
#     json_qvals = json.loads(file.read())
#     return json_qvals