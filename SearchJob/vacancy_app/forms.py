from django.core.exceptions import ValidationError
from django.forms import ModelForm

from vacancy_app.models import Response


class ResponseForm(ModelForm):
	class Meta:
		model = Response
		fields = ['name', 'phone', 'cover_letter']

	def clean_phone(self):
		"""Валидация ввёденного номера телефона"""

		# обрезаем стандартные символы,
		# которые обычно указывают в номерах телефонах (+, -,  ., " ")
		phone_num = self.cleaned_data['phone'].translate(str.maketrans('', '', '+-. '))
		if not phone_num.isnumeric():
			raise ValidationError("в номере телефона необходимо указать только цифры")
		elif len(phone_num) > 12:
			raise ValidationError(
				"Кол-во цифр указанного тел.номера больше 12, "
				"это не соответствует нумерации мобильных телефонов в РФ"
			)
		elif len(phone_num) < 11:
			raise ValidationError(
				"Кол-во цифр указанного тел.номера меньше 11,"
				" это не соответствует нумерации мобильных телефонов в РФ"
			)

		return phone_num
