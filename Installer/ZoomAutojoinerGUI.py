import logging
import datetime
logging.basicConfig(filename='logs/%s.log' % (datetime.datetime.now().strftime("%Y%m"
    "%d-%H%M%S")), filemode='w', format=('[%(asctime)s] [%(name)s:%(levelna'
    'me)s] [pid:%(process)d, tid:%(thread)d] %(message)s'), datefmt='%c', 
    level=logging.INFO)
from zoom_autojoiner_gui import main

main()