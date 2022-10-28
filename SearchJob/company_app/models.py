from django.contrib.auth.models import User
from django.db import models
from SearchJob.settings import MEDIA_COMPANY_LOGO


class Company(models.Model):
	title = models.CharField(max_length=30)
	logo = models.ImageField(upload_to=MEDIA_COMPANY_LOGO, null=True, blank=True,
	                         verbose_name='Логотип')
	employee_count = models.PositiveSmallIntegerField(verbose_name='Кол-во сотрудников')
	location = models.CharField(max_length=100, verbose_name='География')
	description = models.TextField(max_length=3000)
	owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
	                             blank=True, related_name='company')

	def __str__(self):
		return f'{self.title}'

	# def get_absolute_url(self):
	# 	return reverse('company_edit', kwargs={'pk': self.pk})
