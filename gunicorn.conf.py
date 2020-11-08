import multiprocessing
import os


bind = os.environ.get('URL', 'localhost:5000')
workers = multiprocessing.cpu_count() * 2 + 1
