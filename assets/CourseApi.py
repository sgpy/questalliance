import requests

BASE_URL = 'http://localhost:1234/api/sink/'
FIND_COURSES_URL = BASE_URL + 'find_courses/{}'



def find_courses (query):
	req  = requests.post(FIND_COURSES_URL.format('1234'), json=query)
	return req.json()