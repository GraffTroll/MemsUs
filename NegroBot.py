from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime
import psycopg2
import random
from aiogram.utils.callback_data import CallbackData

memes = ['1', '2', '3', '4', '5', '6', '7', '8', '9',                 # Делаю вид типа шарю за списки
         '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
         '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
         '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
         '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
         '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
         '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
         '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
         '80', '81', '82', '83', '84', '85', '86', '87', '88',
          ]


bot = Bot(token='6170342020:AAFpoZ7WaavFzGK8_4XGj8-U7TjkRLMdQ2U')

iad = 1
#######################БАЗА ДАННЫХ################################
connection = psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password="12344321",
        database="MEME"
        )
connection.autocommit = True
##################################################################



#######################ТЕЛЕГРАМ БОТ###############################

#создаю кнопки и сокращение подключения
kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Каталог')
b2 = KeyboardButton(text='Мои сохры')
b3 = KeyboardButton(text='Статистика')
kb.add(b1).add(b2).add(b3)

dp = Dispatcher(bot)   # Облегчаю себе жизнь


@dp.message_handler(commands=['start']) # По факту должна регать пользователя и перенаправлять дальше с кнопками
async def start_step(message: types.Message):
    global iad
    iad = "@"+message.from_user.username #Юзер пользователя
    print(iad)
    with connection.cursor() as cursor: # Проверяю есть ли он в бд
        cursor.execute(
            f"""
            SELECT id FROM user_meme WHERE user_ = '{iad}';
        
            """
                    )
        if cursor.fetchone() == None:   # Добавляю если его нет
            print(12)
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO user_meme (user_, save_pic, see_like, see_dislike, see_all) VALUES ('{iad}', ARRAY['1'], 0, 0, 0); 
                    """
                           )                                                               # Йо, это не баг, это фича лол
            await bot.send_message(chat_id=message.from_user.id,
                               text='Вы только что зарегались',
                               reply_markup=kb)
        else:
        

            await bot.send_message(chat_id=message.from_user.id,
                           text='Вы уже зареганы',
                           reply_markup=kb)

                                        # Начинаю делать основную часть 


  
@dp.message_handler(text='Каталог') # В задумке здесь реализовать отправку мема с ожиданием реакции
async def catalog_step(message: types.Message):
    global random_pic
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='❤️',
                               callback_data="like")
    ib2 = InlineKeyboardButton(text='💔',
                               callback_data="dislike") # Кнопки по инлайну
    ikb.add(ib1, ib2)
    random_pic = random.choice(memes)
    MEMEphoto = f"C:\\Users\\Q\\Desktop\\Прога\\Мемы\\1 ({random_pic}).jpg" # Случайная фоточка
    photo = open(MEMEphoto, 'rb')
    await bot.send_photo(message.chat.id,
                         photo=photo,
                         caption="Как тебе?",
                         reply_markup=ikb)
    with connection.cursor() as cursor: # Быстренько добавляю просмотр 
            cursor.execute(
            f"""UPDATE user_meme
            SET see_all = see_all + 1 
            WHERE user_ = '{iad}';"""
            )

@dp.message_handler(text='Мои сохры') # Хочу вывести случайную пикчу из сохранённых
async def sohr_step(message: types.Message):
    with connection.cursor() as cursor: # Собств беру списочек с сохрами 
            cursor.execute(
            f"""SELECT save_pic FROM user_meme
            WHERE user_ = '{iad}'
            """                       
                        )
            sohra = cursor.fetchone()
    random_sohra = random.choice(sohra[0])
    print(random_sohra)
    MEMEphoto = f"C:\\Users\\Q\\Desktop\\Прога\\Мемы\\1 ({random_sohra}).jpg" # Опять случайная фоточка но из сохр
    photo = open(MEMEphoto, 'rb')
                        
                        
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo,
                         reply_markup=kb)



@dp.message_handler(text='Статистика') # Здесь наверно буду считать сколько чувак нажал + и сколько -
async def stata_step(message: types.Message):
    with connection.cursor() as cursor: 
            cursor.execute(
            f"""SELECT see_all FROM user_meme
            WHERE user_ = '{iad}'
            """                       
            )
            see_all = cursor.fetchone()

            
    with connection.cursor() as cursor: 
            cursor.execute(
            f"""SELECT see_like FROM user_meme
            WHERE user_ = '{iad}'
            """                       
            )
            see_like = cursor.fetchone()


    with connection.cursor() as cursor: 
            cursor.execute(
            f"""SELECT see_dislike FROM user_meme
            WHERE user_ = '{iad}'
            """                       
            )
            see_dislike = cursor.fetchone()



    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Чувак, чекни свою статут по сохрам\nВсего посмотрел пикч: {see_all[0]}\nПонравилось вот столько: {see_like[0]}\nКринжанул с {see_dislike[0]}'
                                 ,
                           reply_markup=kb)




@dp.callback_query_handler()                # Обработка этих инлайн кнопок
async def otvet_step(callback: types.CallbackQuery):
    global random_pic
    print(random_pic)
    if callback.data == 'like':
        await callback.answer('Йо, ты её сохранил')
        with connection.cursor() as cursor: # Быстренько добавляю лайк 
            cursor.execute(
            f"""UPDATE user_meme
            SET see_like = see_like + 1 
            WHERE user_ = '{iad}';""" 
            )
        with connection.cursor() as cursor: # Добавляю сохру в БД  
            cursor.execute(
            f"""UPDATE user_meme
            SET save_pic = ARRAY_APPEND(save_pic, '{random_pic}') 
            WHERE user_ = '{iad}';"""                           
            )
        await catalog_step(callback.message)



        
        
    if callback.data == 'dislike':           # Здесь тоже нужно учёт поставить сколько чел раз тыкнул
        await callback.answer('Думаю тебе стоит поискать ещё')
        with connection.cursor() as cursor: # Быстренько добавляю кринге 
            cursor.execute(
            f"""UPDATE user_meme
            SET see_dislike = see_dislike + 1 
            WHERE user_ = '{iad}';""" 
            )
        await catalog_step(callback.message)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)












































