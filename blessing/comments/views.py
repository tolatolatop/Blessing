from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from .models import LabelModel, Report, Tweet
from .form import CommentForm


class LabelDetailView(DetailView):
    model = LabelModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommentFormView(FormView):
    template_name = 'comments/comment.html'
    form_class = CommentForm
    success_url = '/success/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        return super().form_valid(form)


class ReportDetailView(DetailView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_obj: Report = context['object']
        tweets = Tweet.objects.filter(search=report_obj.search)
        context["tweets"] = tweets
        context['comment_form'] = CommentForm
        return context
