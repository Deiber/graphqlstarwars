from django.db import models

"""
	too basic models proposal
"""


class Producer(models.Model):

	name = models.CharField(max_length=100)
	age = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Planet(models.Model):

	name = models.CharField(max_length=100)
	rotation_period = models.CharField(max_length=40)
	orbital_period = models.CharField(max_length=40)
	diameter = models.CharField(max_length=40)
	climate = models.CharField(max_length=40)
	gravity = models.CharField(max_length=40)
	surface_water = models.CharField(max_length=40)
	population = models.CharField(max_length=40)

	def __str__(self):
		return self.name


class Person(models.Model):
	""" A person i.e. - Luke Skywalker """

	name = models.CharField(max_length=100)
	height = models.CharField(max_length=10, blank=True)
	mass = models.CharField(max_length=10, blank=True)
	hair_color = models.CharField(max_length=20, blank=True)
	skin_color = models.CharField(max_length=20, blank=True)
	eye_color = models.CharField(max_length=20, blank=True)
	birth_year = models.CharField(max_length=10, blank=True)
	gender = models.CharField(max_length=40, blank=True)
	homeworld = models.ForeignKey(Planet, related_name="residents", on_delete=models.PROTECT)

	def __str__(self):
		return self.name


class Film(models.Model):
	""" A film i.e. The Empire Strikes Back (which is also the best film) """

	title = models.CharField(max_length=100)
	episode_id = models.IntegerField()
	opening_crawl = models.TextField(max_length=1000)
	director = models.CharField(max_length=100)
	release_date = models.DateField()
	producers = models.ManyToManyField(Producer, related_name="film_producers")
	characters = models.ManyToManyField(Person, related_name="film_characters")
	planets = models.ManyToManyField(Planet, related_name="film_planets")

	def __str__(self):
		return self.title
