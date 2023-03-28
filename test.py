import requests, json

def main():
    packet = {
        'user': "test_user",
    }

    session = requests.Session()
    session.headers.update({'Content-type': 'application/json'})
    r = session.post('http://172.29.249.77:49999', data=json.dumps(packet))
    print('packet:', r.json())

if __name__ == "__main__":
    main()