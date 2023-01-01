from random import randint
from time import sleep
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, ChatAction, ReplyKeyboardRemove


class User():
    def __init__(self, update):
        try:
            self.id = int(update.message.chat_id)
            self.name = update.message.from_user.first_name
        except Exception:
            self.id = int(update.callback_query.from_user.id)
            self.name = update.callback_query.from_user.first_name
        try:
            self.text = update.message.text
        except Exception:
            pass
        try:
            self.username = update.message.from_user.username
        except Exception:
            pass
        try:
            self.phone_num = update.message.contact.phone_number
        except Exception:
            pass
        try:
            self.photo_id = update.message.photo[-1].file_id
        except Exception:
            pass
        try:
            self.msg_id = update.callback_query.message.message_id
        except Exception:
            pass
        try:
            current_position = (update.message.location.longitude, update.message.location.latitude)
            self.coords = '{},{}'.format(current_position[0],current_position[1])
        except Exception:
            pass

class Bot(User):
    def __init__(self, context, update):
        super().__init__(update)
        self.context = context
    def send_msg(self, text):
        self.typing()
        self.context.bot.send_message(text=text, chat_id=self.id, reply_markup=ReplyKeyboardRemove())
    def send_msg_with_inline(self, text, buttons_list):
        self.typing()
        self.context.bot.send_message(text=text, chat_id=self.id, reply_markup=InlineKeyboardMarkup(buttons_list))
    def send_msg_with_keyboard(self, text, buttons_list):
        self.typing()
        self.context.bot.send_message(text=text, chat_id=self.id, reply_markup=ReplyKeyboardMarkup(buttons_list, resize_keyboard=True,
                                                                                                   one_time_keyboard=True))
    def typing(self):
        self.context.bot.send_chat_action(action=ChatAction.TYPING, chat_id=self.id)
        sleep(randint(1, 2))
    def sending_pht(self):
        self.context.bot.send_chat_action(action=ChatAction.UPLOAD_PHOTO, chat_id=self.id)
        sleep(randint(1, 2))
    def edit_message_without_buttons(self, text):
        self.context.bot.edit_message_text(text=text, chat_id=self.id, message_id=self.msg_id, reply_markup=None)
    def edit_message(self, text, buttons_list):
        self.context.bot.edit_message_text(text=text, chat_id=self.id, message_id=self.msg_id, reply_markup=InlineKeyboardMarkup(buttons_list))
    def send_pic(self,file):
        self.sending_pht()
        self.context.bot.send_photo(photo=file, chat_id = self.id)
    def send_pic_with_caption(self,file, text):
        self.sending_pht()
        self.context.bot.send_photo(photo=file, chat_id = self.id, caption=text)
