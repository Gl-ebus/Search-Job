from django.core.exceptions import ValidationError
from django.forms import ModelForm
from company_app.models import Company
from django import forms
from vacancy_app.models import Vacancy


class CompanyForm(ModelForm):
	class Meta:
		model = Company
		fields = ['title', 'employee_count', 'location', 'description', 'logo']

	def clean_logo(self):
		"""Проверить на ограничение по размеру файла логотипа - 2 Мб"""
		logo = self.cleaned_data['logo']
		size_logo_file = logo.size
		if size_logo_file > 2097152:
			raise ValidationError("Размер загруженного файла больше 2 Мб")
		return logo


class CompanyVacancyForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['specialty'].empty_label = '---Выберите Специализацию---'

	class Meta:
		model = Vacancy
		fields = ['title', 'specialty', 'salary_from', 'salary_to',
		          'skills', 'description', 'is_published']
		widgets = {
			'specialty': forms.Select()
		}
