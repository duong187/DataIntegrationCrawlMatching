import json

with open("vietnamwork_data_hanoi.txt") as f:
    for line in f.readlines():
        print(line)
        line = line[:-1] + "," + "\n"
        with open("vietnamworkdata_hanoi_json.txt", "a") as file:
            file.writelines(line)