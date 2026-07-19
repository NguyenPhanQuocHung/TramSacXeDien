# Configuration for TramSacXeDien Web App

# Flask Configuration
DEBUG = True
SECRET_KEY = 'your-secret-key-here-change-in-production'
HOST = '127.0.0.1'
PORT = 5000

# Algorithm Configuration
DEFAULT_NUM_AREAS = 30
DEFAULT_K_STATIONS = 5
DEFAULT_NUM_RESTARTS = 100

# Simulated Annealing Configuration
SA_T_INIT = 10000
SA_COOLING = 0.997
SA_MAX_STEPS = 15000

# Optimization Parameters
MIN_AREAS = 10
MAX_AREAS = 100
MIN_STATIONS = 1
MAX_STATIONS = 20
