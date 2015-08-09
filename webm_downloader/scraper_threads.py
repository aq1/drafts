# -*- coding: utf8 -*-

try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

import os
import sys
import threading
from cStringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist

os.environ["DJANGO_SETTINGS_MODULE"] = "WillBeams.settings"
sys.path.append("WillBeams/")

from will_beams import models


urls = []

FOLDER = 'webm'


def save_file(name, data, mdb, semaphore):
    with open(os.path.join(FOLDER, name), 'wb') as f:
        f.write(data)

    print('Finished %s' % name)


def get_url(url, md5, semaphore):
    try:
        models.Webm.increase_rating(md5)
    except ObjectDoesNotExist:
        raw_data = request.urlopen(url)
        save_to_django_model(name=url.split('/')[-1],
                             data=raw_data.read(),
                             semaphore=semaphore,
                             md5=md5)
    finally:
        semaphore.release()


def save_to_django_model(name, data, md5, semaphore=None):
    buf = StringIO(data)
    buf.seek(0, 2)
    webm = InMemoryUploadedFile(
        buf, 'video', name, None, buf.tell(), None)
    django_webm = models.Webm(md5=md5)
    django_webm.video.save(name, webm)


def main(urls):
    print('PID %s has started for %s webms' %
          (os.getpid(), len(urls)))

    semaphore = threading.BoundedSemaphore(value=2)
    with semaphore:
        try:
            for url, md5 in urls:
                print('Starting %s' % url)
                semaphore.acquire()
                t = threading.Thread(
                    target=get_url, args=(url, md5, semaphore))
                t.daemon = True
                t.start()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    main()
