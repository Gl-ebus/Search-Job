from django.contrib import admin
from vacancy_app.models import Vacancy, Specialty, Response
from company_app.models import Company

# Register your models here.


class VacancyAdmin(admin.ModelAdmin): pass

class SpecialtyAdmin(admin.ModelAdmin): pass

class CompanyAdmin(admin.ModelAdmin): pass

class ResponseAdmin(admin.ModelAdmin): pass

admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Response, ResponseAdmin)
