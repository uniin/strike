from models import User


def get_user_by_id(user_id, chat_id):
    try:
        return User().get(vk_id=user_id, chat=chat_id)
    except:
        User(
            vk_id=user_id,
            warns=0,
            chat=chat_id
        ).save()
        return User().get(vk_id=user_id, chat=chat_id)