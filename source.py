import constant #подключаем файл с константными значениями
import data_base_mini   #подключаем файл для обработки наших функций
import telebot  #библиотека для взаимодействия с API нашего бота
import _thread
import time


bot = telebot.TeleBot(constant.token)  # указываем token бота для подключения
print(bot.get_me()) #вывод на консоль сведений о боте (полезно, чтобы понять, что бот активен)

@bot.message_handler(commands=['start'])    #показать клаву
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True,
                                                    False)  # атрибут адаптивности клавы и одноразового использования
    user_markup.row('/close_keyboard')  #команды для бота
    user_markup.row("Новая задача") #простое сообщение для бота
    user_markup.row("Сайт автора")
    bot.send_message(message.from_user.id, "Клавиатура активна!", reply_markup=user_markup) #выдача сооющения юзеру об активности клавиатуры

@bot.message_handler(commands=['help'])    #показать инструкцию
def handle_start(message):
    bot.send_message(message.from_user.id, "Это бот-помощник, он поможет Вам ничего не забыть!") #отправка сообщения юзеру с инструкцией
    bot.send_message(message.from_user.id, "Чтобы воспользоваться ботом нажмите /start и создайте новую задачу!")
    from datetime import datetime
    print('ФИО пользователя: ', message.from_user.first_name, message.from_user.last_name)
    print('ID user: ', message.from_user.id)
    print('Пользователь запросил инструкцию!')
    print('Время создания: ', datetime.today())
    print('\n-------\n\n')

@bot.message_handler(commands=['close_keyboard']) #спрятать клавиатуру
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()   #прятание клавиатуры
    bot.send_message(message.from_user.id, 'Клавиатура убрана!', reply_markup=hide_markup)  #выдача сообщения юзеру об неактивности клавиатуры

