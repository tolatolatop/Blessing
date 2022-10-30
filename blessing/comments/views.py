import json
import pathlib

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.http import Http404
from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .form import CommentForm, FilterForm, TimelineCommentForm
from .models import LogData, Branch
from .restful import LogDataSerializer, StandardResultsSetPagination, BranchSerializer


class TimelineView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = LogDataSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        branch_id = self.kwargs["branch_id"]
        branch = Branch.objects.get(pk=branch_id)
        saved_filter = self.request.session.get("saved_filter", {})
        return LogData.objects.filter(branch=branch, **saved_filter)


class BranchView(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CommentFormView(FormView):
    template_name = 'comments/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        super().form_valid(form)
        success_url = reverse("comment-form")
        return HttpResponseRedirect(success_url)


def timeline(request, branch_id):
    log_data_path = settings.STATIC_DIR / "log_data_info.json"
    with open(log_data_path, "r") as f:
        headers = json.load(f)

    saved_filter = request.session.get("saved_filter", {})
    data_url = reverse('timeline', kwargs={"branch_id": branch_id})
    filter_form = FilterForm(saved_filter)
    timeline_comment_form = TimelineCommentForm()
    export_url = reverse('branch-export', kwargs={"branch_id": branch_id})

    context = {
        'headers': headers,
        'data_url': data_url,
        'filter_form': filter_form,
        'comment_form': timeline_comment_form,
        'export_url': export_url
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'comments/index.html', context=context)


@csrf_exempt
def save_filter(request):
    HttpResponse("Got json data")
    if request.method == 'POST':
        data = request.body
        request.session["saved_filter"] = json.loads(data)
        return HttpResponse(request.body)
    return HttpResponseServerError("Malformed data!")
