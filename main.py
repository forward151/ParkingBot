from dotenv import dotenv_values
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import csv
import time
from datetime import datetime
from db_operations import check_user_status, add_user_data, take_data, change_user_status

DELTA_TIME = [1, 0, 2]
START_TIME = [21, 1]
WEEK_LST = []


class Bot:

    def __init__(self):
        self.users_ids = [1474831001]
        self.result_list = []
        self.user_data = {}
        self.keys = dotenv_values('local_tokens.env')
        self.tg_token = self.keys['token']
        self.updater = Updater(self.tg_token)
        self.dp = self.updater.dispatcher
        self.open = False
        self.max_num = 10
        self.count = 0
        self.add_keyboard = [
            ['Забронировать место', 'Удалить бронь']
        ]

    def file_operator(self):
        file = open('data.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['tg_id', 'name', 'patronymic', 'surname', 'car_number'])
        for i in self.result_list:
            writer.writerow([i[0], i[1], i[2], i[3], i[4]])

        file.close()





    def text_operator(self, update, context):
        user_id = update.message.from_user['id']
        text = update.message.text
        if user_id not in self.users_ids:
            context.bot.send_message(chat_id=user_id, text='К сожалению, у вас нет прав регистрации на автостоянку')
        else:
            if not self.open:
                if self.count >= self.max_num:
                    context.bot.send_message(chat_id=user_id, text='К сожалению, все места забронированы')
                else:
                    context.bot.send_message(chat_id=user_id, text='К сожалению, регистрация на автостоянку закрыта')

            else:
                user_status = check_user_status(user_id)
                print(user_status)
                if text == 'Забронировать место' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    if take_data(user_id) not in self.result_list:
                        self.result_list.append(take_data(user_id))
                        self.count += 1
                        if self.count >= self.max_num:
                            self.open = False

                elif text == 'Удалить бронь' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    if take_data(user_id) in self.result_list:
                        self.result_list.remove(take_data(user_id))
                        self.count -= 1
                        if self.count < self.max_num:
                            self.open = True

                else:
                    if user_status == 1:
                        context.bot.send_message(chat_id=user_id, text='Необходимо зарегистрироваться. Введите свое имя',
                                                  reply_markup=ReplyKeyboardRemove())
                        change_user_status(user_id, 2)
                        self.user_data[user_id] = {'id': user_id}
                    elif user_status == 2:
                        self.user_data[user_id]['name'] = text
                        context.bot.send_message(chat_id=user_id, text='Теперь введите свое отчество',
                                                  reply_markup=ReplyKeyboardRemove())
                        change_user_status(user_id, 3)
                    elif user_status == 3:
                        self.user_data[user_id]['patronymic'] = text
                        context.bot.send_message(chat_id=user_id, text='Введите свою фамилию',
                                                  reply_markup=ReplyKeyboardRemove())
                        change_user_status(user_id, 4)
                    elif user_status == 4:
                        self.user_data[user_id]['surname'] = text
                        context.bot.send_message(chat_id=user_id, text='Введите номер своей машины',
                                                  reply_markup=ReplyKeyboardRemove())
                        change_user_status(user_id, 5)
                    elif user_status == 5:
                        self.user_data[user_id]['car'] = text
                        context.bot.send_message(chat_id=user_id, text='Регистрация завершена. Теперь вы можете забронировать место',
                                                  reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                        change_user_status(user_id, 6)
                        add_user_data(self.user_data[user_id])



                    else:
                        context.bot.send_message(chat_id=user_id, text='Действие не распознано, воспользуйтесь клавиатурой',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))

                print(self.result_list)





    def open_message(self, context: CallbackContext):
        self.open = True
        for user_id in self.users_ids:
            try:
                context.bot.send_message(chat_id=user_id, text='Открыта регистрация на автостоянку',
                                          reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
            except:
                continue

    def close_message(self, context: CallbackContext):
        self.open = False
        for user_id in self.users_ids:
            try:
                context.bot.send_message(chat_id=user_id, text='Регистрация на автостоянку закрыта',
                                          reply_markup=ReplyKeyboardRemove())
            except:
                continue
        print(self.result_list)
        self.file_operator()

    def warning_message(self, context: CallbackContext):
        self.result_list = []
        for user_id in self.users_ids:
            try:
                context.bot.send_message(chat_id=user_id,
                                         text='Через 10 минут будет открыта регистрация на автостоянку')
            except:
                continue

    def start(self):
        text_handler = MessageHandler(Filters.text, self.text_operator)
        self.dp.add_handler(text_handler)
        self.updater.start_polling()
        print('bot starts')
        print('bot continue')
        fst_key = False
        scd_key = False
        thd_key = False
        while True:
            h = datetime.now().hour
            m = datetime.now().minute
            wd = datetime.now().weekday()
            if h == START_TIME[0] and m == START_TIME[1] and wd not in WEEK_LST and fst_key is False:
                self.warning_message(self.dp)
                fst_key = True
                scd_key = False
            if h == START_TIME[0] and m == START_TIME[1] + DELTA_TIME[0] and wd not in WEEK_LST and scd_key is False:
                self.open_message(self.dp)
                scd_key = True
                thd_key = False
            if h == START_TIME[0] + DELTA_TIME[1] and m == START_TIME[1] + DELTA_TIME[2] and wd not in WEEK_LST and thd_key is False:
                self.close_message(self.dp)
                thd_key = True
                fst_key = False

            time.sleep(5)


if __name__ == '__main__':
    tg_bot = Bot()

    tg_bot.start()