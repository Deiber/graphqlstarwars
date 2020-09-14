# **StarWars**

Simple [Django] project that implements APIs under the [GraphQL] technology

## Installation

### Docker libraries

Docker libraries are required before starting the project set up

- [Docker] - Official site
- [Docker-Compose] - Official site

### SetUp
- clone the repo
- navegate to project root and build the image
    ```
    $ docker build . -t starwars
    ```
- up the service
    ```
    $ docker-compose up web
    ```
- browse to your local [graphql-api]

### Tests

- run the command `docker exec <container-hash> python manage.py test`

# Example of Queries

```
 query{
    allPersons{
        id
        name
        filmCharacters{
            edges{
                node{
                    title
                    id
                    director
                    releaseDate
                    openingCrawl
                }
            }
        }
    }
}
```

```
 query{
    person(name:"Person2"){
        id
        name
        homeworld{
            name
        }
        filmCharacters {
            edges {
                node {
                    director
                    id
                    title
                    characters{
                        name
                        id
                    }
                    producers{
                        name
                    }
                }
            }
        }
    }
}
```

# Example of mutations

```
 mutation{
    createPlanet(
        name:"Urano", rotationPeriod:"0d 17h 14m", orbitalPeriod:"0d 17h 14m",
        diameter:"50,724km", climate:"Cold", gravity:"8.87 m/s2",
        surfaceWater:"0", population:"0"
        ){
            planet{
                id name rotationPeriod orbitalPeriod diameter climate gravity 
                surfaceWater population
            }
        }
    }
 ```
```
 mutation{
    createProducer(
            name:"Jorge", age:"28", city:"Bogota", country:"Colombia",
            address: "street false 123", description:"Nothing to write"
        ){
        producer{
            id name age city country address description
        }
    }
}
```
```
 mutation{
    createPerson(
        name:"Joe", height:"1.70m",mass:"73kgs",hairColor:"Black",
        skinColor:"Brown",eyeColor:"Gold",birthYear:"1972", gender:"Male",
        homeworldId:"{planet_id}"
    ){
        person{
            name height mass hairColor skinColor eyeColor birthYear gender
            homeworld{
                id
            }
        }
    }
}
```
```
 mutation{
    createFilm(
        title:"Film of test",episodeId:1, openingCrawl:"xxxx",
        director:"Lisa",releaseDate:"2020-09-13",producers:[],
        characters:[],planets:[]
    ){
        film{
            id
        }
    }
}
```

### Useful links:

 - [GraphQL] - Official site
 - [python-graphene] - Official site
 - [GQL-Auth] - Authentication

 [Django]: <https://www.djangoproject.com/>
 [GQL-Auth]: <https://django-graphql-auth.readthedocs.io/en/latest/>
 [graphql-api]: <http://localhost:8000/graphql/>
 [GraphQL]: <https://graphql.org>
 [python-graphene]: <https://docs.graphene-python.org/en/latest/>
 [Docker]: <https://docs.docker.com/>
 [Docker-Compose]: <https://docs.docker.com/compose/install/>
