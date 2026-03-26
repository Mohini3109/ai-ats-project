from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField(help_text="Comma-separated skills (e.g. Python, SQL, React)")
    experience = models.CharField(max_length=100, help_text="e.g. 2+ years")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='candidates', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    resume = models.FileField(upload_to="resumes/")
    skills = models.TextField(blank=True, help_text="Automatically extracted skills")
    match_score = models.FloatField(default=0.0, help_text="Skill match percentage with job posting")
    is_shortlisted = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

