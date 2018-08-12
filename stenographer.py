import csv


def write(data, path):
    with open(path, 'a') as csvfile:
        fieldnames = ['Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude', 'MD5', 'SHA1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(data)
    pass


def make_new(path):
    with open(path, 'w') as csvfile:
        fieldnames = ['Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude', 'MD5', 'SHA1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    pass


def read(path):
    with open(path, 'r') as csvfile:
        r = list(csv.reader(csvfile))
        return r
    pass


def check(path):
    try:
        with open(path) as json_file:
            a = json_file
            return a
            pass
    except Exception:
        return False
