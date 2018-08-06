import hashlib

def hashall(inputfile):
    f = open(inputfile, 'rb')
    data = f.read()
    f.close()

    r = {'md5': hashlib.md5(data).hexdigest(),
         'SHA-1': hashlib.sha1(data).hexdigest(),
         'SHA-256': hashlib.sha256(data).hexdigest()}

    return r
