
from .models import ChatRoom, User

def get_or_create_private_chat(user1, user2):
    """
    Get or create a private chat room between two users.
    """
    
    usernames = sorted([user1.username, user2.username])
    room_name = f"private_{usernames[0]}_{usernames[1]}"


    room = ChatRoom.objects.filter(name=room_name, is_private=True).first()

    if not room:

        room = ChatRoom.objects.create(name=room_name, is_private=True)
        room.participants.add(user1, user2)

    return room