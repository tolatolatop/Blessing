import json
from datetime import datetime, timedelta, timezone

from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, CreateView

from .common import call_snscrape, save_tweet
from .models import Search
from comments.models import Tweet


class SearchCreateView(CreateView):
    model = Search
    fields = ('name', 'query')
    template_name = 'sns/search.html'

    def form_valid(self, form):
        resp = super().form_valid(form)
        result = call_snscrape(self.object)
        tweets = save_tweet(result)
        return resp


class SearchDetailView(DetailView):
    model = Search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_obj: Search = context['object']
        life = timedelta(days=1)
        now = datetime.now(timezone.utc)
        if (now - search_obj.modified) > life:
            result = call_snscrape(search_obj)
            tweets = save_tweet(result)
        else:
            tweets = Tweet.objects.filter(search=search_obj)
        context["tweets"] = tweets
        return context
