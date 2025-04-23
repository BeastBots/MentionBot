import sys
import os
import logging
from importlib import import_module
from subprocess import run as srun, call as scall
from os import path, remove, environ

# Logging setup
if path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)
if path.exists("rlog.txt"):
    remove("rlog.txt")

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

# Config/env merging
var_list = [
    "BOT_TOKEN", "MONGODB_URI", "OWNER_ID", "UPSTREAM_REPO", "UPSTREAM_BRANCH", "UPDATE_PKGS"
]
try:
    settings = import_module("bot.config_loader")
    config_file = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in vars(settings).items()
        if not key.startswith("__")
    }
except Exception:
    logging.info("config_loader.py import failed! Checking ENVs only.")
    config_file = {}

env_updates = {
    key: value.strip() if isinstance(value, str) else value
    for key, value in environ.items()
    if key in var_list
}
if env_updates:
    logging.info("Config data is updated with ENVs!")
    config_file.update(env_updates)

def get_config_flag(key, default=None):
    """
    Get a config flag from config_file (merged config/env),
    falling back to environment variable, then to default.
    """
    value = config_file.get(key)
    if value is not None:
        return value.strip() if isinstance(value, str) else value
    value = environ.get(key)
    if value is not None:
        return value.strip() if isinstance(value, str) else value
    return default

BOT_TOKEN = config_file.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN variable is missing! Exiting now")
    sys.exit(1)

UPSTREAM_REPO = config_file.get("UPSTREAM_REPO", "").strip()
UPSTREAM_BRANCH = config_file.get("UPSTREAM_BRANCH", "main").strip() or "main"
UPDATE_PKGS = config_file.get("UPDATE_PKGS", "True")

# Git update logic
if UPSTREAM_REPO:
    if path.exists(".git"):
        if os.name == "nt":
            srun(["rmdir", "/S", "/Q", ".git"], shell=True)
        else:
            srun(["rm", "-rf", ".git"])
    git_cmd = (
        f"git init -q && "
        f"git config --global user.email 131198906+ThePrateekBhatia@users.noreply.github.com && "
        f"git config --global user.name Prateek Bhatia && "
        f"git add . && "
        f"git commit -sm update -q || true && "
        f"git remote add origin {UPSTREAM_REPO} && "
        f"git fetch origin -q && "
        f"git reset --hard origin/{UPSTREAM_BRANCH} -q"
    )
    result = srun(git_cmd, shell=True)
    if result.returncode == 0:
        logging.info("Successfully updated with latest upstream repo!")
    else:
        logging.error("Git update failed! Check repo/branch details.")
    logging.info(f"UPSTREAM_REPO: {UPSTREAM_REPO} | UPSTREAM_BRANCH: {UPSTREAM_BRANCH}")

# Package update logic
if (isinstance(UPDATE_PKGS, str) and UPDATE_PKGS.lower() == "true") or UPDATE_PKGS is True:
    pip_cmd = f"pip install -U -r requirements.txt"
    result = srun(pip_cmd, shell=True)
    if result.returncode == 0:
        logging.info("Successfully updated all the packages!")
    else:
        logging.error("Failed to update packages!")
