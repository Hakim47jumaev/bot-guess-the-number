from telebot import TeleBot, types
import psycopg2
 

bot = TeleBot("7200472270:AAF8u1LRxt-KsM4JyyMBtzUO_pbqAxjt49Y")


def connection_database():
    connection = psycopg2.connect(
        database="polechud",
        user="postgres",
        host="localhost",
        password=".......",
        port=5432
    )
    return connection

def close_connection(conn, cur):
    cur.close()
    conn.close()

def create_tables():
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                ID SERIAL PRIMARY KEY,
                USER_ID VARCHAR(100) UNIQUE,
                FIRST_NAME VARCHAR(30) NOT NULL,
                LAST_NAME VARCHAR(30) NOT NULL,
                USERNAME VARCHAR(60) NOT NULL,
                IS_ADMIN BOOL DEFAULT FALSE
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS QUESTIONS (
                ID SERIAL PRIMARY KEY,
                TG_ID VARCHAR(50),
                NAME VARCHAR(50),
                DISCRIPTIONS VARCHAR(100)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS FEEDBACKS (
                ID SERIAL PRIMARY KEY,
                TG_ID VARCHAR(50),
                name varchar(50),
                FEED VARCHAR(59) 
            );
        """) 
        conn.commit()
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_connection(conn, cur)

def add_users(user_id, first_name, last_name, username):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO USERS (USER_ID, FIRST_NAME, LAST_NAME, USERNAME) VALUES (%s, %s, %s, %s)
            ON CONFLICT (USER_ID) DO NOTHING""", (user_id, first_name, last_name, username))
        conn.commit()
    except Exception as e:
        bot.send_message(user_id, "Ин корбар аллакай вуҷуд дорад")
    finally:
        close_connection(conn, cur)  

def check_user_exists(user_id):
    conn = connection_database()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT 1 FROM USERS WHERE USER_ID = '{user_id}' ")
        result = cur.fetchone()
        return bool(result)
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_connection(conn, cur)

def send_welcome_message(user_id):
    global usenamee
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Калимаи нав илова кардан')
    btn2 = types.KeyboardButton('Бозиро оғоз кардан')
    btn3 = types.KeyboardButton('Дидани калимахои худ')
    btn4 = types.KeyboardButton('РОҲНАМО')
    btn5 = types.KeyboardButton('Додани шарҳ')
    btn6 = types.KeyboardButton('Дидани ҳамаи калимаҳо')
    btn7 = types.KeyboardButton('Дидани ҳамаи шарҳҳо')
    btn8 = types.KeyboardButton('Нест кардани шарҳ')
    btn9 = types.KeyboardButton('Иваз кардани шарҳ')
    btn10 = types.KeyboardButton('Иваз кардани калима')
    btn11 = types.KeyboardButton('Нест кардани калима')
    if usenamee=='hkm220':
        markup.add(btn1, btn3, btn6 )
        markup.add( btn11, btn10,btn5 )
        markup.add( btn7,btn8,btn9)
        
    else:
        markup.add(btn1, btn5 )
        markup.add( btn3, btn4  )
        markup.add(  btn2 )
    bot.send_message(user_id, " Бот кор карда истодааст.....", reply_markup=markup)
usenamee=''
@bot.message_handler(commands=['start'])
def start(message):
    create_tables()
    global usenamee
    user_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username
    usenamee=username
    if check_user_exists(user_id):
        bot.send_message(user_id, "Шумо аллакай ба қайд гирифта шудаед!")
         
    if not first_name:
        msg = bot.send_message(user_id, 'Номи худро ворид кунед')
        bot.register_next_step_handler(msg, get_first_name, last_name, username)
    elif not last_name:
        msg = bot.send_message(user_id, 'Насаби худро ворид кунед')
        bot.register_next_step_handler(msg, get_last_name, first_name, username)
    elif not username:
        msg = bot.send_message(user_id, 'Номи корбарии худро ворид кунед')
        bot.register_next_step_handler(msg, get_username, first_name, last_name)
    else:
        add_users(user_id, first_name, last_name, username)
        send_welcome_message(user_id)

