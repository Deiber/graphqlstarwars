import base64, re
import graphene
from graphene.relay import Node
from graphql_jwt.decorators import token_auth
from graphene_django.types import DjangoObjectType
from .models import Person, Planet, Producer, Film


class ProducerType(DjangoObjectType):
	class Meta:
		model = Producer
		interfaces = (Node,)


class PersonType(DjangoObjectType):
	class Meta:
		model = Person
		interfaces = (Node,)


class PlanetType(DjangoObjectType):
	class Meta:
		model = Planet
		interfaces = (Node,)


class FilmType(DjangoObjectType):
	producers = graphene.List(ProducerType)
	characters = graphene.List(PersonType)
	planets = graphene.List(PlanetType)

	@graphene.resolve_only_args
	def resolve_producers(self):
		return self.producers.all()

	@graphene.resolve_only_args
	def resolve_characters(self):
		return self.characters.all()

	@graphene.resolve_only_args
	def resolve_planets(self):
		return self.planets.all()

	class Meta:
		model = Film
		interfaces = (Node,)


class CharacterType(DjangoObjectType):
	filmcharacters = graphene.List(FilmType)

	@graphene.resolve_only_args
	def resolve_filmcharacters(self):
		return self.films.all()

	class Meta:
		model = Person
		interfaces = (Node,)


class Query(graphene.ObjectType):
	producer = graphene.Field(ProducerType, name=graphene.String())
	planet = graphene.Field(PlanetType, name=graphene.String())
	person = graphene.Field(CharacterType, name=graphene.String())
	film = graphene.Field(FilmType, title=graphene.String())
	
	all_producers = graphene.List(ProducerType)
	all_planets = graphene.List(PlanetType)
	all_persons = graphene.List(CharacterType)
	all_films = graphene.List(FilmType)

	def resolve_producer(self, info, **kwargs):
		name = kwargs.get("name")
		if name:
			return Producer.objects.get(name=name)
		return None

	def resolve_planet(self, info, **kwargs):
		name = kwargs.get("name")
		if name:
			return Planet.objects.get(name=name)
		return None

	def resolve_person(self, info, **kwargs):
		name = kwargs.get("name")
		if name:
			return Person.objects.get(name=name)
		return None

	def resolve_film(self, info, **kwargs):
		title = kwargs.get("title")
		if title:
			return Film.objects.get(title=title)
		return None

	def resolve_all_producers(self, info, **kwargs):
		return Producer.objects.all()

	def resolve_all_planets(self, info, **kwargs):
		return Planet.objects.all()

	def resolve_all_persons(self, info, **kwargs):
		return Person.objects.all()

	def resolve_all_films(self, info, **kwargs):
		return Film.objects.all()


class CreateProducer(graphene.Mutation):
	producer = graphene.Field(ProducerType)

	class Arguments:
		name = graphene.String()
		age = graphene.String()
		country = graphene.String()
		city = graphene.String()
		address = graphene.String()
		description = graphene.String()

	def mutate(self, info, **kwargs):
		producer = Producer(**kwargs)
		producer.save()
		return CreateProducer(producer=producer)


class CreatePlanet(graphene.Mutation):
	planet = graphene.Field(PlanetType)

	class Arguments:
		"""The list of the fields required for create a planet"""
		name = graphene.String()
		rotation_period = graphene.String()
		orbital_period = graphene.String()
		diameter = graphene.String()
		climate = graphene.String()
		gravity = graphene.String()
		surface_water = graphene.String()
		population = graphene.String()

	def mutate(self, info, **kwargs):
		planet = Planet(**kwargs)
		planet.save()
		return CreatePlanet(planet=planet)


class CreatePerson(graphene.Mutation):
	person = graphene.Field(PersonType)

	class Arguments:
		"""The list of the fields required for create a person"""
		name = graphene.String()
		height = graphene.String()
		mass = graphene.String()
		hair_color = graphene.String()
		skin_color = graphene.String()
		eye_color = graphene.String()
		birth_year = graphene.String()
		gender = graphene.String()
		homeworld_id = graphene.String()

	@token_auth
	def mutate(self, info, **kwargs):
		data = dict(filter(lambda x: x[0] != "homeworld_id", kwargs.items()))
		data["homeworld_id"] = _get_id(kwargs.get("homeworld_id"))
		person = Person(**data)
		person.save()
		return CreatePerson(person=person)


class CreateFilm(graphene.Mutation):
	film = graphene.Field(FilmType)

	class Arguments:
		"""The list of the fields required for create a film"""
		title = graphene.String()
		episode_id = graphene.Int()
		opening_crawl = graphene.String()
		director = graphene.String()
		release_date = graphene.Date()
		producers = graphene.List(graphene.String)
		characters = graphene.List(graphene.String)
		planets = graphene.List(graphene.String)

	@token_auth
	def mutate(self, info, **kwargs):
		"""
		The interface relay.Node returns a encoded string as the id field that 
		contains the type class name and the real id of its related record 
		(FilmType:1), therefore, the real id needs be taken from it
		 """
		many_to_many_fields = ["producers","characters","planets"]
		data = dict(
			filter(lambda x: x[0] not in many_to_many_fields, kwargs.items())
		)
		film = Film(**data)
		film.save()
		set_many_to_many(film, film.producers.add, kwargs.get("producers",[]), Producer)
		set_many_to_many(film, film.characters.add, kwargs.get("characters",[]), Person)
		set_many_to_many(film, film.planets.add, kwargs.get("planets",[]), Planet)

		return CreateFilm(film=film)


class Mutations(graphene.ObjectType):
	create_producer = CreateProducer.Field()
	create_planet = CreatePlanet.Field()
	create_person = CreatePerson.Field()
	create_film = CreateFilm.Field()


def set_many_to_many(instance, method, ids, related_model):
	"""
	helper method that sets records for many to many relationships

	:param instance: the target instance
	:type instance: a record's instance
	:param method: the name of the field that has the M2M relationship
	:type method: py:class:method, i.e: `intance.field.add`
	:param ids: the list of relay.node ids
	:type ids: py:class:list
	:param related_model: the field related model
	:type related_model: py:class:str
	"""

	if all([instance, method, ids, related_model]):
		ids = [_get_id(_id) for _id in ids]
		qs = related_model.objects.filter(id__in=ids)
		if qs:
			for rc in qs:
				method(rc)


def _get_id(_id):
	"""
	helper method that returns the real id of a record from given node's id
	:param _id: the id to decode
	:type _id: py:class:str or py:class:bytes
	return str
	"""
	if not isinstance(_id, (str,bytes)):
		_id = bytes(_id.encode("utf-8"))

	_id = base64.b64decode(_id).decode()
	return "".join(re.findall(r"\d+",_id))
