# -*- coding: utf8 -*-

try:
    import urllib.request as request
    from io import StringIO
except ImportError:
    import urllib2 as request
    from cStringIO import StringIO

import os
import sys
import threading

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


def get_url(thumbnail, webm, md5, semaphore, download_thumbnail_only=True):
    try:
        models.Webm.increase_rating(md5)
    except ObjectDoesNotExist:
        thumbnail = (thumbnail.split('/')[-1], request.urlopen(thumbnail).read())

        if download_thumbnail_only:
            webm = None
        else:
            webm = (webm.split('/')[-1], request.urlopen(webm).read())

        save_to_django_model(thumbnail=thumbnail,
                             webm=webm,
                             semaphore=semaphore,
                             md5=md5)
    finally:
        semaphore.release()


def save_to_django_model(thumbnail, webm, md5, semaphore=None):
    django_webm = models.Webm(md5=md5)

    t_name, thumb = thumbnail
    thumb_buf = StringIO(thumb)
    thumb_buf.seek(0, 2)
    thumbnail = InMemoryUploadedFile(
        thumb_buf, 'thumbnail', t_name, None, thumb_buf.tell(), None)

    if webm:
        w_name, webm = webm
        webm_buf = StringIO(webm)
        webm_buf.seek(0, 2)
        webm = InMemoryUploadedFile(
            webm_buf, 'video', w_name, None, webm_buf.tell(), None)

        django_webm.video.save(w_name, webm)

    django_webm.thumbnail.save(t_name, thumbnail)


def main(urls, quantity='some', download_thumbnail_only=True):
    print('PID %s has started for %s webms' %
          (os.getpid(), quantity))
    semaphore = threading.BoundedSemaphore(value=2)
    while True:
        with semaphore:
            try:
                thumbnail, webm, md5 = urls.get()
                if not all((thumbnail, webm, md5)):
                    print('Thats all')
                    return

                print('Starting %s' % webm)
                semaphore.acquire()
                t = threading.Thread(
                    target=get_url, args=(thumbnail, webm, md5,
                                          semaphore, download_thumbnail_only))
                t.daemon = True
                t.start()
            except KeyboardInterrupt:
                exit()


if __name__ == '__main__':
    main()
