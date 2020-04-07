from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list(request):
	return render(request, 'butter/project_list.html')

def project_detail(request, project_slug):
	project = get_object_or_404(Project, slug = project_slug)
	expense_list = project.expenses
	return render(request, 'butter/project_detail.html', {'project': project, 'expense_list': project.expenses.all()})

