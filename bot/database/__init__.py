from pymongo import MongoClient
import config

# Initialize MongoDB client
client = MongoClient(config.MONGO_URI)
db = client['mention']

# Collections
users_collection = db['user.pm']
groups_collection = db['groups']
commands_history_collection = db['commands.history']
boot_collection = db['boot']

# Ensure indexes for efficient queries
users_collection.create_index("user_id", unique=True)
groups_collection.create_index("group_id", unique=True)
