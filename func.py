import time

from classes import *
from const import *
from sql_req import *
from telegram import KeyboardButton, ReplyKeyboardMarkup

def start(update, context):
    bot = Bot(update=update, context=context)
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    try:
        print('{} : {}'.format(bot.username, bot.id))
    except Exception:
        pass
    if bot.id > 0:
        try:
            id = cur.execute(select_id.format(bot.id)).fetchone()[0]
            if bot.id == ADMIN_ID:
                admin_menu(update, context)
            else:
                menu(update,context)
        except TypeError:
            if bot.id == ADMIN_ID:
                cur.execute(admin_insert.format(bot.id))
                admin_menu(update, context)
            else:
                bot.send_msg(STRT_MSGS[0])
                cur.execute(first_insert.format(bot.id))
                bot.send_msg(STRT_MSGS[1])
                bot.send_msg(STRT_MSGS[2])
    con.commit()

def text_answer(update, context):
    bot = Bot(update=update, context=context)
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    stage = cur.execute(select_stage.format(bot.id)).fetchone()[0]
    buttons = []
    if bot.id == ADMIN_ID:
        if bot.text == ADM_BUTT_LIST[0]:
            cur.execute(set_stage.format(51, bot.id))
            ids = cur.execute(select_all_ids).fetchall()
            for e in ids:
                name = cur.execute(select_name.format(e[0])).fetchone()[0]
                buttons.append([KeyboardButton(text=name)])
            buttons.append([KeyboardButton(text='Закончить')])
            bot.send_msg_with_keyboard(ADM_MSGS[0], buttons)
        elif bot.text == ADM_BUTT_LIST[1]:
            cur.execute(set_stage.format(52, bot.id))
            ids = cur.execute(select_all_ids).fetchall()
            for e in ids:
                name = cur.execute(select_name.format(e[0])).fetchone()[0]
                buttons.append([KeyboardButton(text=name)])
            buttons.append([KeyboardButton(text='Закончить')])
            bot.send_msg_with_keyboard(ADM_MSGS[1], buttons)
        elif bot.text == ADM_BUTT_LIST[2]:
            cur.execute(set_stage.format(53, bot.id))
            ids = cur.execute(select_all_ids).fetchall()
            for e in ids:
                name = cur.execute(select_name.format(e[0])).fetchone()[0]
                buttons.append([KeyboardButton(text=name)])
            bot.send_msg_with_keyboard(ADM_MSGS[2], buttons)
        elif bot.text == ADM_BUTT_LIST[3]:
            ids = cur.execute(select_all_ids).fetchall()
            lst = []
            for e in ids:
                name = cur.execute(select_name.format(e[0])).fetchone()[0]
                total = cur.execute(select_total.format(e[0])).fetchone()[0]
                lst.append([total, name])
            new_l = sorted(lst, reverse=True)
            s = ''
            c = 1
            for e in new_l:
                if c == 1:
                    s += '👑 {} : {} 🪙\n'.format(e[1], e[0])
                    c += 1
                else:
                    s += '{}. {} : {} 🪙\n'.format(c, e[1], e[0])
                    c += 1
            bot.send_msg(text=s)
            admin_menu(update, context)
        elif bot.text == ADM_BUTT_LIST[4]:
            bot.send_msg('Введите сообщение, которое все получат: ')
            cur.execute(set_stage.format(55, bot.id))
        elif stage == 51:
            if bot.text == 'Закончить':
                f = open('madrichim.txt', 'r')
                names = []
                while True:
                    name = f.readline()
                    name = name[:-1]
                    if not name: break
                    names.append(name)
                ids = cur.execute(select_all_ids).fetchall()
                for e in ids:
                    name = cur.execute(select_name.format(e[0])).fetchone()[0]
                    if name in names:
                        context.bot.send_message(chat_id=e[0],
                                                 text='Директор не застал вас на трапезе, по этому вы не получаете токены за приём пищи')
                        time.sleep(0.5)
                        continue
                    else:
                        b = cur.execute(select_balance.format(e[0])).fetchone()[0]
                        t = cur.execute(select_total.format(e[0])).fetchone()[0]
                        t += 2
                        b += 2
                        cur.execute(set_balance.format(b, e[0]))
                        cur.execute(set_total.format(t, e[0]))
                f = open('madrichim.txt', 'w')
                f.close()
                cur.execute(set_stage.format(50, ADMIN_ID))
                admin_menu(update,context)
            else:
                f = open('madrichim.txt', 'a')
                f.write(bot.text + '\n')
                f.close()
        elif stage == 52:
            if bot.text == 'Закончить':
                f = open('madrichim.txt', 'r')
                names = []
                while True:
                    name = f.readline()
                    name = name[:-1]
                    if not name: break
                    names.append(name)
                ids = cur.execute(select_all_ids).fetchall()
                for e in ids:
                    name = cur.execute(select_name.format(e[0])).fetchone()[0]
                    if name in names:
                        context.bot.send_message(chat_id = e[0], text='Вы опоздали на мадриховку, по этому не получите токены за пунктуальность')
                        time.sleep(0.5)
                        continue
                    else:
                        b = cur.execute(select_balance.format(e[0])).fetchone()[0]
                        t = cur.execute(select_total.format(e[0])).fetchone()[0]
                        t += 5
                        b += 5
                        cur.execute(set_balance.format(b, e[0]))
                        cur.execute(set_total.format(t, e[0]))
                f = open('madrichim.txt', 'w')
                f.close()
                cur.execute(set_stage.format(50, ADMIN_ID))
                admin_menu(update, context)
            else:
                f = open('madrichim.txt', 'a')
                f.write(bot.text + '\n')
                f.close()
        elif stage == 53:
            name = bot.text
            f = open('madrichim.txt', 'w')
            f.write(name)
            cur.execute(set_stage.format(54, ADMIN_ID))
            bot.send_msg(ADM_MSGS[3])
        elif stage == 54:
            f = open('madrichim.txt', 'r')
            name = f.readline()
            id = cur.execute('''
                            SELECT TG_ID
                            FROM Users
                            WHERE NAME = '{}'
                            '''.format(name)).fetchone()[0]
            balance = cur.execute(select_balance.format(id)).fetchone()[0]
            tok = int(bot.text)
            balance += tok
            total = cur.execute(select_total.format(id)).fetchone()[0]
            total += tok
            cur.execute(set_total.format(total,id))
            cur.execute(set_balance.format(balance,id))
            con.commit()
            ids = cur.execute(select_all_ids).fetchall()
            for e in ids:
                context.bot.send_message(chat_id=e[0], text=ADM_MSGS[4].format(tok, name))
                time.sleep(0.5)
            f.close()
            f = open('madrichim.txt', 'w')
            f.close()
            cur.execute(set_stage.format(50, ADMIN_ID))
            admin_menu(update, context)
        elif stage == 55:
            text = bot.text
            ids = cur.execute(select_all_ids).fetchall()
            for e in ids:
                context.bot.send_message(chat_id = e[0], text='❗❗ Объявление от директора ❗❗\n"{}"'.format(text))
                time.sleep(0.5)
                cur.execute(set_stage.format(50, bot.id))
                admin_menu(update, context)
        else: admin_menu(update, context)

    else:
        if stage == 0:
            cur.execute(set_name.format(bot.text, bot.id))
            cur.execute(set_stage.format(1,bot.id))
            buttons = [[KeyboardButton(text=MENU[0]), KeyboardButton(text=MENU[1])],[KeyboardButton(text=MENU[2]), KeyboardButton(text=MENU[3])]]
            bot.send_msg_with_keyboard(text=MENU_MSG, buttons_list=buttons)
        if stage == 1:
            if bot.text == MENU[0]:
                bot.send_msg(MON_MSG)
                for e in range(1,17):
                    bot.send_pic_with_caption(open('JOBS/{}.jpg'.format(e),'rb'),text=DESCRIPTIONS[e-1])
                menu(update, context)
            elif bot.text == MENU[1]:
                b = cur.execute(select_balance.format(bot.id)).fetchone()[0]
                for e in POSITIONS:
                    butt = [KeyboardButton(text=e)]
                    buttons.append(butt)
                buttons.append([KeyboardButton(text='Назад 🔙')])
                bot.send_msg_with_keyboard(text=POS_MSG.format(b), buttons_list=buttons)
            elif bot.text == MENU[2]:
                ids = cur.execute(select_all_ids).fetchall()
                lst = []
                for e in ids:
                    name = cur.execute(select_name.format(e[0])).fetchone()[0]
                    total = cur.execute(select_total.format(e[0])).fetchone()[0]
                    lst.append([total,name])
                new_l = sorted(lst, reverse=True)
                s = ''
                c = 1
                for e in new_l:
                    if c == 1:
                        s += '👑 {} : {} 🪙\n'.format(e[1], e[0])
                        c += 1
                    else:
                        s += '{}. {} : {} 🪙\n'.format(c,e[1],e[0])
                        c += 1
                bot.send_msg(text=s)
                menu(update, context)
            elif bot.text == MENU[3]:
                b = cur.execute(select_balance.format(bot.id)).fetchone()[0]
                bot.send_msg('Ваш баланс: {}🪙'.format(b))
                menu(update, context)
            elif bot.text == MENU[4]:
                bot.send_msg(FAQ)
                menu(update, context)
            elif bot.text in POSITIONS:
                balance = cur.execute(select_balance.format(bot.id)).fetchone()[0]
                price = int(bot.text.split('\n')[1][:-1])
                if balance < price:
                    bot.send_msg(BUYING[0].format(price-balance))
                else:
                    bot.send_msg(BUYING[1])
                    ids = cur.execute(select_all_ids).fetchall()
                    name = cur.execute(select_name.format(bot.id)).fetchone()[0]
                    balance -= price
                    cur.execute(set_balance.format(balance,bot.id))
                    con.commit()
                    for e in ids:
                        context.bot.send_message(chat_id = e[0], text=BUYING[2].format(name, bot.text.split('\n')[0]))
                        time.sleep(1.5)
                    menu(update, context)
            elif bot.text == 'Назад 🔙':
                menu(update, context)
    con.commit()

def menu(update, context):
    bot = Bot(update=update, context=context)
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    stage = cur.execute(select_stage.format(bot.id)).fetchone()[0]
    if stage == 1:
        buttons = [[KeyboardButton(text=MENU[0]), KeyboardButton(text=MENU[1])], [KeyboardButton(text=MENU[2]), KeyboardButton(text=MENU[3])],[KeyboardButton(text=MENU[4])]]
        bot.send_msg_with_keyboard(text=MENU_MSG, buttons_list=buttons)





def admin_menu(update, context):
    bot = Bot(update=update, context=context)
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    buttons = [[KeyboardButton(text=ADM_BUTT_LIST[0])],
               [KeyboardButton(text=ADM_BUTT_LIST[1])],
               [KeyboardButton(text=ADM_BUTT_LIST[2])],
               [KeyboardButton(text=ADM_BUTT_LIST[3])],
               [KeyboardButton(text=ADM_BUTT_LIST[4])]]
    bot.send_msg_with_keyboard(ADM_HELLO,buttons)




def imba(update, context):
    bot = Bot(update=update, context=context)
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute(set_balance.format(1000, bot.id))
    con.commit()