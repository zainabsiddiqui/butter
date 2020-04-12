from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext as _
import uuid


MONTH_YEAR_OPTIONS = (
	("April 2020", "April 2020"),
	("May 2020", "May 2020"),
	("June 2020", "June 2020"),
	("July 2020", "July 2020"),
	("August 2020", "August 2020"),
	("September 2020", "September 2020"),
	("October 2020", "October 2020"),
	("November 2020", "November 2020"),
	("December 2020", "December 2020"),
	("January 2021", "January 2021"),
	("February 2021", "February 2021"),
	("March 2021", "March 2021"),
	)

	
class Project(models.Model):
	month = models.CharField(
		max_length = 20,
		choices = MONTH_YEAR_OPTIONS,
		default = ''
		)
	slug = models.SlugField(max_length = 100, unique = True, blank = True, default = uuid.uuid1)
	budget = models.IntegerField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "project", null = True)


	def save(self, *args, **kwargs):
		self.slug = slugify(self.month)
		super(Project, self).save(*args, **kwargs)

	def budget_left(self):
		expense_list = Expense.objects.filter(project = self)
		total_expense_amount = 0
		for expense in expense_list:
			total_expense_amount += expense.amount

		return self.budget - total_expense_amount

	def total_transactions(self):
		expense_list = Expense.objects.filter(project = self)
		return len(expense_list)


class Category(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE) 
	name = models.CharField(max_length = 50)

class Expense(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = "expenses")
	title = models.CharField(max_length = 100)
	amount = models.DecimalField(max_digits = 8, decimal_places = 2)
	in_or_out = models.CharField(max_length = 20)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	date = models.DateField(_("Date"), default = date.today)

	class Meta:
		ordering = ('-date',)