import json
from datetime import datetime, timedelta, timezone

from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, CreateView

from .common import call_snscrape, save_log_data, save_log_data_as_excel
from .models import Search
from comments.models import LogData


class SearchCreateView(CreateView):
    model = Search
    fields = ('name', 'query')
    template_name = 'sns/search.html'

    def form_valid(self, form):
        resp = super().form_valid(form)
        result = call_snscrape(self.object)
        save_log_data_as_excel(result)
        return resp


class SearchDetailView(DetailView):
    model = Search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_data_collect"] = {}
        return context
