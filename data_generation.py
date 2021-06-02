import csv
import random
import time


def generate_header(fieldnames, filename):
    with open (file=filename, mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
        csv_writer.writeheader()


def generate_random_data(fieldnames, filename, initial):
    index = 0
    with open(file=filename, mode='a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
        info = dict(zip(["Id"] + fieldnames, [index] + initial))
        csv_writer.writerow(info)
        random_data = initial
    while True:
        with open(file=filename, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
            random_data[:] = [x + random.randint(-5,5) for x in random_data]
            info = dict(zip(["Id"] + fieldnames, [index] + random_data))
            csv_writer.writerow(info)
            print(random_data)
            index = index + 1
        time.sleep(0.5)

def add_column_in_csv(input_file, output_file, func):
    main()
    with open(input_file, 'r') as read:
        csv_reader = csv.reader(read)
        with open(output_file, 'w', newline='\n') as write:
            for row in csv_reader:
                func(row, csv_reader.line_num)
                csv.writer.writerow(row)

def add_index_column_in_csv(input_file, output_file, id = "Id"):
        add_column_in_csv(input_file, output_file, lambda row, line_num: row.insert(0,id) if line_num == 1 else row.insert(0,line_num - 1))


# if __name__ == "__main__":
def main():
    strings = ["value1", "value2", "value3", "value4"]
    initial = [1000, 1000, 1000,1000]
    generate_header(strings, "data.csv")
    generate_random_data(strings, "data.csv",initial)
    add_index_column_in_csv("data.csv", "data1.csv")