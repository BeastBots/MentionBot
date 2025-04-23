import importlib.util
import os

# Try to import config.py if it exists
config = None
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py')
if os.path.exists(config_path):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

BOT_TOKEN = getattr(config, 'BOT_TOKEN', None) or os.environ.get("BOT_TOKEN")
MONGODB_URI = getattr(config, 'MONGODB_URI', None) or os.environ.get("MONGODB_URI")
OWNER_ID = getattr(config, 'OWNER_ID', None) or int(os.environ.get("OWNER_ID", "0"))
UPSTREAM_REPO = getattr(config, 'UPSTREAM_REPO', None) or os.environ.get("UPSTREAM_REPO")
UPSTREAM_BRANCH = getattr(config, 'UPSTREAM_BRANCH', None) or os.environ.get("UPSTREAM_BRANCH", "master")
UPDATE_PKGS = getattr(config, 'UPDATE_PKGS', None) or os.environ.get("UPDATE_PKGS", "False")