import csv


def write(data, path):
    with open(path, 'a') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(data)
    pass


def make_new(path):
    with open(path, 'w') as csvfile:
        fieldnames = ['Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude', 'MD5', 'SHA1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    pass
