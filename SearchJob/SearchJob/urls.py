"""SearchJob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

from company_app.views import *
from profile_app.views import RegisterUserView, LoginUserView
from vacancy_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView.as_view(), name='home'),
    path('find/vacancies/', FindVacanciesView.as_view(), name='search_query'),
    path('vacancies/specialty/<str:code>',VacanciesListInSpecView.as_view(), name='vacanc_in_spec'),
    path('vacancies/company/<int:pk>',VacanciesListCompanyView.as_view(), name='vacanc_in_comp'),
    path('vacancies/',AllVacanciesListView.as_view(), name='all_vacancies'),
    path('vacancy/<int:pk>/',VacancyDetailView.as_view(), name='vacancy'),

    path('profile/company_start/', CompanyStartView.as_view(), name='company_start'),
    path('profile/company/create/', CompanyCreateView.as_view(), name='company_create'),
    path('profile/company/edit/<int:pk>', CompanyUpdateView.as_view(), name='company_edit'),
    path('profile/company/<int:pk>/vacancies/', CompanyVacanciesView.as_view(), name='company_vacancies'),
    path('profile/company/<int:pk>/vacancies/create/', CompanyVacancyCreateView.as_view(), name='company_vac_create'),
    path('profile/company/<int:pk>/vacancy/update/<int:pk_vac>/', CompanyVacancyUpdateView.as_view(), name='company_vac_update'),
    path('profile/company/<int:pk>/vacancy/response/<int:pk_vac>/', CompanyVacancyResponseView.as_view(), name='company_vac_resp'),
    path('profile/company/<int:pk>/vacancy/del/<int:pk_vac>/', CompanyVacancyDelView.as_view(), name='company_vac_del'),
    path('profile/company/<int:pk>/del/', CompanyDelView.as_view(), name='company_del'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]

urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