def get_first_name(message, last_name, username):
    first_name = message.text
    if not last_name:
        msg = bot.send_message(message.chat.id, 'Насаби худро ворид кунед')
        bot.register_next_step_handler(msg, get_last_name, first_name, username)
    elif not username:
        msg = bot.send_message(message.chat.id, 'Номи корбарии худро ворид кунед')
        bot.register_next_step_handler(msg, get_username, first_name, last_name)
    else:
        add_users(message.chat.id, first_name, last_name, username)
        send_welcome_message(message.chat.id)

def get_last_name(message, first_name, username):
    last_name = message.text
    if not username:
        msg = bot.send_message(message.chat.id, 'Номи корбарии худро ворид кунед')
        bot.register_next_step_handler(msg, get_username, first_name, last_name)
    else:
        add_users(message.chat.id, first_name, last_name, username)
        send_welcome_message(message.chat.id)

def get_username(message, first_name, last_name):
    username = message.text
    add_users(message.chat.id, first_name, last_name, username)
    send_welcome_message(message.chat.id)

@bot.message_handler()
def hendler(messege):
    if messege.text == 'Калимаи нав илова кардан':
        add_word(messege)
    elif messege.text == 'Бозиро оғоз кардан':
        start_game(messege)
    elif messege.text == 'Дидани калимахои худ':
        get_my_words(messege)
    elif messege.text == 'Додани шарҳ':
        feed(messege)
    elif messege.text == 'РОҲНАМО':
        help(messege)
    elif messege.text == 'Дидани ҳамаи калимаҳо':
        get_all_words(messege)
    elif messege.text == 'Дидани ҳамаи шарҳҳо':
        get_all_feeds(messege)
    elif messege.text == 'Нест кардани шарҳ':
        delete_feeds(messege)
    elif messege.text == 'Нест кардани калима':
        delete_words(messege)
    elif messege.text == 'Иваз кардани калима':
        chenge_words(messege)
    elif messege.text == 'Иваз кардани шарҳ':
        chenge_feeds(messege)

def help(messege):
    bot.send_message(messege.chat.id, f"""
Салом мӯҳтарам  {messege.chat.first_name}
Шумо қарор доред дар чат-боти бозӣ, барои муайян намудани дараҷаи калимадонии шумо.Дар бот як калимаи махфишуда бо таффсилоташ ба шумо мешниҳод карда мешавад, шумо бояд онро ҳарф ба ҳарф ё пурра муайян намоед. Барои ин шумо 10 шонс доред .
МУВАФФАҚИЯТ
""")

def chenge_feeds(messege):
    get_all_feeds(messege)
    bot.send_message(messege.chat.id,'ID-и   шарҳееро, ки шумо нест кардан мехоҳед, ворид кунед')
    bot.register_next_step_handler(messege,chenge_fedd)

feedd=''
def chenge_fedd(messege):
    global feedd
    feedd=messege.text
    bot.send_message(messege.chat.id,' Шарҳи навро ворид кунед ')
    bot.register_next_step_handler(messege,chenge_feedd)

def chenge_feedd(messege):
    conn=connection_database()
    cur=conn.cursor()
    try:
        cur.execute(f"update feedbacks  set feed = '{messege.text}' where id='{feedd}'")
        bot.send_message(messege.chat.id,' Шарҳ иваз шуд')
    except:
        bot.send_message(messege.chat.id,'Шарҳ ёфт нашуд ')



def chenge_words(messege):
    get_all_words(messege)
    bot.send_message(messege.chat.id,'Номи калимаеро, ки тағир додан мехоҳед, ворид кунед')
    bot.register_next_step_handler(messege,cheng_word )
