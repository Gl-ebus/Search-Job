# Generated by Django 4.1.1 on 2022-10-01 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company_app', '0002_company_owner'),
        ('vacancy_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies_comp', to='company_app.company'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_from',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_to',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancy_app.specialty'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('cover_letter', models.TextField(max_length=3000)),
                ('resp_vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancy_app.vacancy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