@bot.message_handler(content_types=['text'])
def handle_start(message):
    temp = str(message.from_user.id) + '.txt'  # ID user + расширение
    file_name_task = open(temp, 'a')  # создаём и открываем файл с именем ID user
    try:
        if (message.text.lower() == str('новая задача'.lower())):    #если новая задача, то создаём новую задачу с записью в базе
            bot.send_message(message.chat.id, 'Введите имя задачи') #запрос от бота на название задачи
            constant.variable_pass_for_get_name_task = 1    #переменная для дачи новой задаче имени

        elif(message.text.lower() == 'сайт автора'.lower()):
            bot.send_message(message.chat.id, 'Я в telegram: https://t.me/Nikulux')
            bot.send_message(message.chat.id, 'http://nikulux.ru')
            bot.send_message(message.chat.id, 'Сайт по обучению программированию и помощи в решении проблем')
            bot.send_message(message.chat.id, 'Вам понравится!')


            from datetime import datetime
            print('ФИО пользователя: ', message.from_user.first_name, message.from_user.last_name)
            print('ID user: ', message.from_user.id)
            print('Пользователь запросил Ваш сайт!')
            print('Время создания: ', datetime.today())
            print('\n-------\n\n')

        elif((constant.variable_pass_for_get_name_task == 1) and (message.text.lower() != 'Новая задача'.lower())):
            constant.name_task_y = message.text    #помещаем имя новой задачи в переменную

            from datetime import datetime  # библиотека для получения времени и даты
            date_and_time = datetime.now()

            file_name_task.write('Имя создателя: ')
            file_name_task.write(str(message.from_user.first_name))    #помещаем в файл имя создателя новой задачи
            file_name_task.write('\n')
            file_name_task.write('Фамилия создателя: ')
            file_name_task.write(str(message.from_user.last_name))  # помещаем в файл фамилию создателя новой задачи
            file_name_task.write('\n')
            file_name_task.write('ID создателя: ')
            file_name_task.write(str(message.from_user.id))  # помещаем в файл ID создателя новой задачи
            file_name_task.write('\n\n')
            file_name_task.write('Время создания задачи: ')
            file_name_task.write(str(date_and_time))    #помещаем в файл запись о времени создания новой задачи
            file_name_task.write('\n')
            file_name_task.write('Имя задачи: ')
            file_name_task.write(str(constant.name_task_y))    #помещаем в файл имя новой задачи

            print('ФИО пользователя: ', message.from_user.first_name, message.from_user.last_name)
            print('ID user: ', message.from_user.id)
            print('Название задачи: ', constant.name_task_y)
            print('Время создания: ', date_and_time)

            constant.temp_user_id = message.from_user.id    #сохраняем сообщение юзера
            constant.name_task_and_user_id.setdefault(str(constant.name_task_y), str(message.from_user.id)) #добавляем в базу имя задачи и ID юзера

            temp_db = data_base_mini.read_name_task_and_user_id()   #временная переменная для проверки наличия одинаковости задачи
            if(temp_db == 'ERROR_TIME'):
                bot.send_message(message.chat.id, 'Извините, произошла ошибка ввода!')
                bot.send_message(message.chat.id, 'Попробуйте снова!')
                constant.variable_pass_for_get_name_task = 0  # переменная-пропуск для получения имени задачи
                constant.variable_pass_for_run_timer = 0  # переменная-пропуск для запуска таймера
                constant.variable_pass_for_function_reminders = 0  # переменная-пропуск для напоминалки
                del constant.name_task_and_user_id[constant.name_task_y]
                print('\nПользователь совершил ошибку в указании времени!')
                file_name_task.write('\n')
                file_name_task.write('Пользователь совершил ошибку в указании времени!')
                file_name_task.write('\n-------\n\n')
                file_name_task.close()

            if(temp_db == False or temp_db == None):    #условие для проверки существования такой же задачи
                constant.variable_pass_for_run_timer = 1    #если не правда, то блок таймера становится доступным использовать
                today = datetime.today()
                today_time = 'Например: ' + str(today.strftime("%Y.%m.%d %H:%M:%S"))
                bot.send_message(message.chat.id, 'Введите время отведённое на выполнение этой задачи')
                bot.send_message(message.chat.id, 'Формат даты должен быть следующий: день.месяц.год час:минута:секунда')
                bot.send_message(message.chat.id, today_time)
                bot.send_message(message.chat.id, 'Кстати, это время, которое сейчас')

            else:
                bot.send_message(message.chat.id, 'Вы уже создали такую задачу!')
                print('Пользователь уже создал такую задачу!')
                file_name_task.write('\n')
                file_name_task.write('Такая задача уже была создана!')
                file_name_task.write('\n-------\n\n')
                file_name_task.close()

            constant.variable_pass_for_get_name_task = 0    #зануляем чтобы можно было снова использовать этот блок

        elif ((constant.variable_pass_for_run_timer == 1) and (message.text.lower() != 'Новая задача'.lower())):    #блок таймера

            from datetime import datetime  # библиотека для получения времени и даты
            time_for_calculation = str(message.text)
            date_now = datetime.today()

            if(time_for_calculation > str(date_now)):
                temp_time_for_calculation = data_base_mini.calculation_time(time_for_calculation, date_now)

                print('Дата окончания задачи: ', str(time_for_calculation))
                file_name_task.write('\n')
                file_name_task.write('Дата окончания задачи: ')
                file_name_task.write(str(time_for_calculation))
                file_name_task.write('\n')

                size_timer = temp_time_for_calculation
                constant.size_timer = float(size_timer)  #преобразуем во float тип, требуется для корректного задания условия таймера

                constant.variable_pass_for_run_timer = 0    #зануляем, чтобы таймер не активировался случайно
                constant.variable_pass_for_function_reminders = 1
                bot.send_message(message.chat.id, 'Сколько раз Вам напомнить о Вашей задаче?')

            else:
                bot.send_message(message.chat.id, 'Извините, произошла ошибка ввода!')
                bot.send_message(message.chat.id, 'Попробуйте сначала!')
                constant.variable_pass_for_get_name_task = 0  # переменная-пропуск для получения имени задачи
                constant.variable_pass_for_run_timer = 0  # переменная-пропуск для запуска таймера
                constant.variable_pass_for_function_reminders = 0  # переменная-пропуск для напоминалки
                del constant.name_task_and_user_id[constant.name_task_y]
                print('Неправильное время окончания задачи!')
                file_name_task.write('\n')
                file_name_task.write('Неправильное время окончания задачи!')
                file_name_task.write('\n-------\n\n')
                file_name_task.close()

        elif((constant.variable_pass_for_function_reminders == 1) and (message.text.lower() != 'Новая задача'.lower())):

            def SMS1(rerere, eeee):
                name_task_time_end = 'Напоминаю о задаче ' + '"' + str(rerere) + '"' + ', сделате её, я жду!!!'  # красиво оформленный ответ бота о завершении задачи
                time.sleep(eeee)
                bot.send_message(message.chat.id, name_task_time_end)  # бот отвечает юзеру

            def SMS2(rerere, eeee):
                name_task_time_end = 'Срок для задачи ' + '"' + str(rerere) + '"' + ' пришёл'  # красиво оформленный ответ бота о завершении задачи
                time.sleep(eeee)
                bot.send_message(message.chat.id, name_task_time_end)  # бот отвечает юзеру
                del constant.name_task_and_user_id[rerere]  #удаляем ячейку в базе в связи с не актуальностью


            temp_message_for_count = int(message.text)   #запись в переменную сообщения пользователя о количестве повторов

            print('Количество напоминаний: ', str(temp_message_for_count))
            file_name_task.write('\n')
            file_name_task.write('Количество напоминаний: ')    #запись в лог-файл количества напоминаний
            file_name_task.write(str(temp_message_for_count))
            file_name_task.write('\n')

            if(temp_message_for_count == 1):    #если пользователь запросил одно напоминание
                temp_message_for_count = 2  #то отправить напоминание в общее время делить пополам
                temp_r = constant.size_timer / temp_message_for_count
                temp_message_for_count = 1
            elif(temp_message_for_count == 0):  #если пользователь запросил ноль напоминаний
                temp_r = 0  #то не отправлять ему напоминания
            else:
                temp_r = constant.size_timer / temp_message_for_count   #иначе отправлять напоминания общее время делёное на кол-во напоминаний
            temp = temp_r

            for m in range(0, temp_message_for_count):  #цикл для кол-ва таймеров-напоминалок
                if(temp != temp_message_for_count):
                    _thread.start_new_thread(SMS1, (str(constant.name_task_y), temp))   #наводим таймер на указанное время
                temp += temp_r


            _thread.start_new_thread(SMS2, (str(constant.name_task_y), constant.size_timer+0.01))   #таймер с окончанием времени задачи
            bot.send_message(message.chat.id, 'Поздравляю!\nВы приступили к реализации новой задачи!')  #уведомление об успешной операции

            file_name_task.write('\n-------\n\n')   #запись в файл окончания лога
            file_name_task.close()  #закрытие файла



        else:   #вариант на случай, если юзер ввёл сообщение, которое не было запланировано
            bot.send_message(message.chat.id, 'Прошу прощения, я Вас не понял...')

            from datetime import datetime
            print('ФИО пользователя: ', message.from_user.first_name, message.from_user.last_name)
            print('ID user: ', message.from_user.id)
            print('Пользователь ввёл: ', message.text)
            print('Время создания: ', datetime.today())
            print('\n-------\n\n')


    except:
        print('Произошла ошибка при вводе входных данных!\n\n')
        bot.send_message(message.chat.id, 'Извините, произошла ошибка ввода!')
        bot.send_message(message.chat.id, 'Попробуйте снова!')
        constant.variable_pass_for_get_name_task = 0 #переменная-пропуск для получения имени задачи
        constant.variable_pass_for_run_timer = 0 #переменная-пропуск для запуска таймера
        constant.variable_pass_for_function_reminders = 0 #переменная-пропуск для напоминалки
        file_name_task.write('\n')
        file_name_task.write('Ошибка ввода входных данных!')
        file_name_task.write('\n-------\n\n')
        file_name_task.close()


bot.polling(none_stop=True, interval=0)  # вечный цикл бота


