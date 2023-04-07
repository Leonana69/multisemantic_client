import time
from utils import request_service

def main():
    data = {
        'model_info': {
            'name': 'human-pose',
            'url': 'https://tfhub.dev/google/movenet/singlepose/thunder/4?tf-hub-format=compressed'
        }
    }
    response = request_service('https://mscv.yale.edu/api', 'guojun', 'deploy', [], time.time(), data)
    print(response)

if __name__ == "__main__":
    main()