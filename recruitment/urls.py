from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ⭐ ADD THIS
    path('upload/', views.upload_resume, name='upload-resume'),
    path('success/', views.resume_success, name='resume-success'),
    path('ranking/', views.candidate_ranking, name='candidate-ranking'),
    path('add-job/', views.add_job, name='add-job'),
    path('shortlist/<int:candidate_id>/', views.toggle_shortlist, name='toggle-shortlist'),
]