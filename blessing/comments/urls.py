from django.urls import path, include

from .views import CommentFormView, TimelineView, timeline, save_filter, BranchView
from .common import export_excel

from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'restful', BranchView)

urlpatterns = [
    path('comment', CommentFormView.as_view(), name='comment-form'),
    path('<int:branch_id>/export', export_excel, name='branch-export'),
    path('<int:branch_id>/home', timeline, name='home'),
    path('<int:branch_id>/timeline', TimelineView.as_view({'get': 'list'}), name='timeline'),
    path('save_filter', save_filter, name='save-filter'),
    path('', include(router.urls)),
]
