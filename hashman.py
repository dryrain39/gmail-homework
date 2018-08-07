import hashlib


def hashall(inputfile):
    f = open(inputfile, 'rb')
    data = f.read()
    f.close()

    r = {
        'MD5': hashlib.md5(data).hexdigest(),
        'SHA1': hashlib.sha1(data).hexdigest()
    }

    return r
