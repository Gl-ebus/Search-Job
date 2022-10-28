from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from company_app.models import Company


class OnlyUserCompanyMixin(LoginRequiredMixin):
	""" Checking that the request came from the owner of the company.
		Only the owner of the company can change the information about
		the company and work with vacancies.
	    Also return pk company in context data"""

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk_company'] = self.kwargs['pk']
		return context

	def dispatch(self, request, *args, **kwargs):
		company_in_url = get_object_or_404(Company.objects.only('owner'), id=self.kwargs['pk'])
		if request.user.id != company_in_url.owner.id:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)