lst=[]
name=''
def cheng_word (messege):
    global name
    name=messege.text
    bot.send_message(messege.chat.id,'Барои ин калима номи нав ворид кунед')
    bot.register_next_step_handler(messege,chenge_word_name)

def chenge_word_name(messege):
    global lst
    lst=['','']
    lst[0]=messege.text
    bot.send_message(messege.chat.id,'Барои ин калима тавсифи нав ворид кунед')
    bot.register_next_step_handler(messege,chenge_word_disc)
     
def chenge_word_disc(messege):
    global name
    global lst
    lst[1]=messege.text
     
    try:
        conn=connection_database()
        cur=conn.cursor()
        cur.execute(f"""
update questions set  name='{lst[0]}' , discriptions='{lst[1]}'
where name='{name}' 
""")
        conn.commit()
        bot.send_message(messege.chat.id,f"Калимаи {f'{name}'} бомуваффақият иваз карда шуд")
    except:
        bot.send_message(messege.chat.id,f"{name} ёфт нашуд")




def delete_words(messege):
    get_all_words(messege)
    bot.send_message(messege.chat.id,'Номи калимаеро, ки шумо нест карда мехоҳед, ворид кунед')
    bot.register_next_step_handler(messege,del_word)

def del_word(messege):
    conn=connection_database()
    cur=conn.cursor()
    try:
        cur.execute(f"delete from questions where name='{messege.text}'")
        conn.commit()
        bot.send_message(messege.chat.id,f"Калима бо номи {messege.text} бомуваффақият нест карда шуд")
    except:
        bot.send_message(messege.chat.id,f'{messege.text} ёфт нашуд')



def delete_feeds(messege):
    get_all_feeds(messege)
    bot.send_message(messege.chat.id,'ID-и   шарҳееро, ки шумо нест кардан мехоҳед, ворид кунед')
    bot.register_next_step_handler(messege,del_feed)

def del_feed(messege):
    conn=connection_database()
    cur=conn.cursor()
    try:
        cur.execute(f"delete from feedbacks where id={messege.text}")
        conn.commit()
        bot.send_message(messege.chat.id,f"Шарҳ бо ID-и {messege.text} бомуваффақият нест карда шуд")
    except:
        bot.send_message(messege.chat.id,f'Шарҳ бо ID-и{messege.text} ёфт нашуд')


def get_all_words(messege):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"select * from questions ")
    words=cur.fetchall()
    if words:
        for word in words:
            bot.send_message(messege.chat.id,f"{word[2]} \n {word[3]}")
    else:
        bot.send_message(messege.chat.id, "Дар база ҳанӯз ягон калима нест.")



def get_all_feeds(messege):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"select * from feedbacks ")
    words=cur.fetchall()
    if words:
        for word in words:
            bot.send_message(messege.chat.id,f""" id: {word[0]}  
user: {word[2]}   
feed: {word[3]}""")
    else:
        bot.send_message(messege.chat.id, " ")



def feed(messege):
    bot.send_message(messege.chat.id,"Enter your feedback --> ")
    bot.register_next_step_handler(messege,get_feed)

def get_feed(messege):
    conn=connection_database()
    cur=conn.cursor()
    feeed=messege.text
    cur.execute(f"insert into feedbacks(tg_id,name,feed) values('{messege.chat.id}','{messege.chat.first_name}','{feeed}')")
    conn.commit()
    bot.send_message(messege.chat.id,'Ташаккур барои фикру мулоҳиза. Мо кӯшиш мекунем, ки ҳама мушкилотро ҳал кунем')
        
def get_my_words(messege):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"select * from questions where tg_id='{messege.chat.id}'")
    words=cur.fetchall()
    if words:
        for word in words:
            bot.send_message(messege.chat.id,f"{word[2]} \n {word[3]}")
    else:
        bot.send_message(messege.chat.id, "Шумо то ҳол ягон калима илова накардаед.")

