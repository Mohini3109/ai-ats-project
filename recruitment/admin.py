from django.contrib import admin
from .models import Candidate, Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "experience", "created_at")
    search_fields = ("title", "skills_required")

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "job", "match_score", "uploaded_at")
    search_fields = ("name", "email")
    list_filter = ("job",)