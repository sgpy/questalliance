from assets.CourseApi import find_courses
class Course:
    def __init__(self,tk_pk_id,tk_tags,tk_name,tk_description,language,url,tk_image):
        self.name=tk_name
        self.tags = tk_tags
        self.image=tk_image
        self.description=tk_description
        self.url =url


    def get_card_response(self, platform):
        platform_obj = self.get_supported_pltform(platform)
        return platform_obj.card_response(self)


    def get_supported_pltform(self,platform):
        platform_dct = {
            'TELEGRAM': Telegram(),
            'FACEBOOK': Facebook()
        }

        return platform_dct.get(platform, lambda: InvalidPlatform() )




class Telegram:



    def card_response(self,course):

       return  {
            'card': {
                'buttons': [
                      {
                        'postback': course.url,
                        'text': 'Play'
                      }
                ],
             'imageUri': course.image,
             'title': course.name
      },
      'platform': 'TELEGRAM'
    }


class Facebook:


    def card_response(self):
        print("in facebook")

class InvalidPlatform:

    def __init__(self,course):
        self.course =course

    def card_response(self):
        print("in telegram")




def main():

    bot_response=[]
    #bot_response['fulfillmentMessages']=''
    data = {
        'tags': '#Understanding Self'
    }
    courses = find_courses(data)
    for course in courses.get('data'):
        courseobj = Course(course.get('tk_pk_id'),
                           course.get('tk_tags'),
                           course.get('tk_name'),
                           course.get('tk_description'),
                           course.get('language'),
                           course.get('url'),
                           course.get('tk_image'))
        response = courseobj.get_card_response('TELEGRAM')
        bot_response['fulfillmentMessages'].append(response)


if __name__ == "__main__": main()

    #Course course = Course('My course', '' ,'Enlgi')