from django.urls import path

from .views import LabelDetailView, CommentFormView

urlpatterns = [
    path('label/<int:pk>', LabelDetailView.as_view(), name='labelmodel-detail'),
    path('comment', CommentFormView.as_view(), name='comment-form'),
]
