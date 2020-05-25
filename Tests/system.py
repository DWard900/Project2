import unittest, os, time
from app import app, db
from app.models import User, Exercise
from selenium import webdriver
from flask_login import current_user, login_user, logout_user, login_required

class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'chromedriver'))
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            db.init_app(app)
            db.create_all()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()
    
    # Login helper function
    def login(self, username, password):
        self.driver.get('http://localhost:5000/')
        self.driver.implicitly_wait(5)
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')
        user_field.send_keys(username)
        password_field.send_keys(password)
        time.sleep(1)
        submit.click()

    # Test user login
    def test_login(self):
        self.login("admin", "pw")

        # Check login success
        time.sleep(1)
        self.driver.implicitly_wait(5)
        greeting = self.driver.find_element_by_id('greeting').get_attribute('innerHTML')
        self.assertEqual(greeting, "Welcome to FitTrack App, admin!")

    # Test quiz submission
    def test_quiz(self):
        self.login("admin", "pw")
        self.driver.implicitly_wait(5)
        self.driver.get('http://localhost:5000/quiz')
        style = self.driver.find_element_by_id('style')
        distance = self.driver.find_element_by_id('distance')
        time = self.driver.find_element_by_id('time')
        date = self.driver.find_element_by_id('date')
        rating = self.driver.find_element_by_id('rate_exercise')
        comment = self.driver.find_element_by_id('exercise_comments')
        submit = self.driver.find_element_by_id('submit')
        style.send_keys("Walk")
        distance.send_keys("5")
        time.send_keys("60")
        date.send_keys("27/05/2020")
        rating.send_keys("8")
        comment.send_keys("Test comment")
        submit.click()

        # Check quiz success
        self.driver.implicitly_wait(5)
        results = self.driver.find_element_by_id('quiz-test').get_attribute('innerHTML')
        self.assertEqual(results, "Thank you for posting your exercise!")

    # Test user is coach
    def test_coach(self):
        self.login("admin", "pw")
        self.driver.implicitly_wait(5)
        self.driver.get('http://localhost:5000/user/pw')
        coach = self.driver.find_element_by_id('Coachtest').get_attribute('innerHTML')
        self.assertEqual(coach, "You are a Coach")

    # Test admin login works
    def test_admin(self):
        self.login("admin", "pw")
        self.driver.implicitly_wait(5)
        self.driver.get('http://localhost:5000/admin_login')
        self.driver.implicitly_wait(5)
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')
        user_field.send_keys("admin")
        password_field.send_keys("pw")
        submit.click()

        # Test admin login works
        self.driver.implicitly_wait(5)
        greeting = self.driver.find_element_by_id('Admintest').get_attribute('innerHTML')
        self.assertEqual(greeting, "Administrator view")


if __name__=='__main__':
    unittest.main(verbosity=2)