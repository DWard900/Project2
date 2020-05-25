from datetime import datetime, timedelta
import unittest, os
from app import app, db
from app.models import User, Exercise
from flask_login import current_user, login_user, logout_user, login_required

class UserModelTest(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        # Create virtual environment for test
        self.app = app.test_client()
        db.create_all()
        user = User(username = "Bob", email="bob@gmail.com", is_coach=True, is_admin=True)
        user.set_password("pw")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Register helper function
    def register(self, username, email, password, password2):
        return self.app.post(
            '/register', data=dict(username=username, email=email, password=password, 
            password2=password2), follow_redirects=True
        )

    # Login helper function
    def login(self, username, password):
        return self.app.post(
            '/login', data=dict(username=username, password=password), follow_redirects=True
        )

    # Test user registration
    def test_user_registration(self):
        response = self.register("Test", "test@email.com", "pw", "pw")
        self.assertIn(b"Congratulations, you are now a registered user!", response.data)

    # Test errors thrown with incorrect user registration
    def test_incorrect_user_registration(self):
        # Username that already exists
        response = self.register("Bob", "bill@gmail.com", "pw", "pw")
        self.assertIn(b'Please use a different username.', response.data)
        
        # Email address that already exists
        response2 = self.register("Bill", "bob@gmail.com", "pw", "pw")
        self.assertIn(b'Please use a different email address.', response2.data)

    # Test login page loads correctly
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertIn(b'Sign in below to access the app', response.data)

    # Test user login with correct credentials
    def test_login(self):
        with self.app:
            response = self.login("Bob", "pw")
            self.assertIn(b'Welcome to FitTrack App, Bob!', response.data)
            self.assertTrue(current_user.username == "Bob")
            self.assertFalse(current_user.username == "Wrong" )
    
    # Test user login with incorrect credentials
    def test_invalid_login(self):
        with self.app:
            response = self.login("Wrong", "wrongpw")
            self.assertIn(b"Invalid username or password", response.data)

    # Test that logging out works
    def test_logout(self):
        with self.app:
            self.login("Bob", "pw")
            response = self.app.get('/logout', follow_redirects=True)
            self.assertFalse(current_user.is_authenticated)

    # Test user page loads
    def test_user_page(self):
        with self.app:
            self.login("Bob", "pw")
            response = self.app.get('/user/Bob', follow_redirects=True)
            self.assertIn(b"Welcome to your profile page, Bob", response.data)
            self.assertIn(b"Your exercise data", response.data)

    # Test password hashing and check password functionality
    def test_password_hashing(self):
        u = User(username = "Test")
        u.set_password("test")
        self.assertFalse(u.check_password('case'))
        self.assertTrue(u.check_password('test'))

    # Test avatar
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    # Test follow functionality
    def test_follow(self):
        u1 = User(username='elise', email='elise@example.com')
        u2 = User(username='dan', email='dan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'dan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'elise')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    # Test follow exercise posts functionality
    def test_follow_posts(self):
        # create four users
        u1 = User(username='elise', email='elise@example.com')
        u2 = User(username='dan', email='dan@example.com')
        u3 = User(username='sarah', email='sarah@example.com')
        u4 = User(username='james', email='james@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four exercise posts
        now = datetime.utcnow()
        e1 = Exercise(style="run", time="5", distance="1", user=u1, timestamp=now + timedelta(seconds=1))
        e2 = Exercise(style="walk", time="50", distance="4", user=u2, timestamp=now + timedelta(seconds=4))
        e3 = Exercise(style="swim", time="30", distance="2", user=u3, timestamp=now + timedelta(seconds=3))
        e4 = Exercise(style="run", time="17", distance="5", user=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([e1, e2, e3, e4])
        db.session.commit()

        # set up the followers
        u1.follow(u2) # elise follows dan
        u1.follow(u4) # elise follows james
        u2.follow(u3) # dan follows sarah
        u3.follow(u4) # sarah follows james 
        db.session.commit()

        # check the followed exercise posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [e2, e4, e1])
        self.assertEqual(f2, [e2, e3])
        self.assertEqual(f3, [e3, e4])
        self.assertEqual(f4, [e4])

    # Test edit profile functionality
    def test_edit_profile(self):
        with self.app:
            self.login("Bob", "pw")
            response = self.app.post('/edit_profile', data=dict(username="Bob", about_me="All about Bob"), follow_redirects=True)
            self.assertIn(b"Your changes have been saved", response.data)
            self.assertIn(b"All about Bob", response.data)

    # Test set goal functionality
    def test_set_goal(self):
        with self.app:
            self.login("Bob", "pw")
            # Check coach user can see "Change Goal" button on profile
            response = self.app.get('/user/Bob', follow_redirects=True)
            self.assertIn(b"Change Goal", response.data)
            # Check user can change own goal
            response = self.app.post('/set_goal/Bob', data=dict(username="Bob", goals="This is a test goal"), follow_redirects=True)
            self.assertIn(b"Your changes have been saved", response.data)
            # Check goal appears on user page
            response = self.app.get('/user/Bob', follow_redirects=True)
            self.assertIn(b"This is a test goal", response.data)

        # Check user can change another person's goals
        u1 = User(username='elise', email='elise@example.com')
        db.session.add(u1)
        db.session.commit()
        with self.app:
            response = self.app.get('/user/elise', follow_redirects=True)
            self.assertIn(b"Change Goal", response.data)
            response = self.app.post('/set_goal/elise', data=dict(username="elise", goals="This is another test goal"), follow_redirects=True)
            self.assertIn(b"Your changes have been saved", response.data)
            # Check goal appears on user page
            response = self.app.get('/user/elise', follow_redirects=True)
            self.assertIn(b"This is another test goal", response.data)

    # Test messages functionality
    def test_messages(self):
        with self.app:
            self.login("Bob", "pw")
            # Test Messages page loads
            response = self.app.get('/messages/Bob', follow_redirects=True)
            self.assertIn(b"Messages", response.data)

        # Test send message functionality
        u1 = User(username='elise', email='elise@example.com')
        u1.set_password("password")
        db.session.add(u1)
        db.session.commit()
        with self.app:
            response = self.app.get('/user/elise', follow_redirects=True)
            response = self.app.post('/send_message/elise', data=dict(username="elise", message="Message from Bob to Elise"), follow_redirects=True)
            self.assertIn(b"Your message has been sent", response.data)

        # Test messages received
        with self.app:
            self.login("elise", "password")
            response = self.app.get('/messages/elise', follow_redirects=True)
            self.assertIn(b"Message from Bob to Elise", response.data)
            # Test delete messages
            response = self.app.post('/delete_message/1', follow_redirects=True)
            self.assertNotIn(b"Message from Bob to Elise", response.data)

    # Test admin login
    def test_admin(self):
        # User is admin
        with self.app:
            self.login("Bob", "pw")
            response = self.app.post('/admin_login', data=dict(username="Bob", password="pw"), 
            follow_redirects=True)
            self.assertIn(b"Administrator view", response.data)

        # If user is not admin
        u1 = User(username='elise', email='elise@example.com')
        u1.set_password("password")
        db.session.add(u1)
        db.session.commit()
        with self.app:
            self.login("elise", "password")
            response = self.app.post('/admin_login', data=dict(username="elise", password="password"), 
            follow_redirects=True)
            self.assertIn(b"Not an admin user", response.data)
            self.assertNotIn(b"Administrator view", response.data)


if __name__=='__main__':
    unittest.main(verbosity=2)


