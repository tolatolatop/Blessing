from django.utils import timezone
from django.views.generic.detail import DetailView

from .models import LabelModel


class LabelDetailView(DetailView):
    model = LabelModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
