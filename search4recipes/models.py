from __future__ import unicode_literals

# for creating and manipulating models
from django.db import models
#for loading a translation of a string (Unicode support) in a lazy fashion
from django.utils.translation import ugettext_lazy as _
# for populating slug from another filed (generating unique URL)
from autoslug import AutoSlugField
#for rating filed
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
#for admin account
from django.contrib.auth.models import User
#for text editing
from django.utils.safestring import mark_safe
#for file processing
import os
from django.core.files.storage import FileSystemStorage

from io_site import settings


class Przepis(models.Model):
    """
    Model przepisu: tablica przepisow
    """
    nazwa_przepisu = models.CharField(max_length=250, verbose_name=_('Nazwa przepisu'))
    slug = AutoSlugField(_('slug'), populate_from='nazwa_przepisu', unique=True)
    czas_przygotowania = models.IntegerField(null=True, blank=True,help_text="Wprowadź czas w minutach.")
    zdjecie = models.ImageField(_('Zdjęcie przepisu'), blank=True, upload_to=settings.PHOTO_MEDIA_URL,
                                storage=FileSystemStorage(location = settings.FS_IMAGE_UPLOADS, base_url= settings.FS_IMAGE_URL))
    porcje = models.IntegerField(_('Porcje'), default=1, help_text=mark_safe("Wprowadź liczbę porcji:<br/>(domyśnie 1)"))
    ocena = GenericRelation(Rating, related_query_name='przepisy')
    #ocena = models.FloatField()

    def __unicode__(self):
        return self.nazwa_przepisu

    def __str__(self):
        return '{}'.format(self.nazwa_przepisu)


    def get_absolute_url(self):
        return "/przepis/%s/" % self.slug

    class Meta:
        ordering = ['nazwa_przepisu', 'czas_przygotowania']
        verbose_name = _('Przepis')
        verbose_name_plural = _('Przepisy')


class Skladnik(models.Model):
    """
    Model skladnika: tablica skladnikow przepisu
    """
    nazwa_produktu = models.CharField(_('nazwa'), max_length=250)
    skladnik_lm = models.CharField(max_length=250, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Skladnik, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.nazwa_produktu

    def __str__(self):
        return '{}'.format(self.nazwa_produktu)

    class Meta:
        ordering = ['nazwa_produktu']
        verbose_name = ('Składnik')
        verbose_name_plural = ('Składniki')


class Miara(models.Model):
    """
    Model miar: tablica jednostek miar skladnikow
    """
    jednostka_miary = models.CharField(max_length=250, unique=True, verbose_name=_('Jednostka miary'))
    skrot= models.CharField(max_length=60, blank=True, verbose_name=_('Skrót jednostki'))
    jednostka_miaryLm2_4 = models.CharField(max_length=250,blank=False, null=False,verbose_name=_('Jednostka w liczbie mnogiej (2-4)'))  #związek zgody, formy nmos związek rządu
    jednostka_miaryLm5plus = models.CharField(max_length=250,blank=False, null=False,verbose_name=_('Jednostka w liczbie mnogiej (5+) i ułamki'))  #związki rządu + ułamki


    def __unicode__(self):
        return self.jednostka_miary

    def __str__(self):
        return format(self.jednostka_miary)

    class Meta:
        verbose_name = _('Miara')
        verbose_name_plural = _('Miary')
        ordering = ['jednostka_miary']

class SkladnikiwPrzepisach(models.Model):
    """
    Model skladnikow w przepisach: tablica przepisow
    """
    skladnik = models.ForeignKey(Skladnik, verbose_name=_('Składnik'),on_delete=models.PROTECT)
    przepis = models.ForeignKey(Przepis, verbose_name=_('Przepis'),on_delete=models.PROTECT)
    miara = models.ForeignKey(Miara, verbose_name=_('Miara'), blank=False, null=False, on_delete=models.PROTECT)
    ilosc = models.FloatField(_('Ilość'), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.przepis.nazwa_przepisu

    def __str__(self):
        return '{} - {}'.format(self.przepis.nazwa_przepisu, self.skladnik.nazwa_produktu)

    def formatowanie_skladnika(self):
        if Skladnik.skladnik_lm is not None and Skladnik.skladnik_lm != '' and (self.ilosc != 1):
            skladnik_str = Skladnik.skladnik_lm
        else:
            skladnik_str = Skladnik.nazwa_produktu
        return skladnik_str

    def formatowanie_miary(self):
        if self.ilosc == 1:
            miara_str = Miara.jednostka_miary
        else:
            #wykluczamy ulamki, bierzemy przedzial 2-4
            if self.ilosc.is_integer() and self.ilosc < 5 and self.ilosc > 1:
                miara_str = Miara.jednostka_miaryLm2_4
            else:
                miara_str = Miara.jednostka_miaryLm5plus
        return miara_str

    class Meta:
        verbose_name = _('Składnik w przepisie')
        verbose_name_plural = _('Składniki w przepisach')