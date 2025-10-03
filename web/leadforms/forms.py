from django import forms
import re

class BaseLeadForm(forms.Form):
    # имя может прийти как name или как first_name/last_name
    name = forms.CharField(max_length=120, required=False)
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)

    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    def clean(self):
        data = super().clean()

        if data.get("website"):
            raise forms.ValidationError("Spam detected")

        # собрать name из first/last если нужно
        name = (data.get("name") or f"{data.get('first_name','').strip()} {data.get('last_name','').strip()}").strip()
        if not name:
            raise forms.ValidationError("Укажите имя")
        data["name"] = name

        # нормализовать телефон до цифр
        if data.get("phone"):
            data["phone"] = re.sub(r"\D+", "", data["phone"])

        if not data.get("email") and not data.get("phone"):
            raise forms.ValidationError("Укажите email или телефон")

        return data


class ContactForm(BaseLeadForm):
    pass


class FinancingForm(BaseLeadForm):
    # в шаблоне кредит-скор — строки ("720+","660–719"...), делаем CharField
    credit_score = forms.CharField(required=False, max_length=32)
    income = forms.IntegerField(required=False, min_value=0)  # если пришлют это имя
    # остальные новые поля уйдут в extra через view


class ShippingForm(BaseLeadForm):
    # имена соответствуют шаблону
    from_zip = forms.CharField(max_length=16)
    to_zip = forms.CharField(max_length=16)


class CarLeadForm(BaseLeadForm):
    pass
