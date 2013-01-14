from django.db import models

class PhonoString(models.Model):
    Transcription = models.CharField(max_length=300)
    NoStress = models.CharField(max_length=300)

    def __unicode__(self):
        return self.Transcription
