import json
import os

FRIENDS_FILE = "friends.json"


class FriendManager:

    def __init__(self):
        if not os.path.exists(FRIENDS_FILE) or os.path.getsize(FRIENDS_FILE) == 0:
            with open(FRIENDS_FILE, "w") as f:
                json.dump({}, f)

    def add_friend(self, code):
        with open(FRIENDS_FILE, "r") as f:
            data = json.load(f)

        if code in data:
            print("Friend already added.")
            return

        data[code] = {"code": code}

        with open(FRIENDS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Friend added!")

    def show_friends(self):
        with open(FRIENDS_FILE, "r") as f:
            data = json.load(f)

        if not data:
            print("No friends added.")
            return

        print("\nFriends:")
        for code in data:
            print(f"- {code}")

