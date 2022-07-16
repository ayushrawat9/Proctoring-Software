from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('create-test-obj', create_test_objective),
    path('create-test-subj', create_test_subjective),
    path('view-questions', view_question),
    path('view-tests-logs', view_tests_logs),
    path('view-live-tests-logs', view_live_tests_logs),
]
