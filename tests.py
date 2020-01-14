from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'date': 1578499809, 'from_id': 11973212, 'id': 84, 'out': 0, 'peer_id': 11973212,
                   'text': '1', 'conversation_message_id': 83, 'fwd_messages': [], 'important': False,
                   'random_id': 0, 'attachments': [],
                   'is_hidden': False},
        'group_id': 189286301, 'event_id': 'c0c99049c2571af5ecc4b83aef94f3b101390001'}



    def test_run(self):
        count = 5
        obj = {"a": 1}
        events = [obj] * count
        long_poll_listen_mock = Mock()
        long_poll_listen_mock.listen = Mock(return_value=events)
        with patch("bot.vk_api.VkApi"):
            with patch("bot.VkBotLongPoll", return_value=long_poll_listen_mock):
                bot = Bot("", "")
                bot.on_event = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        with patch("bot.vk_api.VkApi"):
            with patch("bot.VkBotLongPoll"):
                bot = Bot("", "")
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)
        send_mock.assert_called_once_with(peer_id=self.RAW_EVENT['object']['peer_id'],
                                          message=self.RAW_EVENT['object']['text'],
                                          random_id=ANY)

    # def test_get_user_name(self):
    #     get_name = Mock()
    #     with patch("bot.vk_api.VkApi"):
    #         with patch("bot.VkBotLongPoll"):
    #             bot = Bot("", "")
    #             bot.api = Mock()
    #             bot.api.users.get = get_name
    #             bot.api.get_name(self.RAW_EVENT['object']['from_id'])
    #     get_name.assert_called_once_with(user_id=self.RAW_EVENT['object']['from_id'])


if __name__ == '__main__':
    pass
