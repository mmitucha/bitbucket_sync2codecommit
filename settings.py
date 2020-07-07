import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SUBPROCESS_TIMEOUT = 60

# dynamic values
if os.getenv("REPOS_DIR"):
    REPOS_DIR = os.getenv("REPOS_DIR")
else:
    REPOS_DIR = os.path.join(BASE_DIR, "_repos")

