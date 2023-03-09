# in loop:
## user: duke_drone_1, duke_drone_2
## frame: cv_mat
results = request_service('https://mscv.yale.edu/api', user, 'stream', ['slam'], time.time(), frame)

# end usage
results = request_service('https://mscv.yale.edu/api', user, 'stop', ['slam'], time.time(), None)