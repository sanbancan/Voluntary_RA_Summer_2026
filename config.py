import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20240620")
DATA_PATH = "data/dssg_21_projects.json"
OUTPUT_DIR = "outputs"
MOCK_MODE = os.getenv("MOCK_MODE", "1") == "1"
