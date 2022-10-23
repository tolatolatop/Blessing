from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, CreateView

from .models import Search


class SearchCreateView(CreateView):
    model = Search
    fields = ('name', 'query')
    template_name = 'search.html'

    def form_valid(self, form):
        return super().form_valid(form)


class SearchDetailView(DetailView):
    model = Search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
