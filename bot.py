from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize, BotCommand, )
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(storage=storage)

admins = [1114704281, 938955199] #938955199
users = {}
unical_id = 1

class FSMFillForm(StatesGroup):
    fill_admin = State()                 # Состояние управления ботом для админов
    fill_admin_add_text_help = State()
    fill_admin_new_text_help = State()
    fill_new = State()                   # Состояние ожидания даты и времени записи от пользователя
    fill_answer = State()                # Состояние ожидания ответа по заявке от админа

# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/about_as',
                   description='Расскажу о нашем коллективе'),
        BotCommand(command='/view',
                   description='Покажу наши выступления'),
        BotCommand(command='/new',
                   description='Записаться на занятие'),
        BotCommand(command='/date',
                   description='Когда ближайший концерт?'),
        BotCommand(command='/contacts',
                   description='О руководителе'),
        BotCommand(command='/help',
                   description='Задать вопрос'),

        ]

    await bot.set_my_commands(main_menu_commands)

def about_as_filter(message: Message) -> bool:
    return message.text == '/about_as'

def view_filter(message: Message) -> bool:
    return message.text == '/view'

def new_filter(message: Message) -> bool:
    return message.text == '/new'

def date_filter(message: Message) -> bool:
    return message.text == '/date'

def help_filter(message: Message) -> bool:
    return message.text == '/help'

def contacts_filter(message: Message) -> bool:
    return message.text == '/contacts'

def admin_filter(message: Message) -> bool:
    if message.text == '/admin':
        if message.from_user.id in admins:
            return True

def admin_add_text_help_filter(message: Message) -> bool:
    return message.text == '/admin_add_text_help'

def admin_new_text_help_filter(message: Message) -> bool:
    return message.text == '/admin_new_text_help'

def answer_yes_filter(message: Message) -> bool:
    return message.text == '/answer_yes'

def answer_no_filter(message: Message) -> bool:
    return message.text == '/answer_no'

def show_filter(message: Message) -> bool:
    return message.text == '/show'

# Этот хэндлер будет срабатывать на команду /start
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Отлично!\n'
                              'Теперь я запущен и могу полноценно работать\n'
                              '\n'
                              'Что вы хотите узнать?\n'
                              'Нажмите на кнопку меню, и выберите действие:')


# Этот хэндлер будет срабатывать на команду "/about_as"
@dp.message(about_as_filter, StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Здесь будет лежать информация о вокальной студии - текст и пару фоток')

# Этот хэндлер будет срабатывать на команду "/view"
@dp.message(view_filter, StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Здесь будут видео (ссылки на ютуб) с выступлениями')

# Этот хэндлер будет срабатывать на команду "/new"
@dp.message(new_filter, StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Напишите день и время, когда Вы хотите записаться на занятие')
    await state.set_state(FSMFillForm.fill_new)

@dp.message(StateFilter(FSMFillForm.fill_new))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Мы обработаем вашу заявку в ближайшее время и дадим ответ')
    key = str(message.from_user.id)+" "+str(message.text)
    users[key] = key
    for admin in admins:
        await bot.send_message(chat_id=admin, text="Вам поступила новая заявка")
        await bot.send_message(chat_id=admin, text='Чтобы посмотреть все активные заявки \n'
                                                   'Отправьте команду /admin')
    await state.set_state(default_state)

# Этот хэндлер будет срабатывать на команду "/date"
@dp.message(date_filter, StateFilter(default_state))
async def process_start_command(message: Message):
    f = open('date_text.txt', 'r')
    str1 = f.read()
    f.close()
    await message.answer(text=str1)

# Этот хэндлер будет срабатывать на команду "/contacts"
@dp.message(contacts_filter, StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Руководитель вокальной студии "Звёздочка"\n'
                              'Попадука Юлия ..'
                              'В общем сюда информации добавить и фото')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(help_filter, StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Вы всегда можете задать свой вопрос лично руководителю вокальной студии\n'
                              'Здесь будет ссылка на создание чата с Юлией')

@dp.message(admin_filter, StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Вам как админу доступны следующие команды:\n'
                              'Посмотреть все необработанные заявки - /show\n'
                              'Обновить информацию о ближайшем концерте\n'
                              '- /admin_new_text_help \n'
                              'Дописать информацию о ближайшем концерте\n'
                              '- /admin_add_text_help')
    await state.set_state(FSMFillForm.fill_admin)

@dp.message(show_filter, StateFilter(FSMFillForm.fill_admin))
async def process_start_command(message: Message, state: FSMContext):
    if len(users)>0:
        for keys in users:
            await message.answer(text=users[keys])
        await message.answer(text='Чтобы обработать заявку, скопируйте выбранную заявку и допишите да или нет в конце')
        await state.set_state(FSMFillForm.fill_answer)
    elif len(users)==0:
        await message.answer(text='Необработанных заявок нет')
        await state.set_state(default_state)

@dp.message(StateFilter(FSMFillForm.fill_answer))
async def process_start_command(message: Message, state: FSMContext):
    answer = message.text.split()
    if answer[-1].lower()=='да':
        await message.answer(text="Вы приняли заявку")
        answer2 = "Вашу заявку успешно одобрили ("
        for i in range(1,len(answer)-1):
            answer2+=answer[i]+" "
        answer2 += ")"
        await bot.send_message(chat_id=answer[0], text=answer2)
        users.pop(message.text[:-3])
    elif answer[-1].lower()=='нет':
        await message.answer(text="Вы отказались от заявки")
        answer2 = "Вашу заявку отклонили ("
        for i in range(1, len(answer) - 1):
            answer2 += answer[i] + " "
        answer2 += ")"
        await bot.send_message(chat_id=answer[0], text=answer2)
        users.pop(message.text[:-4])
    else:
        await message.answer(text="Я не понял вашего ответа, скопируйте выбранную заявку и допишите да или нет в конце")
    await state.set_state(default_state)

@dp.message(admin_new_text_help_filter, StateFilter(FSMFillForm.fill_admin))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Напиши текст сообщения, который нужно добавить')
    await state.set_state(FSMFillForm.fill_admin_new_text_help)

# Этот хэндлер будет срабатывать только для админов, когда они введут текст
@dp.message(StateFilter(FSMFillForm.fill_admin_new_text_help))
async def process_start_command(message: Message, state: FSMContext):
    f = open('date_text.txt', 'w')
    f.write(message.text+'\n')
    f.close()
    await message.answer(text='Ваш текст был обновлен')
    await state.set_state(default_state)

@dp.message(admin_add_text_help_filter, StateFilter(FSMFillForm.fill_admin))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Напиши текст сообщения для вкладки ближайший концерт')
    await state.set_state(FSMFillForm.fill_admin_add_text_help)

# Этот хэндлер будет срабатывать только для админов, когда они введут текст
@dp.message(StateFilter(FSMFillForm.fill_admin_add_text_help))
async def process_start_command(message: Message, state: FSMContext):
    f = open('date_text.txt', 'a')
    f.write(message.text+'\n')
    f.close()
    await message.answer(text='Ваш текст был обновлен')
    await state.set_state(default_state)

# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, не понимаю Вас')


# Запускаем поллинг
if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)