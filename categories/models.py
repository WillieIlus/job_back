from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count


class CategoryManager(models.Manager):
    def with_jobs_count(self):
        return self.annotate(total_jobs_count=Count('job'))


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    job_count = models.PositiveIntegerField(blank=True, null=True)

    objects = CategoryManager()  # Use the custom manager

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-job_count', 'name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # self.job_count = self.get_active_jobs_count()
        super(Category, self).save(*args, **kwargs)

    def get_jobs(self):
        return self.jobs.all()

    def get_active_jobs(self):
        return self.jobs.filter(active=True)

    def get_active_jobs_count(self):
        return self.jobs.filter(active=True).count()
