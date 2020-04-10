from mysql.connector    import MySQLConnection, Error
import telebot
import config
import sys

bot = telebot.TeleBot(config.TOKEN)

#Connect to DB
def connectDb(host="mysql_testzone", user="ohrimenko-dmitry", passwd="nY8UsWe=ybSg", db="ccss"):
    db = MySQLConnection(host="mysql_testzone",
                                 user="ohrimenko-dmitry",
                                 passwd="nY8UsWe=ybSg",
                                 db="confident")
    return db


def getUserData(userId=None):

    if(userId is not None and int(userId) > 0):
        dbConnect = connectDb()

        if(dbConnect.is_connected()):

            #Cursor options    
	    cursor = dbConnect.cursor()
	    cursor = dbConnect.cursor(buffered=True, dictionary=True)
        
	    #execute query, extract data, close connection
            query = "SELECT * FROM ap_members apm LEFT JOIN tg_bot_messages tbm ON tbm.user_id = apm.id WHERE apm.id=" + str(userId) + " LIMIT 1"
            cursor.execute(query) 
	    result = cursor.fetchone()
            cursor.close()

            return result
    return None



@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/AnimatedSticker.tgs', 'rb')

    bot.send_sticker(message.chat.id, sti)

    mess = "Welcome"

    print(message)
    print(message.from_user)
    print(bot.get_me())

    #bot.send_message(message.chat.id, mess.format(message.from_user, bot.get_me()), parse_mode="html")
    #bot.send_message(message.chat.id, "<a href='/' style='max-height: 300px; padding: 10px 5px'> TEST </a>", parse_mode="html")





#send message for user
@bot.message_handler(commands=['user'])
def getUser(message):
    bot.send_message(message.chat.id, "Hi <i style='text-decorate: underline;'>@" + message.from_user.username + "</i>! \n<b>Please, enter user id </b>", parse_mode="html")
    bot.register_next_step_handler(message, getUserInfo)

    print(message.from_user)


def getUserInfo(message):
    chat_id = message.chat.id
    userId = message.text

    if not userId.isdigit():
        msg = bot.send_message(chat_id, 'id must be is integer')
        bot.register_next_step_handler(msg, getUserInfo) #askSource
        return
    user = getUserData(userId)
    if(user is not None):
	

	if(user['alredy_send'] == 1):
	    bot.send_message(chat_id, "Sorry, already sent(")
	    return
	
	
	#Write to tg_bot_messages table that alredy sent
	dbConnect = connectDb()

        if(dbConnect.is_connected()):
 
            #Cursor options
	    cursor = dbConnect.cursor()
            
            #execute query, extract data, close connection
            query = "INSERT INTO tg_bot_messages (user_id, alredy_send) VALUES (" + userId + ", 1)"
            cursor.execute(query)
	    dbConnect.commit()
            cursor.close()
	msg = bot.send_message(chat_id, "User name: " + user['name'] + " Surname: " + user['cname'])
    else:
	msg = bot.send_message(chat_id, "User with id " + userId + " not found, sorry=(")



@bot.message_handler(commands=['revertUser'])
def revertUser(message):
    bot.send_message(message.chat.id, "Revert, please, enter user id:", parse_mode="html")
    bot.register_next_step_handler(message, revertUserData)

    print(message.from_user)


def revertUserData(message):
    chat_id = message.chat.id


    print(chat_id)

    userId = message.text

    #Write to tg_bot_messages table that alredy sent
    dbConnect = connectDb()

    if(dbConnect.is_connected()):

        #Cursor options
        cursor = dbConnect.cursor()

        #execute query, extract data, close connection
        query = "DELETE FROM tg_bot_messages WHERE user_id = " + userId
        cursor.execute(query)
        dbConnect.commit()
        cursor.close()
        msg = bot.send_message(chat_id, "User data with id " + userId + " reverted")



@bot.message_handler(content_types=['text'])
def echo_bot(message):

    print(message)
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)
