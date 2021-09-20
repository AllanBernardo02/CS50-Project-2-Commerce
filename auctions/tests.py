from django.http import response
from django.test import TestCase, Client
from django.urls import reverse 
from .models import *

# Create your tests here.

class ListingTestCase(TestCase):
   

# You'll need to log him in before you can send requests through the client
    
    def setUp(self):   
        #create user
        self.register = {
            'username': "will",
            'email': "",
            'password': "1234",
            'confirmation':"1234"
        }
        self.credentials1 = {
            'username': 'jan',
            'password': 'top_secret'}
        self.credentials2 = {
            'username': 'carlo',
            'password': 'top_secret'}
        self.user1 = User.objects.create_user(
            username='jan', email='', password='top_secret')
        self.user2 = User.objects.create_user(
            username='carlo', email='', password='top_secret')
        
        #create category
        c1 = Category.objects.create(Cat_name = "Shoes")
        c2 =  Category.objects.create(Cat_name = "Accesories")
        c3 =  Category.objects.create(Cat_name = "Bags")
        c4 =  Category.objects.create(Cat_name = "Real Estate")
        c5 =  Category.objects.create(Cat_name = "Technology")
        
        # create bid
        bid1 = Bid.objects.create(user = self.user2, bid = 10.23)
        bid2 = Bid.objects.create(user = self.user2, bid = 99.23)
        
        # create Comment
        com1=  Comment.objects.create(user = self.user2, comment = "Nice item!")
        
        #create Listing
        l1 = Listing.objects.create(title = "Puma Shoes", price =  46, category = c1, user = self.user1)
        l2 = Listing.objects.create(title = "The Best Backpack", price = 21, category = c3, user = self.user1)
        l3 = Listing.objects.create(title = "Aerobook Pro", price =  120, category = c5, user = self.user1)
        
        #adding comments
        l3.comment.add(com1)    
        l3.bid.add(bid1)    
        l3.bid.add(bid2)    
        #create watchlist
        Watchlist.objects.create(user = self.user2 , list = l1)
 
        
          
    #Unit Testing
    
    # modeltests
    def test_listing_count(self):
         a = Listing.objects.all()
         self.assertEqual(a.count(),3)
        
    def test_category_count(self):
        c = Category.objects.all()
        self.assertEqual(c.count(),5)
        
    def test_comments_counts(self):
        c = Comment.objects.all().count()
        self.assertEqual(c,1)
    
    def test_bid_counts(self):
        b = Bid.objects.all().count()
        self.assertEqual(b,2)
    
    def test_watchlist_counts(self):
        w = Watchlist.objects.all().count()
        self.assertEqual(w,1)
    
    def test_is_listing_valid(self):
        list = Listing.objects.get(pk =1)
        self.assertTrue(list.is_listing_valid())
    
    # views Tests
    def test_index(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['listing'].count(),3)
    
    def test_categories(self):
        c = Client()
        response = c.get("/categories")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['category'].count(),5)
        
    def test_login_page(self):
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code,200)
        
    def test_register_page(self):
        c = Client()
        response = c.get("/register")
        self.assertEqual(response.status_code,200)
    
    def test_specific_listing(self):
        self.client.login(**self.credentials2)
        response = self.client.get("/1")
        self.assertEqual(response.status_code,200)    
        self.assertEqual(response.context['list'].title,"Puma Shoes")
        
    def test_registration(self):
        response = self.client.post('/register',data ={**self.register},follow=True,)
        a = User.objects.all()
        self.assertEqual(response.status_code,200)
        self.assertEqual(a.count(),3)
        
    def test_login(self):
        response = self.client.post('/login', self.credentials1, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        
    def test_watchlist(self):
        self.client.login(**self.credentials2)
        response = self.client.get('/watchlist/')
        self.assertEqual(len(response.context['listing']),1)
        self.assertNotEqual(response.context['listing'][0].user,self.credentials2['username'])
        
    def test_comment(self):
        self.client.login(**self.credentials2)
        response = self.client.get('/3')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['list'].comment.all().count(),1)
        
    def test_bid(self):
        self.client.login(**self.credentials2)
        response = self.client.get('/3')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['list'].bid.all().count(),2)
        
        
        
        
        
    