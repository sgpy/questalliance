import requests

BASE_URL = 'http://localhost:1234/api/sink/'
FIND_COURSES_URL = BASE_URL + 'find_courses/{}'

class course_api:

	def find_courses (self,tags):
		data = {
			'tags': tags
		}
		req  = requests.post(FIND_COURSES_URL.format('1234'), json=tags)
		return req.json()