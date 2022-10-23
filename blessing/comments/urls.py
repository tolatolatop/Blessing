from django.urls import path

from .views import LabelDetailView

urlpatterns = [
    path('label/<int:pk>', LabelDetailView.as_view(), name='labelmodel-detail'),
]
