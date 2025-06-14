import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

import utils
from config import *


class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


class VkBot:

    def __init__(self):
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = MyLongPoll(self.vk_session, 207081595)

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message
                user_id = msg['from_id']
                chat_id = msg['peer_id'] - 2000000000
                # user = utils.get_user_by_id(user_id, chat_id)
                text = msg['text']

                # print(f'[{chat_id}] От {user_id}: {text}')

                global fwd, message

                try:
                    fwd = self.vk_session.method('messages.getByConversationMessageId', {
                        'conversation_message_ids': msg['conversation_message_id'],
                        'peer_id': msg['peer_id']
                    })['items'][0]

                    # print(fwd)

                    if 'reply_message' in fwd:
                        fwd = fwd['reply_message']
                    else:
                        fwd = None

                    # print(msg['conversation_message_id'])
                    # print(msg)
                    # print(msg['attachments'])
                    # print(msg['text'])
                    attachments = f"{msg['attachments']}"
                    sticker = 'sticker' in attachments
                    audio_message = 'audio_message' in attachments
                    # message = f"{msg['text']}"
                    # print(msg)

                    if chat_id in stickers:
                        if sticker:
                            self.vk_session.method('messages.delete', {
                                'group_id': 207081595,
                                'delete_for_all': 1,
                                'peer_id': msg['peer_id'],
                                'cmids': f"{msg['conversation_message_id']}"
                            })

                    if chat_id in audio_messages:
                        if audio_message:
                            self.vk_session.method('messages.delete', {
                                'group_id': 207081595,
                                'delete_for_all': 1,
                                'peer_id': msg['peer_id'],
                                'cmids': f"{msg['conversation_message_id']}"
                            })

                    if chat_id in messages:  # audio_message
                        self.vk_session.method('messages.delete', {
                            'group_id': 207081595,
                            'delete_for_all': 1,
                            'peer_id': msg['peer_id'],
                            'cmids': f"{msg['conversation_message_id']}"
                        })

                except Exception as n:
                    print(f'[ ! ] #{chat_id} | Исключение: {n}')

                """

                with open('bad_words.txt', 'r', encoding="utf-8", newline='') as words:
                    flag = False
                    forcheck = event.message.text.lower()
                    for word in words:
                        if flag:

                            user.warns += 1
                            user.save()

                            if user.warns != 3:
                                self.vk_session.method('messages.send', {
                                    'chat_id': msg['peer_id'] - 2000000000,
                                    'message': f'Тебе вынесено предупреждение. Штрафных баллов {user.warns}/3. '
                                               f'Старайся соблюдать правила беседы, написанные в закреплённом сообщении, 
                                               иначе нам придется с тобой попрощаться.',
                                    'random_id': 0
                                })

                            elif user.warns >= 3:
                                self.vk_session.method('messages.send', {
                                    'chat_id': msg['peer_id'] - 2000000000,
                                    'message': f'Тебе вынесено предупреждение. Штрафных баллов {user.warns}/3. '
                                               f'Увы, вы набрали максимальное количество штрафных баллов, мы вынуждены 
                                               попрощаться.',
                                    'random_id': 0
                                })

                                try:
                                    self.vk_session.method('messages.removeChatUser', {
                                        'user_id': fwd['from_id'],
                                        'chat_id': msg['peer_id'] - 2000000000
                                    })
                                except IndexError:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Вы что-то не правильно указали!',
                                        'random_id': 0
                                    })
                                except Exception:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Ошибка доступа: пользователя нет в этом чате/он является 
                                        администратором.',
                                        'random_id': 0
                                    })
                            break
                        else:
                            if forcheck.find(word[:-1]) != -1:
                                flag = True
                                
                """

                if user_id in admin_id:
                    try:
                        if fwd:
                            if text == 'кик' and fwd['from_id'] not in admin_id:
                                self.vk_session.method('messages.sendReaction', {
                                    'peer_id': msg['peer_id'],
                                    'cmid': f"{msg['conversation_message_id']}",
                                    'reaction_id': 2
                                })

                                self.vk_session.method('messages.send', {
                                    'chat_id': msg['peer_id'] - 2000000000,
                                    'message': f'Увы, нам пора прощаться.',
                                    'random_id': 0
                                })
                                try:
                                    self.vk_session.method('messages.removeChatUser', {
                                        'user_id': fwd['from_id'],
                                        'chat_id': msg['peer_id'] - 2000000000
                                    })
                                except IndexError:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Вы что-то не правильно указали!',
                                        'random_id': 0
                                    })
                                except Exception:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Ошибка доступа: пользователя нет в этом чате/он является '
                                                   f'администратором.',
                                        'random_id': 0
                                    })

                            elif text == 'пред' and fwd['from_id'] not in admin_id:
                                self.vk_session.method('messages.sendReaction', {
                                    'peer_id': msg['peer_id'],
                                    'cmid': f"{msg['conversation_message_id']}",
                                    'reaction_id': 2
                                })

                                fwd_user = utils.get_user_by_id(fwd['from_id'], msg['peer_id'] - 2000000000)

                                fwd_user.warns += 1
                                fwd_user.save()

                                if fwd_user.warns < 3:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Тебе вынесено предупреждение. Штрафных баллов {fwd_user.warns}/3. '
                                                   f'Старайся соблюдать правила беседы, написанные в закреплённом '
                                                   f'сообщении, иначе нам придется с тобой попрощаться.',
                                        'random_id': 0
                                    })

                                elif fwd_user.warns >= 3:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Тебе вынесено предупреждение. Штрафных баллов {fwd_user.warns}/3. '
                                                   f'Увы, вы набрали максимальное количество штрафных баллов, '
                                                   f'мы вынуждены попрощаться.',
                                        'random_id': 0
                                    })

                                    try:
                                        self.vk_session.method('messages.removeChatUser', {
                                            'user_id': fwd['from_id'],
                                            'chat_id': msg['peer_id'] - 2000000000
                                        })
                                    except IndexError:
                                        self.vk_session.method('messages.send', {
                                            'chat_id': msg['peer_id'] - 2000000000,
                                            'message': f'Вы что-то не правильно указали!',
                                            'random_id': 0
                                        })
                                    except Exception:
                                        self.vk_session.method('messages.send', {
                                            'chat_id': msg['peer_id'] - 2000000000,
                                            'message': f'Ошибка доступа: пользователя нет в этом чате/он является '
                                                       f'администратором.',
                                            'random_id': 0
                                        })
                            elif text == 'снять преды':
                                fwd_user = utils.get_user_by_id(fwd['from_id'], msg['peer_id'] - 2000000000)
                                fwd_user.warns = 0
                                fwd_user.save()

                                self.vk_session.method('messages.send', {
                                    'chat_id': msg['peer_id'] - 2000000000,
                                    'message': f'Пробил возврат предов. Текущий баланс пользователя {fwd_user.warns}/3 '
                                               f'очков социальной кармы.',
                                    'random_id': 0
                                })

                                self.vk_session.method('messages.sendReaction', {
                                    'peer_id': msg['peer_id'],
                                    'cmid': f"{msg['conversation_message_id']}",
                                    'reaction_id': 7
                                })
                            elif text == 'снять пред':
                                fwd_user = utils.get_user_by_id(fwd['from_id'], msg['peer_id'] - 2000000000)

                                if fwd_user.warns == 0:
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Текущий баланс пользователя {fwd_user.warns}/3 очков '
                                                   f'социальной кармы.',
                                        'random_id': 0
                                    })
                                else:
                                    fwd_user.warns -= 1
                                    fwd_user.save()

                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'Пробил возврат преда. Текущий баланс пользователя '
                                                   f'{fwd_user.warns}/3 очков социальной кармы.',
                                        'random_id': 0
                                    })

                                    self.vk_session.method('messages.sendReaction', {
                                        'peer_id': msg['peer_id'],
                                        'cmid': f"{msg['conversation_message_id']}",
                                        'reaction_id': 7
                                    })
                        else:
                            if text == 'пред' or text == 'кик' or text == 'снять пред' or text == 'снять преды':
                                self.vk_session.method('messages.sendReaction', {
                                    'peer_id': msg['peer_id'],
                                    'cmid': f"{msg['conversation_message_id']}",
                                    'reaction_id': 6
                                })
                            elif text == 'ping':
                                self.vk_session.method('messages.send', {
                                    'chat_id': msg['peer_id'] - 2000000000,
                                    'message': f'pong',
                                    'random_id': 0
                                })
                    except Exception as e:
                        print(f'[ ! ] #{chat_id} Исключение: {e}')
                elif text == '#модер' or text == '#moder' or text == '#модератор' or text == '#moderator':
                    self.vk_session.method('messages.send', {
                        'user_id': admin_id,
                        'message': f'Привет. \n\nВ чате под ID: {chat_id} была вызвана команда для призыва '
                                   f'модераторов: всем было отправлено соответствующее '
                                   f'уведомление!\n\nID пользователя: {user_id}.',
                        'random_id': 0
                    })


if __name__ == '__main__':
    VkBot().run()
