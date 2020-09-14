from django.test import TestCase
from graphene.test import Client
from starwars.schema import schema
import re


class CommonTestCase(TestCase):
	fixtures = ["test_data.json"]
	def setUp(self):
		self.client = Client(schema)

class QueryTestCase(CommonTestCase):
	def setUp(self):
		super().setUp()

	def test_query_planets(self):
		# creating and executing query allPlanets
		query = """
			{
				allPlanets { id name }
			}
		"""
		payload = self.client.execute(query)
		# checking payload
		self.assertTrue(isinstance(payload["data"], dict))
		self.assertTrue(payload["data"]["allPlanets"])
		planets = payload["data"]["allPlanets"]
		self.assertTrue(isinstance(payload["data"]["allPlanets"], list))
		# checking planets quantity
		self.assertEqual(len(planets), 3)

	def test_query_producers(self):
		# creating and executing query allProducers
		query = """
			{
				allProducers { id name }
			}
		"""
		payload = self.client.execute(query)
		# checking payload
		self.assertTrue(isinstance(payload["data"],dict))
		self.assertTrue(payload["data"]["allProducers"])
		producers = payload["data"]["allProducers"]
		self.assertTrue(isinstance(payload["data"]["allProducers"], list))
		# checking producers quantity
		self.assertEqual(len(producers), 2)

	def test_query_people(self):
		# creating and executing query allPersons
		query = """
			{
				allPersons{
					id
					name
					filmCharacters{
						edges{
							node{
								title
								id
							}
						}
					}
				}
			}
		"""
		payload = self.client.execute(query)
		# checking payload
		self.assertTrue(isinstance(payload["data"], dict))
		self.assertTrue(payload["data"]["allPersons"])
		persons = payload["data"]["allPersons"]
		self.assertTrue(isinstance(payload["data"]["allPersons"], list))
		# checking people quantity
		self.assertEqual(len(persons), 2)

	def test_query_films(self):
		# creating and executing query allFilms
		query = """
			{
				allFilms{
					id 
					title
					director
					characters{
						id name
					}
					producers{
						id name
					}
					planets{
						id name
					}
				}
			}
		"""
		payload = self.client.execute(query)
		# checking payload
		self.assertTrue(isinstance(payload["data"], dict))
		self.assertTrue(payload["data"]["allFilms"])
		films = payload["data"]["allFilms"]
		self.assertTrue(isinstance(payload["data"]["allFilms"], list))
		# checking films quantity
		self.assertEqual(len(films), 3)


class MutationTestCase(CommonTestCase):
	def setUp(self):
		super().setUp()

	def query_obj_return_id(self, query_name, filter_value=None):
		if filter_value:
			query = """
				query{
					%s (name:"%s"){
						id
					}
				}
			""" % (query_name,filter_value)
		else:
			query = """
				query{
					%s{
						id
					}
				}
			""" % (query_name)
		payload = self.client.execute(query)
		if filter_value:
			_id = payload["data"][query_name]["id"]
		else:
			objs = payload["data"][query_name]
			_id = [rec["id"] for rec in objs]
		return _id

	def test_create_planet_mutation(self):
		# testing the createPlanet mutation
		mutation = """
			mutation{
				createPlanet(
					name:"Uranus", rotationPeriod:"0d 17h 14m", orbitalPeriod:"0d 17h 14m",
					diameter:"50,724km", climate:"Cold", gravity:"8.87 m/s2",
					surfaceWater:"0", population:"0"
				){
					planet{
						id name rotationPeriod orbitalPeriod diameter climate gravity 
						surfaceWater population
					}
				}
			}
		"""
		payload = self.client.execute(mutation)
		# checking payload
		self.assertTrue(isinstance(payload["data"]["createPlanet"]["planet"], dict))
		planet = payload["data"]["createPlanet"]["planet"]
		# checking if the saved name matches to given
		self.assertEqual(planet["name"], "Uranus")

	def test_create_producer_mutation(self):
		# testing the createProducer mutation
		mutation = """
			mutation{
				createProducer(
					name:"Joe", age:"28", city:"Bogota", country:"Colombia",
					address: "street false 123", description:"Nothing to write"
				){
					producer{
						id name age city country address description
					}
				}
			}
		"""
		payload = self.client.execute(mutation)
		# checking payload
		self.assertTrue(isinstance(payload["data"]["createProducer"]["producer"], dict))
		producer = payload["data"]["createProducer"]["producer"]
		# checking if the saved name matches to given
		self.assertEqual(producer["name"], "Joe")

	def test_create_person_mutation(self):
		# testing the createPerson mutation
		mutation = 'mutation{ createPerson ( name:"Jorge", height:"1.70m", '
		mutation += 'mass:"73kgs", hairColor:"Black", skinColor:"Brown", '
		mutation += 'eyeColor:"Gold",birthYear:"1972", gender:"Male",'
		mutation += 'homeworldId:"{planet_id}"'.format(
			planet_id=self.query_obj_return_id("planet","Earth"))
		mutation += '){ person { name height mass hairColor skinColor eyeColor'
		mutation += ' birthYear gender homeworld{ id } } } }'
		payload = self.client.execute(mutation)
		
		# checking payload
		self.assertTrue(isinstance(payload["data"]["createPerson"]["person"], dict))
		person = payload["data"]["createPerson"]["person"]
		# checking if the saved name matches to given
		self.assertEqual(person["name"], "Jorge")

	def test_create_film_mutation(self):
		# testing the createFilm mutation
		producers = self.query_obj_return_id("allProducers")
		characters = self.query_obj_return_id("allPersons")
		planets = self.query_obj_return_id("allPlanets")
		mutation = 'mutation{ createFilm ( title:"Film of test", episodeId:1,'
		mutation += ' openingCrawl:"xxxx", director:"Lisa", releaseDate:"2020-09-13"'
		mutation += f' ,producers:{producers}, characters:{characters}, planets:{planets}'
		mutation += '){ '+ 'film{ id title } } }'
		mutation = mutation.replace("'", '"')
		payload = self.client.execute(mutation)
		# checking payload
		self.assertTrue(isinstance(payload["data"]["createFilm"]["film"], dict))
		film = payload["data"]["createFilm"]["film"]
		# checking if the saved name matches to given
		self.assertEqual(film["title"], "Film of test")
		self.assertFalse(isinstance(film["id"], int))
