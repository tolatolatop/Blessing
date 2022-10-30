from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from .models import LabelModel, Report, Tweet
from .form import CommentForm, ReportCommentForm
from rest_framework import viewsets
from .restful import TweetSerializer


class TimelineView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = TweetSerializer

    def get_queryset(self):
        return Tweet.objects.all().order_by('-date_joined')


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


class TestPageView(FormView):
    template_name = 'comments/test_page.html'
    form_class = ReportCommentForm
    success_url = 'nothing'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        super().form_valid(form)
        return HttpResponseRedirect(form.get_success_url())


def get_timeline(request):
    page_number = request.GET.get("page", 1)
    page_size = int(request.GET.get("page_size", 40))
    tweet_filters = request.session.get("filters", {})

    tweets = Tweet.objects.filter(**tweet_filters)
    paginator = Paginator(tweets, page_size)
    tweets = paginator.get_page(page_number)

    return JsonResponse({"data": tweets})
