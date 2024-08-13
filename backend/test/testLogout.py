import requests
import random

url = 'http://127.0.0.1:5000'

def test_logout_bad_request():
    endpoint = url + '/logout-user'
    # Call endpoint
    response = requests.get(endpoint)

    # Perform assertions
    assert response.status_code == 500
    assert response.json()['result'] == 'Failed'
    assert response.json()['message'] == 'Error - You are not logged in'


def main():
    print('** BEGIN TEST')
    print('-> Call /logout-user without logging in first')
    try:
        test_logout_bad_request()
        print('** END TEST')
        print('TEST RESULT: PASSED')
    except:
        print('** END TEST')
        print('TEST RESULT: FAILED')

if __name__ == '__main__':
    main()