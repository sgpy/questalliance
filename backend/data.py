
import csv

def generate(file_name):
    rs = []
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            reader = csv.reader(f, dialect="excel")
            for index, _ in enumerate(reader):
                rs.append(_)
    return rs

def load_sudent_data():
    rs = generate(file_name="./data/Indian-Female-Names.csv") + \
         generate(file_name="./data/Indian-Male-Names.csv")
    return rs


def load_languages():
    rs = generate(file_name="./data/INDIAN_LANGUAGE.csv")
    return rs


def load_courses():
    rs = generate(file_name="./data/courses.csv")
    return rs

if __name__ == '__main__':
    rs = load_courses()

    for i, data in enumerate(rs):
        print("{} = {}".format(i, data))