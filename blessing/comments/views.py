import json

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.conf import settings

from .models import LabelModel, Report, Tweet
from .form import CommentForm, ReportCommentForm, FilterForm
from rest_framework import viewsets
from .restful import TweetSerializer, StandardResultsSetPagination


class TimelineView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = TweetSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        saved_filter = self.request.session.get("saved_filter", {})
        return Tweet.objects.filter(**saved_filter)


class LabelDetailView(DetailView):
    model = LabelModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommentFormView(FormView):
    template_name = 'comments/comment.html'
    form_class = ReportCommentForm
    success_url = 'nothing'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        super().form_valid(form)
        return HttpResponseRedirect(form.get_success_url())


class ReportDetailView(DetailView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_obj: Report = context['object']
        tweets = Tweet.objects.filter(search=report_obj.search)

        paginator = Paginator(tweets, 40)
        page_number = self.request.GET.get('page')
        tweets = paginator.get_page(page_number)

        context["search"] = report_obj.search
        context["tweets"] = tweets
        rcf = ReportCommentForm()
        rcf.fields["report"].initial = report_obj.pk
        context['comment_form'] = rcf
        return context


def timeline(request):
    tweet_info_file = settings.STATIC_DIR / "tweet_info.json"
    with open(tweet_info_file, "r") as f:
        headers = json.load(f)
    filter_data = settings.STATIC_DIR / "tweet_filter.yaml"

    saved_filter = request.session.get("saved_filter", {})

    context = {
        'headers': headers,
        'data_url': reverse('timeline'),
        'filter_form': FilterForm(filter_data, saved_filter),
        'comment_form': ReportCommentForm()
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'comments/test_page.html', context=context)


@csrf_exempt
def save_filter(request):
    if request.method == 'POST':
        request.session["saved_filter"] = request.body
        return HttpResponse(request.body)
    return HttpResponse("OK")
