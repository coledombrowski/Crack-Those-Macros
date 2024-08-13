import requests
import random

url = 'http://127.0.0.1:5000'

# Call /register-account
def get_register_account():
    endpoint = url + '/register-account'
    random_number = random.random()
    test_user = 'test' + str(random_number)
    obj = {
        "username": test_user,
        "password": test_user
    }

    # Call endpoint
    response = requests.post(endpoint, json = obj)

    if response.status_code == 200:
        return test_user
    else: 
        return False
    
# Call /login-user and assert method integration functionality
def test_user_by_login(test_user):
    endpoint = url + '/login-user'
    obj = {
        "username": test_user,
        "password": test_user
    }

    # Call endpoint
    response = requests.post(endpoint, json = obj)

    # Perform assertions
    assert response.status_code == 200
    assert response.json()['username'] == test_user

def main():
    print('Begin Test:')
    print('-> Create an account with a random test username')
    test_user = get_register_account()

    if(test_user):
        print(f'User {test_user} was created successfully')
        print('-> Test login')
        test_user_by_login(test_user)
        print(f'User {test_user} was logged in successfully')
        print('End test')
        print('TEST RESULT: PASSED')
    else:
        print('End test')
        print('TEST RESULT: FAILED')

if __name__ == '__main__':
    main()