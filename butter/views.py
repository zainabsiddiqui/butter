from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from .forms import ExpenseForm
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.palettes import YlOrRd6
from bokeh.transform import factor_cmap
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
def analysis(request, project_slug):
	project = get_object_or_404(Project, slug = project_slug)
	expense_list = project.expenses.all()
	# Setting up lists for bokeh bar graphs
	date_list = []
	amounts_list = []
	by_type_list = []

	if request.method == 'GET':
		category_list = Category.objects.filter(project =project)

		# For each outflow expense, add it to our list of dates, list of amounts, and list of categories
		for expense in expense_list:
			if expense.in_or_out == 'Outflow':
				date_list.append(expense.date.strftime("%Y-%m-%d"))
				amounts_list.append(int(expense.amount))
				by_type_list.append(expense.category.name)

		#Bar graph #1, shows expenses by date
		p = figure(x_range=date_list, plot_height=250, title="Amount Spent By Date",
           toolbar_location=None, tools="")
		p.vbar(x=date_list, top=amounts_list, width=0.9, fill_color = 'gold', line_color = 'white')

		p.y_range.start = 0

		# Copying amounts_list so that we don't modify the original so previous graph works properly
		amounts_list_by_category = amounts_list.copy()

		# Grabbing duplicates from list of categories
		result=[idx for idx, item in enumerate(by_type_list) if item in by_type_list[:idx]]

		count = 0

		for duplicate in result:
			if count > 0:
				duplicate -= 1

			# Find the index the duplicate originally appears at
			original_index = by_type_list.index(by_type_list[duplicate])

			# Increment the original category's amount with the duplicate category amounts
			amounts_list_by_category[original_index] += amounts_list_by_category[duplicate]

			# Remove the duplicate from both lists
			by_type_list.pop(duplicate)
			amounts_list_by_category.pop(duplicate)

			count += 1

		# Bar graph 2, orders expenses by category
		source = ColumnDataSource(data=dict(by_type_list=by_type_list, amounts_list_by_category=amounts_list_by_category))

		plot = figure(x_range=by_type_list, plot_height=250, title="Amount Spent By Category",
           toolbar_location=None, tools="")
		plot.vbar(x='by_type_list', top= 'amounts_list_by_category', source = source, legend_field = 'by_type_list', 
			width=0.9, line_color='white', fill_color=factor_cmap('by_type_list', palette=YlOrRd6, factors=by_type_list))

		plot.legend.orientation = "horizontal"
		plot.legend.location = "top_center"
		plot.y_range.start = 0

		plots = [p, plot]

		script, div = components(plots)

		return render(request, 'butter/analysis.html', {'script': script, 'div': div, 'project': project, 'expense_list': expense_list, 'category_list': category_list})

	return HttpResponseRedirect(project_slug)

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
			inf_or_outf = form.cleaned_data['in_or_out']
			category_name = form.cleaned_data['category']
			date_time = form.cleaned_data['date']

			category = get_object_or_404(Category, project = project, name = category_name)

			Expense.objects.create(
				project = project, 
				title = title,
				amount = amount,
				in_or_out = inf_or_outf,
				date = date_time,
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