word_lst={}
def add_word(messege):
    word_lst[messege.chat.id]={
        'name':'',
        "disc":''
    }
    bot.send_message(messege.chat.id,'Калимаи нави худро ворид кунед')
    bot.register_next_step_handler(messege,add_word_name)

def add_word_name(messege):
    word_lst[messege.chat.id]['name']=messege.text
    bot.send_message(messege.chat.id,"Тавсифи ин калимаро ворид кунед")
    bot.register_next_step_handler(messege,add_disc)

def add_disc(messege):
    conn=connection_database()
    cur=conn.cursor()
    word_lst[messege.chat.id]['disc']=messege.text
    try:
        cur.execute(f"""
            INSERT INTO QUESTIONS (TG_ID, NAME, DISCRIPTIONS) VALUES ('{messege.chat.id}','{word_lst[messege.chat.id]['name']}','{word_lst[messege.chat.id]['disc']}')
        """)
        conn.commit()
        bot.send_message(messege.chat.id,"Калимаи нав дар база илова карда шуд")
    except Exception as ex:
        bot.send_message(messege.chat.id,ex)

games={}
def start_game(message):
    if message.text=='start':
        return
    user_id = message.chat.id
    games[user_id] = {'correct': False, 'attempts': 0}

    conn = connection_database()
    cur = conn.cursor()
    cur.execute("SELECT NAME, DISCRIPTIONS FROM QUESTIONS ORDER BY RANDOM() LIMIT 1")
    discs = cur.fetchone()
    close_connection(conn, cur)

    if discs:
        games[user_id]['correct_ans'] = discs[0].upper()   
        games[user_id]['description'] = discs[1]
        games[user_id]['revealed_letters'] = ['x '] * len(discs[0])

        bot.send_message(user_id, f" Калимаро муаян кунед: \n\n{games[user_id]['description']}")
        bot.send_message(user_id, f"{' '.join(games[user_id]['revealed_letters'])}")
        bot.register_next_step_handler(message, check_guess)
    else:
        bot.send_message(user_id, "Ҳоло ягон калима дар база вуҷуд надорад.")

def check_guess(message):
    user_id = message.chat.id
    guess = message.text.strip().upper()

    if guess == games[user_id]['correct_ans']:
        bot.send_message(user_id, f"Балее.Шумо ёфтед!  Ҷавоб {games[user_id]['correct_ans']} буд")
        games[user_id]['correct'] = True
        start_game(message)  
        return

    if len(guess) == 1 and guess.isalpha():
        games[user_id]['attempts'] += 1
        if guess in games[user_id]['correct_ans']:
             
            for i, letter in enumerate(games[user_id]['correct_ans']):
                if letter == guess:
                    games[user_id]['revealed_letters'][i] = guess
            bot.send_message(user_id, f"{' '.join(games[user_id]['revealed_letters'])}")
            if 'x 'not in games[user_id]['revealed_letters']:
                bot.send_message(user_id, f" Балее.Шумо ёфтед!  Ҷавоб {games[user_id]['correct_ans']} буд")
                games[user_id]['correct'] = True
                start_game(message)   
                return
            else:
                bot.send_message(user_id, "Кушиш карданро давом диҳед!")
                bot.register_next_step_handler(message, check_guess)
        else:
            bot.send_message(user_id, f"Ҳарфи нодуруст. Шумо {10 - games[user_id]['attempts']} шанси дигар доред.")
            if games[user_id]['attempts'] >= 10:
                bot.send_message(user_id, f"Шумо шансҳои худро тамом кардед.Ҷавоб {games[user_id]['correct_ans']} буд")
                start_game(message)
            else:
                bot.register_next_step_handler(message, check_guess)
    else:
        bot.send_message(user_id, "Лутфан як ҳарф ё номи пурраро ворид кунед.")
        bot.register_next_step_handler(message, check_guess)

bot.infinity_polling()