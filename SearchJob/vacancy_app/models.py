from django.db import models
from company_app.models import Company
from SearchJob.settings import MEDIA_SPECIALITY_LOGO


class Specialty(models.Model):
	code = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	picture = models.ImageField(upload_to=MEDIA_SPECIALITY_LOGO)

	def __str__(self):
		return f'{self.name}'


class Vacancy(models.Model):
	title = models.CharField(max_length=80)
	specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE,
	                              related_name='vacancies', verbose_name='Специализация')
	company = models.ForeignKey(Company, on_delete=models.CASCADE,
	                            related_name='vacancies_comp')
	salary_from = models.PositiveIntegerField(verbose_name='Зарплата от')
	salary_to = models.PositiveIntegerField(verbose_name='Зарплата до')
	skills = models.CharField(max_length=240, verbose_name='Навыки')
	description = models.TextField(max_length=3000)
	posted = models.DateField(auto_now_add=True)
	is_published = models.BooleanField(default=True)

	def __str__(self):
		return f'"{self.title}" в {self.company} (от {self.salary_from} руб)'

	class Meta:
		ordering = ['posted']


class Response(models.Model):
	name = models.CharField(max_length=64, verbose_name='ФИО')
	phone = models.CharField(max_length=15, verbose_name='Моб.телефон')
	cover_letter = models.TextField(max_length=3000, verbose_name='Сопров.письмо')
	resp_vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE,
	                                 related_name='vacancies_resp')

	def __str__(self):
		return f'{self.name} откликнулся на {self.resp_vacancy}'
