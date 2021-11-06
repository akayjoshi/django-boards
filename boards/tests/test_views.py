from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from boards.views import home, board_topics, new_topic
from boards.models import Board,Topic,Post
from boards.forms import NewTopicForm
# Create your tests here.
class HomeTests(TestCase):

    def setUp(self):

         # we need a Board instance for not access this board form db again we save it here.
         #  also can remove url and reponse here to use for other tests.

        self.board = Board.objects.create(name = 'django', description = 'for testing reverse urls.')
        url= reverse('home')
        self.response = self.client.get(url)


    def test_home_view_status_code(self):
        
        # return reponse
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):


        #  use resolve to check `/` pattern is returning the home view.

        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_links_to_topics_page(self):

        # make a reverse url for board topics
        board_topics_url = reverse('board_topics',kwargs={'id':self.board.id})

        #check reponse contains a link to board topics
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))




class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description = 'django test')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics',kwargs={'id':1})
        response  = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_statue_code(self):
        url = reverse('board_topics',kwargs={'id':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolve_boards_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'id':1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'id': 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))



class NewTopicTests(TestCase):
    
    def setUp(self):
        Board.objects.create(name='Django', description='This is used as virtual db') #Two way, can store here in self also.
        User.objects.create_user(username='john',email='jhon@gmail.com', password='123456') # create_user do password hashing for auth

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_fount_status_code(self):
        url = reverse('new_topic', kwargs={'id':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        

    def test_new_topic_url_resolve_new_topic_view(self):
        url = reverse('new_topic',kwargs= {'id': 99})
        view = resolve(url)
        self.assertEquals(view.func, new_topic)

    
    def test_new_topic_view_contains_links_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'id': 1})
        board_topics_url = reverse('board_topics',kwargs={'id': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    
    # testing the form view
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddleware')
    def test_new_topic_valid_test_date(self):
        url = reverse('new_topic', kwargs={'id': 1})
        data = {
            'subject': 'this is subject',
            'message': 'this is a message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists()) # agr post request gyi h to virtually instance bhi bna hoga
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'id':1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200) # if saved redirect status code 302
    
    def test_new_topic_invalid_post_date_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'id': 1})
        data = {
            'subject': '',
            'message':''
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        self.assertTrue(form.errors)

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'id': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)












