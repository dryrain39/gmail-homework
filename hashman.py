# -*- coding: utf-8 -*-

import hashlib


def hashall(inputfile):
    # 해쉬값을 개산해서 MD5와 SHA1로 리턴해준다.
    f = open(inputfile, 'rb')
    data = f.read()
    f.close()

    r = {
        'MD5': hashlib.md5(data).hexdigest(),
        'SHA1': hashlib.sha1(data).hexdigest()
    }

    return r
