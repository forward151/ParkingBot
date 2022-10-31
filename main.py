from dotenv import dotenv_values
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import csv
import time
from datetime import datetime
from db_operations import check_user_status, add_user_data, take_data, change_user_status, add_date_for_user, clear_data

DELTA_TIME = [1, 0, 2]
START_TIME = [21, 36]
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
        self.free = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0}
        self.open_registration = False
        self.max_num = 10
        self.add_keyboard = [
            ['Забронировать место на понедельник', 'Удалить бронь на понедельник'],
            ['Забронировать место на вторник', 'Удалить бронь на вторник'],
            ['Забронировать место на среду', 'Удалить бронь на среду'],
            ['Забронировать место на четверг', 'Удалить бронь на четверг'],
            ['Забронировать место на пятницу', 'Удалить бронь на пятницу']
        ]

    def file_operator(self):
        file = open('data.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['tg_id', 'name', 'patronymic', 'surname', 'car_number', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
        for i in self.result_list:
            writer.writerow([i['id'], i['name'], i['patronymic'], i['surname'], i['car'], i['monday'], i['tuesday'], i['wednesday'], i['thursday'], i['friday']])

        file.close()





    def text_operator(self, update, context):
        user_id = update.message.from_user['id']
        text = update.message.text
        if user_id not in self.users_ids:
            context.bot.send_message(chat_id=user_id, text='К сожалению, у вас нет прав регистрации на автостоянку')
        else:
            if not self.open_registration:
                context.bot.send_message(chat_id=user_id, text='К сожалению, регистрация на автостоянку закрыта')

            else:
                user_status = check_user_status(user_id)
                print(user_status)
                if text == 'Забронировать место на понедельник' and user_status == 6:
                    if self.free['monday'] >= self.max_num:
                        context.bot.send_message(chat_id=user_id,
                                                 text='К сожалению, все места на понедельник заняты')
                        return
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку на понедельник',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['monday'] = True
                    add_date_for_user(local_data, 1)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if not flg:
                        self.result_list.append(take_data(user_id))
                        self.free['monday'] += 1
                    else:
                        self.result_list[idx]['monday'] = 1
                        self.free['monday'] += 1


                elif text == 'Удалить бронь на понедельник' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку на понедельник',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['monday'] = False
                    add_date_for_user(local_data, 1)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if flg:
                        self.result_list[idx]['monday'] = 0
                        self.free['monday'] -= 1
                elif text == 'Забронировать место на вторник' and user_status == 6:
                    if self.free['tuesday'] >= self.max_num:
                        context.bot.send_message(chat_id=user_id,
                                                 text='К сожалению, все места на вторник заняты')
                        return
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку на вторник',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['tuesday'] = True
                    add_date_for_user(local_data, 2)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if not flg:
                        self.result_list.append(take_data(user_id))
                        self.free['tuesday'] += 1
                    else:
                        self.result_list[idx]['tuesday'] = 1
                        self.free['tuesday'] += 1

                elif text == 'Удалить бронь на вторник' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку на вторник',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['tuesday'] = False
                    add_date_for_user(local_data, 2)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if flg:
                        self.result_list[idx]['tuesday'] = 0
                        self.free['tuesday'] -= 1
                elif text == 'Забронировать место на среду' and user_status == 6:
                    if self.free['wednesday'] >= self.max_num:
                        context.bot.send_message(chat_id=user_id,
                                                 text='К сожалению, все места на среду заняты')
                        return
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку на среду',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['wednesday'] = True
                    add_date_for_user(local_data, 3)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if not flg:
                        self.result_list.append(take_data(user_id))
                        self.free['wednesday'] += 1
                    else:
                        self.result_list[idx]['wednesday'] = 1
                        self.free['wednesday'] += 1

                elif text == 'Удалить бронь на среду' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку на среду',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['wednesday'] = False
                    add_date_for_user(local_data, 3)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if flg:
                        self.result_list[idx]['wednesday'] = 0
                        self.free['wednesday'] -= 1
                elif text == 'Забронировать место на четверг' and user_status == 6:
                    if self.free['thursday'] >= self.max_num:
                        context.bot.send_message(chat_id=user_id,
                                                 text='К сожалению, все места на четверг заняты')
                        return
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку на четверг',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['thursday'] = True
                    add_date_for_user(local_data, 4)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if not flg:
                        self.result_list.append(take_data(user_id))
                        self.free['thursday'] += 1
                    else:
                        self.result_list[idx]['thursday'] = 1
                        self.free['thursday'] += 1

                elif text == 'Удалить бронь на четверг' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку на четверг',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['thursday'] = False
                    add_date_for_user(local_data, 4)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if flg:
                        self.result_list[idx]['thursday'] = 0
                        self.free['thursday'] -= 1
                elif text == 'Забронировать место на пятницу' and user_status == 6:
                    if self.free['friday'] >= self.max_num:
                        context.bot.send_message(chat_id=user_id,
                                                 text='К сожалению, все места на пятницу заняты')
                        return
                    context.bot.send_message(chat_id=user_id, text='Вы зарегистрировались на автостоянку на пятницу',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['friday'] = True
                    add_date_for_user(local_data, 5)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if not flg:
                        self.result_list.append(take_data(user_id))
                        self.free['friday'] += 1
                    else:
                        self.result_list[idx]['friday'] = 1
                        self.free['friday'] += 1

                elif text == 'Удалить бронь на пятницу' and user_status == 6:
                    context.bot.send_message(chat_id=user_id, text='Вы удалили бронь на автостоянку на пятницу',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                    local_data = take_data(user_id)
                    local_data['friday'] = False
                    add_date_for_user(local_data, 5)
                    flg = False
                    idx = 0
                    for i in range(len(self.result_list)):
                        if self.result_list[i]['id'] == user_id:
                            flg = True
                            idx = i
                    if flg:
                        self.result_list[idx]['friday'] = 0
                        self.free['friday'] -= 1

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
                        self.user_data[user_id]['monday'] = False
                        self.user_data[user_id]['tuesday'] = False
                        self.user_data[user_id]['wednesday'] = False
                        self.user_data[user_id]['thursday'] = False
                        self.user_data[user_id]['friday'] = False
                        context.bot.send_message(chat_id=user_id, text='Регистрация завершена. Теперь вы можете забронировать место',
                                                  reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
                        change_user_status(user_id, 6)
                        add_user_data(self.user_data[user_id])



                    else:
                        context.bot.send_message(chat_id=user_id, text='Действие не распознано, воспользуйтесь клавиатурой',
                                              reply_markup=ReplyKeyboardMarkup(self.add_keyboard))

                print(self.result_list)





    def open_message(self, context: CallbackContext):
        self.open_registration = True
        for user_id in self.users_ids:
            try:
                context.bot.send_message(chat_id=user_id, text='Открыта регистрация на автостоянку',
                                          reply_markup=ReplyKeyboardMarkup(self.add_keyboard))
            except:
                continue

    def close_message(self, context: CallbackContext):
        self.open_registration = False
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
        fst_key = False
        scd_key = False
        thd_key = False
        not_clear_data = True
        while True:
            h = datetime.now().hour
            m = datetime.now().minute
            wd = datetime.now().weekday()
            if wd == 5 and not_clear_data:
                clear_data()
                self.free = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0}
            if h == START_TIME[0] and m == START_TIME[1] and wd not in WEEK_LST and fst_key is False:
                self.warning_message(self.dp)
                fst_key = True
                scd_key = False
                not_clear_data = False
            if h == START_TIME[0] and m == START_TIME[1] + DELTA_TIME[0] and wd not in WEEK_LST and scd_key is False:
                self.open_message(self.dp)
                scd_key = True
                thd_key = False
                not_clear_data = False
            if h == START_TIME[0] + DELTA_TIME[1] and m == START_TIME[1] + DELTA_TIME[2] and wd not in WEEK_LST and thd_key is False:
                self.close_message(self.dp)
                thd_key = True
                fst_key = False
                not_clear_data = False

            time.sleep(5)


if __name__ == '__main__':
    tg_bot = Bot()

    tg_bot.start()