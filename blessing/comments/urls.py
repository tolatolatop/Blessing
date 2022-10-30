from django.urls import path

from .views import CommentFormView, TimelineView, timeline, save_filter
from .common import export_excel

urlpatterns = [
    path('comment', CommentFormView.as_view(), name='comment-form'),
    path('report/<int:report_id>/excel', export_excel, name='report-excel'),
    path('home', timeline, name='home'),
    path('timeline', TimelineView.as_view({'get': 'list'}), name='timeline'),
    path('save_filter', save_filter, name='save-filter'),
]
