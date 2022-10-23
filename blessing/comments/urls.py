from django.urls import path

from .views import LabelDetailView, CommentFormView, ReportDetailView
from .common import export_excel

urlpatterns = [
    path('label/<int:pk>', LabelDetailView.as_view(), name='labelmodel-detail'),
    path('comment', CommentFormView.as_view(), name='comment-form'),
    path('report/<int:pk>', ReportDetailView.as_view(), name='report-detail'),
    path('report/<int:report_id>/excel', export_excel, name='report-excel'),
]
