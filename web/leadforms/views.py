from django.views.generic import FormView
from django.urls import reverse_lazy
from django.utils.html import escape
from django_ratelimit.core import is_ratelimited
from django.shortcuts import get_object_or_404
from .forms import ContactForm, FinancingForm, ShippingForm, CarLeadForm
from .models import Lead
from .telegram import send_message


class RateLimitedFormView(FormView):
    rate = "5/m"

    def dispatch(self, request, *args, **kwargs):
        limited = is_ratelimited(
            request,
            group=f"leadforms:{getattr(self, 'kind', 'generic')}",
            key="ip",
            rate=self.rate,
            method="POST",
            increment=True,
        )
        if limited and request.method == "POST":
            from django.http import HttpResponseTooManyRequests
            return HttpResponseTooManyRequests("Слишком часто. Попробуйте позже.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        req = self.request

        # собрать extra из POST, чтобы не терять новые поля
        extra = {
            k: v
            for k, v in req.POST.items()
            if k
            not in {
                "csrfmiddlewaretoken",
                "website",
                "name",
                "first_name",
                "last_name",
                "email",
                "phone",
                "message",
            }
        }

        lead = Lead.objects.create(
            kind=self.kind,
            name=form.cleaned_data.get("name", ""),
            email=form.cleaned_data.get("email", ""),
            phone=form.cleaned_data.get("phone", ""),
            message=form.cleaned_data.get("message", ""),
            extra=extra,
            source_url=req.headers.get("Referer", ""),
            user_agent=req.headers.get("User-Agent", ""),
            ip=req.META.get("REMOTE_ADDR"),
            car=getattr(self, "car", None),
        )

        parts = [
            f"<b>Новая заявка: {escape(self.kind)}</b>",
            f"Имя: {escape(lead.name)}",
            f"Email: {escape(lead.email)}",
            f"Телефон: {escape(lead.phone)}",
        ]
        if lead.car:
            parts.append(f"Авто: {escape(lead.car.title)}")
        if lead.message:
            parts.append(f"Сообщение:\n{escape(lead.message)}")
        if lead.extra:
            parts.append(f"Детали: {escape(str(lead.extra))}")
        parts.append(f"URL: {escape(lead.source_url)}")

        send_message("\n".join(parts))
        return super().form_valid(form)


class ContactView(RateLimitedFormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("thanks")
    kind = Lead.CONTACT


class FinancingView(RateLimitedFormView):
    template_name = "pages/financing.html"
    form_class = FinancingForm
    success_url = reverse_lazy("thanks")
    kind = Lead.FINANCING


class ShippingView(RateLimitedFormView):
    template_name = "pages/shipping.html"
    form_class = ShippingForm
    success_url = reverse_lazy("thanks")
    kind = Lead.SHIPPING


class CarLeadView(RateLimitedFormView):
    template_name = "cars/car_detail.html"
    form_class = CarLeadForm
    success_url = reverse_lazy("thanks")
    kind = Lead.CAR

    def dispatch(self, request, *args, **kwargs):
        from cars.models import Car
        self.car = get_object_or_404(Car, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)
