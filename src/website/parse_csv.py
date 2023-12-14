import csv
import os
import json

def parse_all(to_csv, to_json, date_range):
    if type(date_range) == int:
        date_range = [date_range, date_range]

    path = os.getcwd()
    abs_path = os.path.join(path[:path.index("SeminarniPraceM") + len("SeminarniPraceM")], "src/tmp")

    #read CSV files and output them to output.json
    all_dict = {
        "roky": []
    }
    start_date = 2004
    i_date = 0

    for filename in os.listdir(abs_path):
        total_num = 0
        file_path = os.path.join(abs_path, filename)

        if os.path.isfile(file_path) and not (filename == ".gitkeep" or filename == "output.csv" or filename == "output.json" or "lock" in filename):
            date = start_date + i_date

            countries = {}
            counties = {}
            ages = {}

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

            #read all the arrays

            #přečtení všech krajů
            for county in counties_data:
                county = county.lower()

                #validace setů
                found_key = False
                for key in counties:
                    if county == key:
                        counties[county] += 1
                        found_key = True
                        break
                    
                if not found_key:
                    counties[county] = 1

            #přečtení všech států ze kterých cizinci pocházejí
            for country in countries_data:
                country = country.lower()

                #validace setů
                found_key = False
                for key in countries:
                    if country == key:
                        countries[country] += 1
                        found_key = True
                        break
                    
                if not found_key:
                    countries[country] = 1

            #přečtení všech věků cizinců
            for age in ages_data:
                #validace setů
                found_key = False
                for key in ages:
                    if age == key:
                        ages[age] += 1
                        found_key = True
                        break
                    
                if not found_key:
                    ages[age] = 1

            #validace (jestli náhodou nekompletní data)

            #pro státy
            i = 0
            while i < len(countries):
                key = list(countries)[i]
                val = list(countries.values())[i]

                if len(key) == 0:
                    countries.pop(key)
                    i -= 1

                    try: 
                        countries["nezjištěno"] += val
                    except Exception as E:
                        #country "nezjištěno" was not created yet
                        countries["nezjištěno"] = val
                i += 1

            #pro města
            try:
                counties.pop("nezjištěno")
            except Exception as E:
                #county "nezjištěno" does not exist
                pass

            all_dict["roky"].append({
                "rok": date,
                "ciz_celk_poc": total_num,
                "ciz_poc_stat": countries,
                "ciz_poc_obec": counties,
                "ciz_vek": ages
            })

            i_date += 1
    
    
    if to_json:
        #přidat do celkového output.json souboru
        with open(os.path.join(abs_path, "output.json"), "w") as outfile: 
            json.dump(all_dict, outfile, indent=4, ensure_ascii=False)

    if to_csv:
        #reparse back to different csv
        fields = ["Obec"]
        data = []

        #přidání obcí do datasetu
        for county_str in all_dict["roky"][0]["ciz_poc_obec"]:
            data.append([county_str])

        #přidání dat obcí do datasetu
        for date in all_dict["roky"]:
            if date_range[0] <= date["rok"] <= date_range[1]:
                fields.append("Počet cizinců: " + str(date["rok"]))

                for county in date["ciz_poc_obec"]:
                    for data_curr in data:
                        if data_curr[0] == county:
                            data_curr.append(date["ciz_poc_obec"][county])

        with open(os.path.join(abs_path, "output.csv"), "w") as outfile:
            csvWriter = csv.writer(outfile)
            csvWriter.writerow(fields)
            csvWriter.writerows(data)

if __name__ == "__main__":
    parse_all(to_csv=True, to_json=True, date_range=[2011, 2014])