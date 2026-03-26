from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CandidateForm, JobForm
from .models import Candidate, Job
from .utils import extract_resume_text, extract_skills_from_text, calculate_tfidf_match_score
from django.shortcuts import get_object_or_404, redirect
from .models import Candidate

def upload_resume(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES) # request.FILES is required for file uploads
        if form.is_valid():
            candidate = form.save()
            
            # Extract raw text from the uploaded resume
            resume_text = extract_resume_text(candidate.resume.path)
            
            if resume_text:
                candidate.skills = extract_skills_from_text(resume_text)
                
            # Calculate match score if applied to a job
            if candidate.job:
                job_document = f"{candidate.job.title} {candidate.job.description} {candidate.job.skills_required}"
                candidate.match_score = calculate_tfidf_match_score(resume_text, job_document)
                
            candidate.save()
            
            messages.success(request, f"Your resume has been uploaded! AI Match Score: {candidate.match_score}%")
            return redirect('resume-success')
    else:
        form = CandidateForm()
    
    return render(request, 'recruitment/upload_resume.html', {'form': form})

def resume_success(request):
    return render(request, 'recruitment/success.html')

@login_required
def candidate_ranking(request):
    job_id = request.GET.get('job_id')
    jobs = Job.objects.all()
    
    if job_id:
        candidates = Candidate.objects.filter(job_id=job_id).order_by('-match_score')
        selected_job = Job.objects.filter(id=job_id).first()
    else:
        candidates = Candidate.objects.all().order_by('-match_score')
        selected_job = None
        
    return render(request, 'recruitment/candidate_ranking.html', {
        'candidates': candidates,
        'jobs': jobs,
        'selected_job': selected_job
    })

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, f"New job posting '{job.title}' created successfully!")
            return redirect('candidate-ranking')
    else:
        form = JobForm()
    
    return render(request, 'recruitment/add_job.html', {'form': form})

@login_required
def toggle_shortlist(request, candidate_id):
    if request.method == 'POST':
        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.is_shortlisted = not candidate.is_shortlisted
        candidate.save(update_fields=['is_shortlisted'])
        
        status = "shortlisted" if candidate.is_shortlisted else "removed from shortlist"
        messages.success(request, f"{candidate.name} has been {status}.")
        
    return redirect('candidate-ranking')

def home(request):
    return render(request, 'home.html')

# from django.contrib.auth.models import User

# def create_admin(request):
#     if not User.objects.filter(username="admin").exists():
#         User.objects.create_superuser("admin", "admin@gmail.com", "admin123")
#     return HttpResponse("Admin created")