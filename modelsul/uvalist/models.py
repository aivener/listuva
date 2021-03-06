from django.db import models

class Student(models.Model):
    email = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    def __str__(self):
    	return self.name

class Category(models.Model):
	title = models.CharField(max_length=100)
	def __str__(self):
		return self.title

class Subcategory(models.Model):
	title = models.CharField(max_length=100)
	category = models.ForeignKey(Category)
	def __str__(self):
		return self.title

class Post(models.Model):
	student = models.ForeignKey(Student)
	title = models.CharField(max_length=100)
	summary = models.CharField(max_length=1000)
	dateTimePosted = models.DateTimeField()
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	#picture
	active = models.BooleanField()
	category = models.ForeignKey(Category)
	subcategory = models.ForeignKey(Subcategory)
	def __str__(self):
		return self.title

class Comment(models.Model):
	student = models.ForeignKey(Student)
	text = models.CharField(max_length=1000)
	dateTimePosted = models.DateTimeField()
	post = models.ForeignKey(Post)
	def __str__(self):
		return self.text

class Authenticator(models.Model):
	user_id	 = models.ForeignKey(Student)
	authenticator = models.CharField(max_length=254, primary_key=True)
	date_created = models.DateTimeField()
	def __str__(self):
		return self.user_id.name


		