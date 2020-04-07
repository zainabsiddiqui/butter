from django.db import models
from django.utils.text import slugify

class Project(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, unique = True, blank = True)
	budget = models.IntegerField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Project, self).save(*args, **kwargs)

class Category(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE) 
	name = models.CharField(max_length = 50)

class Expense(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = "expenses")
	title = models.CharField(max_length = 100)
	amount = models.DecimalField(max_digits = 8, decimal_places = 2)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)