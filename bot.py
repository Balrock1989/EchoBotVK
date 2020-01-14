#!/usr/bin/env python3.7

from random import randint
import logging

try:
    import settings
except ImportError:
    exit('DO cp settings.py.default in settings.py set token and group')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

""" 
versions -> requirements.txt
"""

log = logging.getLogger("bot")


def configure_logging():
    log.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%d-%m-%Y,%H:%M"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%d-%m-%Y,%H:%M"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)


class Bot:
    """ Основной класс бота """

    def __init__(self, token, group_id):
        """
        :param token: секретный токен группы VK
        :param group_id: ID группы VK
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.vk_api = self.vk.get_api()

    def run(self):
        """ Запуск бота """
        for event in self.long_poll.listen():  # Слушаем сервер
            try:
                self.on_event(event)
            except Exception:
                log.exception("Произошла ошибка")

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info("Получено новое сообщение")
            self.vk_api.messages.send(peer_id=event.object.peer_id,
                                      message=f'Привет, Вы сказали"{event.object.text}"!',
                                      random_id=randint(0, 10 ** 20))
            log.info("Сообщение успешно обработано и отправлен ответ")
        else:
            log.debug("Мы пока не умеем обрабатывать это событие %s", event.type)



    # def get_message(self, event: VkBotEventType):
    #     """
    #     Обработка ивента входящего сообщения
    #     :param event: VkBotMessageEvent object
    #     :return: None
    #     """
    #     username = self.get_user_name(event.object.from_id)
    #     print("Username: " + username)
    #     print("From: " + self.get_user_city(event.object.from_id))
    #     print("Text: " + event.object.text)
    #     print("Type: ", end="")
    #     if event.object.id > 0:
    #         print("private message")
    #     else:
    #         print("group message")
    #     print(" --- ")
    #     self.send_message(peer_id=event.object.peer_id,
    #                       message=f'Привет {username}, Вы сказали"{event.object.text}"!')

    def get_user_name(self, user_id):
        """ Получаем имя пользователя """
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']
    #
    # def get_user_city(self, user_id):
    #     """ Получаем город пользователя """
    #     return self.vk_api.users.get(user_id=user_id, fields="city")[0]["city"]['title']


if __name__ == '__main__':
    configure_logging()
    chatbot = Bot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    chatbot.run()

    #  UPDATE// в группе http://joxi.ru/Vm6MPVxT4Bqpgr в терминале http://joxi.ru/KAxK4aotZWLPw2

#  Первая часть - зачет!
