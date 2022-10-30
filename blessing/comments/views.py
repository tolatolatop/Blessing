import json

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from rest_framework import viewsets

from .form import CommentForm, FilterForm, TimelineCommentForm
from .models import Tweet
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


class CommentFormView(FormView):
    template_name = 'comments/comment.html'
    form_class = CommentForm
    success_url = 'timeline'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        super().form_valid(form)
        return HttpResponseRedirect(self.success_url)


def timeline(request):
    tweet_info_file = settings.STATIC_DIR / "tweet_info.json"
    with open(tweet_info_file, "r") as f:
        headers = json.load(f)
    filter_data = settings.STATIC_DIR / "tweet_filter.yaml"

    saved_filter = request.session.get("saved_filter", {})

    context = {
        'headers': headers,
        'data_url': reverse('timeline'),
        'filter_form': FilterForm(saved_filter),
        'comment_form': TimelineCommentForm()
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
