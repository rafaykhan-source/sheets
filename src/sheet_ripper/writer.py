import csv


def write_data(filename: str, data: list[str]):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)
