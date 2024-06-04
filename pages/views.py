from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class ContactUsPageView(TemplateView):
    template_name = 'contactuspage.html'
    
    
class DeliveryPageView(TemplateView):
    template_name = 'delivery.html'


class PaymentsPageView(TemplateView):
    template_name = 'payments.html'


class PolicyPageView(TemplateView):
    template_name = 'policy.html'


class ClientsPageView(TemplateView):
    template_name = 'clients.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class FAQPageView(TemplateView):
    template_name = 'faq.html'