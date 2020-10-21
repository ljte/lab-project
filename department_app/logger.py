"""main logger"""

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(message)s')

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
# logger.addHandler(stream_handler)
