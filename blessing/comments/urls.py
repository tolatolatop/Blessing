from django.urls import path

from .views import CommentFormView, TimelineView, timeline, save_filter
from .common import export_excel

urlpatterns = [
    path('comment', CommentFormView.as_view(), name='comment-form'),
    path('<int:branch_id>/excel', export_excel, name='branch-excel'),
    path('<int:branch_id>/home', timeline, name='home'),
    path('<int:branch_id>/timeline', TimelineView.as_view({'get': 'list'}), name='timeline'),
    path('save_filter', save_filter, name='save-filter'),
]
