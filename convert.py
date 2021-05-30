import json

with open("itviec_data_hanoi_backup.txt") as f:
    for line in f.readlines():
        print(line)
        line = line[:-1] + "," + "\n"
        with open("itviec_data_hanoi_json.txt", "a") as file:
            file.writelines(line)