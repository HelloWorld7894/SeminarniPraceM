import csv
import os
import json

def parse_all():
    path = os.getcwd()
    abs_path = os.path.join(path[:path.index("SeminarniPraceM") + len("SeminarniPraceM")], "src/tmp")

    #read CSV files and output them to output.json
    all_dict = {
        "roky": []
    }
    start_date = 2004
    i_date = 0
    for filename in os.listdir(abs_path):
        file_path = os.path.join(abs_path, filename)
        if os.path.isfile(file_path) and filename != ".gitkeep":

            date = start_date + i_date
            countries = {}
            counties = {}
            age = {}

            ages_data = []
            counties_data = []
            countries_data = []

            with open(file_path, newline="") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for i, row in enumerate(csv_reader):
                    if i > 0:
                        try:
                            if len(row[18]) > 0:
                                age_dist = row[18].split(", ")
                                age1 = age_dist[1][:len(age_dist[1]) - 1]
                                age2 = age_dist[0][1:]

                                if "N" in age2:
                                    ages_data.append(int(age1))
                                    continue

                                if "N" in age1:
                                    ages_data.append(int(age2))
                                    continue

                                age_diff = round((int(age2) - int(age1)) / 2)
                                age = int(age1) + age_diff
                                ages_data.append(age)

                            if row[14] != "Česká republika": #We dont take česká republika as a county
                                counties_data.append(row[14])
                                countries_data.append(row[17])
                        except(IndexError):
                            #incomplete data, pass
                            continue

            i_date += 1

            #read all the arrays
            #TODO


if __name__ == "__main__":
    parse_all()