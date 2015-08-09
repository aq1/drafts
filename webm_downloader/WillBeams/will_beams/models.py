from django.db import models
from django.db.models import F
# from django.contrib.auth.models import User


class Webm(models.Model):
    video = models.FileField(upload_to='webm/%Y/%m/%d')
    rating = models.IntegerField(default=0)
    md5 = models.CharField(db_index=True, unique=True, max_length=16, editable=False)
    nsfw = models.BooleanField(default=False)

    @classmethod
    def _change_rating(cls, md5, value):
        webm = cls.objects.get(md5=md5)
        webm.rating = F('rating') + value
        webm.save()

    @classmethod
    def increase_rating(cls, md5):
        cls._change_rating(md5, 1)

    @classmethod
    def decrease_rating(cls, md5):
        cls._change_rating(md5, -1)

    def is_safe_for_work(self):
        return not self.nsfw

    is_safe_for_work.boolean = True
    is_safe_for_work.short_description = 'Safe for work?'

    def __unicode__(self):
        return self.video.url.split('/')[-1]


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)


class WebmTag(models.Model):
    webm = models.ForeignKey(Webm)
    tag = models.ForeignKey(Tag)
