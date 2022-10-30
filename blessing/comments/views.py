from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from .models import LabelModel, Report, Tweet
from .form import CommentForm, ReportCommentForm
from rest_framework import viewsets
from .restful import TweetSerializer, StandardResultsSetPagination


class TimelineView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = TweetSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Tweet.objects.all()


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
    headers = [
        {
            "field": "id",
            "title": "ID"
        },
        {
            "field": "username",
            "title": "用户名"
        },
        {
            "field": "date",
            "title": "日期"
        },
        {
            "field": "content",
            "title": "内容"
        },
        {
            "field": "likeCount",
            "title": "点赞数"
        }
    ]
    context = {
        'headers': headers,
        'data_url': reverse('timeline')
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'comments/test_page.html', context=context)
