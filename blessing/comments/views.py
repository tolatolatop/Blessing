from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from .models import LabelModel
from .form import CommentForm


class LabelDetailView(DetailView):
    model = LabelModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommentFormView(FormView):
    template_name = '/comments/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_comment()
        return super().form_valid(form)
