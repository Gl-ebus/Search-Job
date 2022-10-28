from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView

from company_app.forms import CompanyForm, CompanyVacancyForm
from company_app.mixins import OnlyUserCompanyMixin
from company_app.models import Company
from vacancy_app.models import Vacancy, Response


class CompanyStartView(LoginRequiredMixin, TemplateView):
	template_name = 'company_app/company_start.html'

	def get(self, request, *args, **kwargs):
		company_user = Company.objects.only('owner').filter(owner=request.user)
		if company_user:
			return redirect('company_edit', company_user.first().pk)
		return super().get(self, request, *args, **kwargs)


class CompanyCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
	template_name = 'company_app/company_create.html'
	model = Company
	form_class = CompanyForm
	success_url = reverse_lazy('company_start')  # СДЕЛАТЬ ДРУГОЙ АДРЕС РЕДИРЕКТА ?!
	success_message = 'Ваша компания успешно зарегистрирована на Job Hunt'

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


class CompanyUpdateView(OnlyUserCompanyMixin, SuccessMessageMixin, UpdateView):
	template_name = 'company_app/company_edit.html'
	model = Company
	form_class = CompanyForm
	success_message = 'Информация о компании обновлена'
	success_url = reverse_lazy('home')


class CompanyDelView(OnlyUserCompanyMixin, SuccessMessageMixin, DeleteView):
	template_name = 'company_app/company_del.html'
	model = Company
	success_message = 'Информация о компании удалена с сайта'
	success_url = reverse_lazy('home')


# Представление для отображения списка заведённых вакансий
class CompanyVacanciesView(OnlyUserCompanyMixin, ListView):
	template_name = 'company_app/company_vacancies.html'

	def get_queryset(self):
		vac_list = Vacancy.objects.only('title',
		                                'salary_from',
		                                'is_published').filter(company__pk=self.kwargs['pk'])

		return vac_list.annotate(count_resp=Count('vacancies_resp'))


class CompanyVacancyCreateView(OnlyUserCompanyMixin, SuccessMessageMixin, CreateView):
	template_name = 'company_app/company_vacancy_create.html'
	model = Vacancy
	form_class = CompanyVacancyForm
	success_message = 'Вакансия успешно создана'

	def form_valid(self, form):
		form.instance.company = Company.objects.get(id=self.kwargs['pk'])
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('company_vacancies', kwargs={'pk': self.kwargs['pk']})


class CompanyVacancyUpdateView(OnlyUserCompanyMixin, SuccessMessageMixin, UpdateView):
	template_name = 'company_app/company_vacancy_edit.html'
	model = Vacancy
	pk_url_kwarg = 'pk_vac'
	form_class = CompanyVacancyForm
	success_message = 'Информация в вакансии успешно обновлена'

	def get_success_url(self):
		return reverse_lazy('company_vacancies', kwargs={'pk': self.kwargs['pk']})


# Представление для удаления владельцем вакансии
class CompanyVacancyDelView(OnlyUserCompanyMixin, SuccessMessageMixin, DeleteView):
	template_name = 'company_app/company_vacancy_del.html'
	model = Vacancy
	pk_url_kwarg = 'pk_vac'
	success_message = 'Вакансия удалена с сайта'

	def get_success_url(self):
		return reverse_lazy('company_vacancies', kwargs={'pk': self.kwargs['pk']})


# Представление для просмотра и удаления откликов по вакансии
class CompanyVacancyResponseView(OnlyUserCompanyMixin, ListView):
	template_name = 'company_app/company_vacancy_resp.html'

	def get_queryset(self):
		resp_vac = Response.objects. \
			select_related('resp_vacancy').filter(resp_vacancy=self.kwargs['pk_vac']). \
			only('name', 'phone', 'cover_letter', 'resp_vacancy__title')
		return resp_vac

	def post(self, *args, **kwargs):
		pk_resp = self.request.POST.get('resp_pk', None)
		obj = Response.objects.only('id').get(id=pk_resp)
		obj.delete()
		messages.success(self.request, 'Отклик удалён')
		return super().get(self.request, *args, **kwargs)
