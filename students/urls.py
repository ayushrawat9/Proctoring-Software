from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('test-login', test_login),
    path('give-test-objective', give_test_objective,name = "give-test-objective"),
    # path('video_stream', video_stream,name = "video_stream"),
    path('test-result', test_result,name = "test-result"),
    path('save-proctor-log-to-media', save_proctor_log),
]
