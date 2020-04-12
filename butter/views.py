from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from .forms import ExpenseForm
from django.db import IntegrityError
import json

@login_required
def project_list(request):
	project_list = Project.objects.all()
	return render(request, 'butter/project_list.html', {'project_list': project_list})

def delete(request, project_pk):
	query = Project.objects.get(pk=project_pk)
	query.delete()
	messages.success(request, f'Budget deleted!')
	return redirect('list')  

def homepage(request):
	return render(request, 'butter/homepage.html')

def about(request):
	return render(request, 'butter/about.html')

@login_required
def project_detail(request, project_slug):
	project = get_object_or_404(Project, slug = project_slug)
	
	if request.method == 'GET':
		category_list = Category.objects.filter(project =project)
		return render(request, 'butter/project_detail.html', {'project': project, 'expense_list': project.expenses.all(), 'category_list': category_list})
	elif request.method == 'POST':
		# process the form
		form = ExpenseForm(request.POST)

		if form.is_valid():
			title = form.cleaned_data['title']
			amount = form.cleaned_data['amount']
			category_name = form.cleaned_data['category']

			category = get_object_or_404(Category, project = project, name = category_name)

			Expense.objects.create(
				project = project, 
				title = title,
				amount = amount,
				category = category).save()

	elif request.method == 'DELETE':
		id = json.loads(request.body)['id']
		expense = get_object_or_404(Expense, id = id)
		expense.delete()

		return HttpResponse('')

	return HttpResponseRedirect(project_slug)

class ProjectCreateView(CreateView):
	model = Project
	template_name = 'butter/add_project.html'
	fields = ('month', 'budget')

	def form_valid(self, form):
		try: 
			form.instance.user = self.request.user
			self.object = form.save(commit=False)
			self.object.save()

			categories = self.request.POST['categoriesString'].split(',')
			for category in categories:
				Category.objects.create(
					project=Project.objects.get(id=self.object.id),
					name=category
				).save()

		except IntegrityError as e:
			if 'unique constraint' in e.args[0]:
				messages.error(request, f'You already have a budget for that month.')
				return redirect('add') 

		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return slugify(self.request.POST.get('month'))
