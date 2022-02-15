from distutils import command
import telebot
from config import TOKEN

from agegender_demo import start


bot = telebot.TeleBot(TOKEN)

knownUsers = []
userStep = {}


@bot.message_handler(commands=['start'])
def getStartCommand(message):
    chatID = message.chat.id

    if chatID not in knownUsers:
        knownUsers.append(chatID)
        userStep[chatID] = 0
        bot.send_message(chatID, "Привет-привет, я умею определять пол и возраст человека по фоточке.\n\nДавай, пришли мне кого-нибудь или себя, а я взгляну.")
    else:
        bot.send_message(chatID, "Привет, а ты тут уже был, давай фотку, сейчас посмотрю!")


@bot.message_handler(commands=['help'])
def getHelpCommand(message):
    bot.send_message(message.chat.id, "Можешь прислать мне фоточку, а я определю пол и возраст человечка на ней!\n\nТакже у меня есть некоторые пасхалочки, которые ты можешь найти :)")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def getPhotoMessage(message):
    print('message.photo =', message.photo)

    if message.photo is None:
        return

    fileID = message.photo[-1].file_id
    fileInfo = bot.get_file(fileID)
    downloadedFile = bot.download_file(fileInfo.file_path)

    with open ("image.jpg", "wb") as newFile:
        newFile.write(downloadedFile)

    age, gender = start("image.jpg")

    if (age == 0):
        bot.reply_to(message, "Ты где там спрятался, я тебя не вижу!")
        return
    
    k = age % 10

    if (age > 9) and (age < 20) or (age > 110) or (k > 4) or (k == 0):
        ageEndWord = 'лет'
    else:
        ageEndWord = "год" if k == 1 else "года"
    
    resultMessage = "Опа, ты {0} и тебе {1} {2}".format(gender, age, ageEndWord)
    bot.reply_to(message, resultMessage)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    chatID = message.chat.id
    messageText = message.text.lower()

    if messageText == "aboba" or messageText == "абоба":
        img = open('./dataset/aboba.jpg', 'rb')

        bot.send_message(chatID, "Чё, шутник что ли, а может бан?)")
        bot.send_photo(chatID, img)
    elif messageText == "отправь чмоню" or messageText == "чмоня":
        img = open('./dataset/chmonya.jpg', 'rb')

        bot.send_message(chatID, "Опа, а вот это милый котик, даа...")
        bot.send_photo(chatID, img)
    elif messageText == "about" or messageText == "автор":
        img = open('./dataset/author.jpg', 'rb')

        bot.send_message(chatID, "Вот он, мой создатель Сашка, крутой чел и в целом приятный парень")
        bot.send_photo(chatID, img)
    else:
        bot.send_message(chatID, "Не понял, ты либо по делу пиши, либо фотку грузи.\n\nЕсли не знаешь что делать, пиши /help")


bot.polling(none_stop=True, interval=0)
