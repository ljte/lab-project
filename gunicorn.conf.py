import multiprocessing


# bind = 'localhost:5000'
workers = multiprocessing.cpu_count() * 2 + 1
