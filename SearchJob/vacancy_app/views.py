from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import BaseFormView
from django.contrib import messages

from vacancy_app.forms import ResponseForm
from vacancy_app.models import Specialty, Vacancy
from company_app.models import Company
from django.db.models import Count, Q


class HomeView(TemplateView):
	template_name = 'vacancy_app/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['specialties'] = Specialty.objects.annotate(vacancy_count=Count(
			'vacancies', filter=Q(vacancies__is_published=True)))

		# 8 крупных компаний (по кол-ву сотрудников) +
		# кол-во опубликованных вакансий по ним (vacancy_count)
		context['companies'] = Company.objects.only('id', 'logo', 'employee_count'). \
			                       order_by('-employee_count')[:8]. \
			annotate(vacancy_count=Count(
				'vacancies_comp',
				filter=Q(vacancies_comp__is_published=True)
				)
			)
		return context


# Представление для поиска
class FindVacanciesView(ListView):
	template_name = 'vacancy_app/vacancies_find.html'

	def get_queryset(self):
		search_query = self.request.GET.get('find').lower()
		res = Vacancy.objects.defer(
			'description', 'specialty',
			'salary_to', 'posted',
			'company__description', 'company__owner'). \
			filter(
			Q(is_published=True),
			Q(title__icontains=search_query) |
			Q(skills__icontains=search_query)
		).select_related('company').order_by('-salary_from')

		return res


# Представление для вакнсий по Специализации
class VacanciesListInSpecView(ListView):
	template_name = "vacancy_app/vacancies_in_spec.html"
	paginate_by = 4

	def get_queryset(self):
		spec = self.kwargs['code']
		get_query = Vacancy.objects.defer(
			'description', 'company__employee_count',
			'company__description', 'company__owner',
			'company__title', 'company__location',
			'specialty__picture'
		).filter(is_published=True, specialty__code=spec). \
			select_related('specialty', 'company')

		return get_query


# Представление для вакансий по Компании
class VacanciesListCompanyView(ListView):
	template_name = "vacancy_app/vacancies_company.html"
	paginate_by = 4

	def get_queryset(self):
		get_query = Vacancy.objects.defer(
			'description', 'company__employee_count',
			'company__description', 'company__owner',
			'company__title', 'company__location',
			'specialty__picture'
		).filter(company__pk=self.kwargs['pk'], is_published=True). \
			select_related('company', 'specialty')

		return get_query


# Представление для отображения всех опубликованных вакансий
class AllVacanciesListView(ListView):
	paginate_by = 4
	model = Vacancy
	template_name = "vacancy_app/vacancies_all.html"

	queryset = Vacancy.objects.defer('description'). \
		filter(is_published=True). \
		select_related('specialty', 'company')


# Представление для конкретной вакансии и обработка формы отклика
class VacancyDetailView(DetailView, BaseFormView):
	template_name = "vacancy_app/vacancy_detail.html"
	model = Vacancy
	form_class = ResponseForm

	def get_object(self, queryset=None):
		obj = get_object_or_404(
			Vacancy.objects.select_related(
				'company', 'specialty'), id=self.kwargs['pk']
		)
		return obj

	def get_context_data(self, form=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = form or self.form_class()
		return context

	def form_valid(self, form):
		resp = form.save(commit=False)
		resp.resp_vacancy = get_object_or_404(
			Vacancy.objects.only('id'),
			id=self.kwargs['pk']
		)
		resp.save()
		messages.success(self.request, 'Ваш отклик на данную вакансию отправлен')
		return super().form_valid(form)

	def form_invalid(self, form):
		self.object = self.get_object()
		messages.error(self.request, 'Ошибка отправки отклика')
		return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		return self.request.path
