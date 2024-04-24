import telebot
import time 
import random
from datetime import datetime, timedelta
from time import sleep
import re
import requests
from pymongo import MongoClient
import json
import uuid

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove

uri = "mongodb+srv://c00478111:1234567890@cluster0.oqewumn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

bot_token = "7030821273:AAGFgjLnhjgxwCqWrkc-AQFBt4BtVxMr458" # Telegram bot token


bot = telebot.TeleBot(bot_token)

mongo_client = MongoClient(uri)

db = mongo_client["dem-ref-bot"]


admin_chat_id = 7119174092

min_with = 1
required_channels = ["@joinxyza", "@joinxyza", "@joinxyza", "@joinxyza"]
payment_channel = '@joinxyza'



def is_chat_member(user_id):
    channel_ids = ['@joinxyza', '@joinxyza', '@joinxyza', '@joinxyza']
    user_id = str(user_id)  # Convert to string in case it's an integer

    for channel_id in channel_ids:
        try:
            member = bot.get_chat_member(channel_id, user_id)
            if member.status in ['left', 'kicked']:
                return False  # Return False if the user is not a member of any channel
        except Exception as e:
            print(f"Error getting chat member for user {user_id} in channel {channel_id}: {e}")

    return True  # Return True if the user is a member of all channels







buttons = {
    'balance_btn': 'Check Balance',
    'referral_btn': 'Invite Users',
    'withdraw_btn': 'Withdraw',
    'back_btn': 'BACK'
}

def menu_markup():
    menu_button = ReplyKeyboardMarkup(resize_keyboard=True)

    m_button1 = KeyboardButton(buttons['balance_btn'])
    m_button2 = KeyboardButton(buttons['referral_btn'])
    m_button3 = KeyboardButton(buttons["withdraw_btn"])

    menu_button.add(m_button1,m_button2)
    menu_button.add(m_button3)

    return menu_button

def menu(user_id):

    start_message = (f"<b>Welcome to DreamxUPI World ❤️\n\n"
    "Choose Given Button To Earn....!! </b>")

    bot.send_message(chat_id=user_id, text= start_message,reply_markup=menu_markup(),parse_mode="HTML")

    time.sleep(1)
    ref_bons(user_id)


@bot.message_handler(commands=['broadcast'])
def send_broadcast(message):
    if message.chat.id == admin_chat_id:
        bot.send_message(message.chat.id, "Send Your Broadcast Message With HTMl")
        bot.register_next_step_handler(message, send_broadcast2)
    else:
        return

def send_broadcast2(message):
    user_ids = [user["user_id"] for user in db.users.find({}, {"user_id": 1})]
    for user_id in user_ids:
        try:
            message_id = bot.send_message(user_id, message.text,parse_mode="HTML")
            bot.pin_chat_message(chat_id=user_id, message_id=message_id.message_id)
            time.sleep(1)
        except Exception as e:
            return
            # print(f"Hata: {e}")

@bot.message_handler(commands=['broadcastwithbtn'])
def send_broadcast_with_btn(message):
    if message.chat.id == admin_chat_id:
        bot.send_message(message.chat.id, "Send Your Broadcast Message With HTML")
        bot.register_next_step_handler(message, send_broadcast_with_btn2)
    else:
        return

def send_broadcast_with_btn2(message):
    try:
        broadcast_info = {
            "msg": message.text,
            "btn_txt": "",
            "btn_url":"",
            "pic_url": ""
        }
        with open("broadcast_info.json", "w") as json_file:
            json.dump(broadcast_info, json_file)

        bot.send_message(message.chat.id, "Send Your Broadcast Button Text")
        bot.register_next_step_handler(message, send_broadcast_with_btn3)

    except Exception as e:
        print(f"Hata: {e}")

def send_broadcast_with_btn3(message):
    try:
        with open("broadcast_info.json", "r") as json_file:
            broadcast_info = json.load(json_file)
            broadcast_info["btn_txt"] = message.text

        with open("broadcast_info.json", "w") as json_file:
            json.dump(broadcast_info, json_file)

        bot.send_message(message.chat.id, "Send Your Broadcast Button URL")
        bot.register_next_step_handler(message, send_broadcast_with_btn4)

    except Exception as e:
        print(f"Hata: {e}")

def send_broadcast_with_btn4(message):
    try:
        with open("broadcast_info.json", "r") as json_file:
            broadcast_info = json.load(json_file)
            broadcast_info["btn_url"] = message.text

        with open("broadcast_info.json", "w") as json_file:
            json.dump(broadcast_info, json_file)

        bot.send_message(message.chat.id, "Send Your Broadcast Photo URL")
        bot.register_next_step_handler(message, send_broadcast_with_btn5)

    except Exception as e:
        print(f"Hata: {e}")

def send_broadcast_with_btn5(message):
    try:
        with open("broadcast_info.json", "r") as json_file:
            broadcast_info = json.load(json_file)
            broadcast_info["pic_url"] = message.text

        with open("broadcast_info.json", "w") as json_file:
            json.dump(broadcast_info, json_file)

        user_ids = [user["user_id"] for user in db.users.find({}, {"user_id": 1})]
        for user_id in user_ids:
            try:
                inline_keyboard = InlineKeyboardMarkup(row_width=2)
                button = [
                    InlineKeyboardButton(broadcast_info["btn_txt"], url=broadcast_info['btn_url'])
                ]
                inline_keyboard.add(*button)

                broadcast_message = broadcast_info["msg"]

                if broadcast_info["pic_url"]:
                    message_id = bot.send_photo(user_id, broadcast_info["pic_url"], broadcast_message, parse_mode="HTML", reply_markup=inline_keyboard)
                    bot.pin_chat_message(chat_id=user_id, message_id=message_id.message_id)
                    time.sleep(1)
                else:
                    message_id = bot.send_message(user_id, broadcast_message, parse_mode="HTML", reply_markup=inline_keyboard)
                    bot.pin_chat_message(chat_id=user_id, message_id=message_id.message_id)
                    time.sleep(1)

            except Exception as e:
                # print(f"Hata: {e}")
                return

    except Exception as e:
        return
        # print(f"Hata: {e}")


@bot.message_handler(commands=['status'])
def status_command(message):
    if message.chat.id == admin_chat_id:
        user_count = db.users.count_documents({})

        bot.send_message(message.chat.id, f"Total users: {user_count}")

@bot.message_handler(commands=['sus'])
def status_command(message):
  user_id = message.chat.id
  h = is_chat_member(user_id)
  bot.send_message(message.chat.id, f"Total users: {h}")


def send_hindi_message(user_id):
    bot.send_message(user_id, "कृपया सभी चैनलों को ज्वाइन करें।")

from telebot import types

def send_join_message(message):
    user_id = message.chat.id
    h = is_chat_member(user_id)
    if not h:
        join_markup = types.InlineKeyboardMarkup()
        join_markup.row(
            types.InlineKeyboardButton(text="Join", url="https://t.me/tehsiltech"),
            types.InlineKeyboardButton(text="Join", url="https://t.me/+oZvOhd0YeXZhMDY1")
        )
        join_markup.row(
            types.InlineKeyboardButton(text="Join", url="https://t.me/+NEF3KcQzI5BkMzc1"),
            types.InlineKeyboardButton(text="Join", url="https://t.me/Earning_Flash")
        )
        join_markup.row(
            types.InlineKeyboardButton(text="Join", url="https://t.me/TECH_MISMAMUL"),
            types.InlineKeyboardButton(text="Join", url="https://t.me/+hf5sPpkUse1iYTM1")
        )
        
        join_markup.row(types.InlineKeyboardButton(text="Verify", callback_data="verify"))

        bot.send_message(user_id, "*Must Join Our All channels before continue*", parse_mode='Markdown', reply_markup=join_markup)
        send_hindi_message(user_id)
    else:
        menu(user_id)





@bot.callback_query_handler(func=lambda call: call.data.split()[0] == "verify")
def verify_handle(call):
    send_welcome(call.message)
    return

@bot.callback_query_handler(func=lambda call: call.data == "/withdraw")
def withraw(call):
    user_id = call.from_user.id
    userData = db.users.find_one({'user_id':user_id})
    balance = userData.get('balance', 0)

    bot.delete_message(user_id,call.message.message_id)
    if float(balance)<float(min_with):
            bot.send_message(user_id,f"<b>Insufficient Balance : Minimum Required is {min_with} INR For Withdrawals.</b>",parse_mode="HTML",reply_markup=menu_markup())
            return

    back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_markup.add(KeyboardButton(buttons['back_btn']))

    bot.send_message(user_id,"Enter Your UPI Payment Address\n\nMust Include '@' in Your UPI ID",reply_markup=back_markup)

    bot.register_next_step_handler(call.message,process_withdraw_upi)


@bot.message_handler(commands=['start'])
def send_welcome(message):
        user_id = int(message.chat.id)
        first_name = message.chat.first_name

        # Track referral
        ref_by = message.text.split()[1] if len(message.text.split()) > 1 and message.  text.split()[1].isdigit() else None

        if not db.users.find_one({'user_id': user_id}):
            if ref_by and int(ref_by) != user_id and db.users.find_one({'user_id': int(ref_by)}):
                db.users.update_one({'user_id': user_id}, {'$set': {'user_id': user_id, 'ref_by': int(ref_by)}},upsert=True)
                db.users.update_one({'user_id': int(ref_by)}, {'$inc': {'total_ref': 1}},upsert=True)
            else:
                db.users.update_one({'user_id': user_id}, {'$set': {'user_id': user_id,'ref_by': "none"}},upsert=True)

        # Check user membership

        send_join_message(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_commands(message):
    user_id = message.chat.id
    first_name = message.chat.first_name
    bot_username = bot.get_me().username

    userData = db.users.find_one({'user_id':user_id})
    balance = userData.get('balance', 0)
    total_referral = userData.get('total_ref', 0)
    ref_link = f"https://telegram.me/{bot_username}?start={user_id}"
    status = userData.get('status',None)
    total_withdraw = userData.get('total_with',0)


    if not is_chat_member(user_id):
        send_join_message(message)
        return

    if message.text == buttons['back_btn']:
        menu(user_id)
        return

    if message.text == buttons['balance_btn']:
        b_markup = InlineKeyboardMarkup()
        b_markup.add(InlineKeyboardButton(text="Withdraw Balance",callback_data='/withdraw'))

        text = (f"💰 Balance : ₹{balance:.2f}\n\n"
                    "Use withdraw button to Transfer Balance in Upi Account ✅")

        bot.send_message(chat_id=user_id,text=text,parse_mode='markdown',reply_markup=b_markup)

    if message.text == buttons['referral_btn']:

        b_markup = InlineKeyboardMarkup()
        b_markup.add(InlineKeyboardButton(text="Withdraw Balance",callback_data='/withdraw'))

        text = (f"<b>First Invite 5 User's & Win UPTO 50 Rs UPI Cash</b> \n\n"
                    f"<b>Your Refer Link - {ref_link}</b>\n\n"
                    "<b>Invite & Earn Fast Don't Miss...!!</b>")

        bot.send_message(chat_id=user_id,text=text,parse_mode='HTML') 

    if message.text == buttons['withdraw_btn']:

        if float(balance)<float(min_with):
            bot.send_message(user_id,f"<b>Insufficient Balance : Minimum Required is {min_with} INR For Withdrawals.</b>",parse_mode="HTML",reply_markup=menu_markup())
            return

        back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        back_markup.add(KeyboardButton(buttons['back_btn']))

        bot.send_message(user_id,"Enter Your UPI Payment Address\n\nMust Include '@' in Your UPI ID",reply_markup=back_markup)

        bot.register_next_step_handler(message,process_withdraw_upi)


def process_withdraw_upi(message):

    user_id = message.chat.id
    upi = message.text

    if message.text == buttons['back_btn']:
        bot.send_message(user_id,"❌ withdraw cancelled",reply_markup=menu_markup())
        return

    if not re.match(r'^[\w.-]+@[\w.-]+$', upi):
        bot.send_message(user_id, "Invalid UPI ID. Please enter a valid upi id.",reply_markup=menu_markup())
        return

    back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_markup.add(KeyboardButton(buttons['back_btn']))

    bot.send_message(user_id,"Enter amount for withdraw:",reply_markup=back_markup)

    bot.register_next_step_handler(message,process_withdraw_amo,upi)

def process_withdraw_amo(message,upi):
    user_id = message.chat.id

    userData = db.users.find_one({'user_id':user_id})
    balance = userData.get('balance', 0)


    if message.text == buttons['back_btn']:
        bot.send_message(user_id,"❌ withdraw cancelled",reply_markup=menu_markup())
        return

    if not re.match(r'^\d+(\.\d{1,8})?$', message.text):
            bot.send_message(user_id, "Invalid withdrawal amount. Please enter a valid number.",reply_markup=menu_markup())
            return


    amount = float(message.text)

    if float(min_with) > float(amount):
        bot.send_message(user_id,f"*❌ Minimum Withdraw:* {min_with} *INR*",reply_markup=menu_markup(),parse_mode="markdown")
        return

    if float(balance) < float(amount):
        bot.send_message(user_id,f"*❌ You Have Only Withdrawal Amount Is:*{balance:.7f} *INR*",reply_markup=menu_markup(),parse_mode="markdown")
        return      

    db.users.update_one({'user_id':user_id},{'$inc':{'total_with':amount}},upsert=True)

    db.users.update_one({'user_id':user_id},{'$inc':{'balance':-amount}},upsert=True)

    bot.send_message(user_id,f"Withdraw Processing....")
    send_withdraw(message,amount,upi)

def ref_bons(user_id):
    #### Referral Bonus ####


    userData = db.users.find_one({'user_id':user_id})

    referred_by =  userData.get("ref_by", None) 
    referred = userData.get("referred",None)
    ref_bonus = random.randint(1, 3)


    if referred_by != "none" and referred == None:

        db.users.update_one({'user_id':user_id},{'$set':{'referred':1}},upsert=True)

        db.users.update_one({'user_id':int(referred_by)},{'$inc':{'balance':float(ref_bonus)}},upsert=True)

        bot.send_message(referred_by, f"*➕ {ref_bonus} INR For New Referral*",parse_mode="markdown")

    #### end ####

def send_withdraw(message,amount,upi):
    orderid = str(uuid.uuid4().int)[:10]
    user_id = message.chat.id
    name = message.chat.first_name
    comment = f"@{bot.get_me().username}"

    url = f"https://cashbacktime.in/api/direct/?name={name}&payid={upi}&amount={amount}&comment={comment}&oid={orderid}&pin=62528"

    data = requests.get(url)

    if data.json()['status'] == 'failed':
        bot.send_message(user_id,"Try Again..")
        bot.send_message(admin_chat_id,f"Response: {data.text}\nOrderId: {orderid}")

        db.users.update_one({'user_id':user_id},{'$inc':{'balance':amount}},upsert=True)
        return

    bot.send_message(user_id,f"<b>Withdraw Success!!</b>",parse_mode='html')

    bot.send_message(payment_channel,f"User Id: {message.chat.id}\nUser FirstName: {message.chat.first_name}\nUserName: @{message.chat.username}\nAmount: {amount}\nUPI: {upi}\nResponse: {data.text}\nOrderId: {orderid}")



# bot.polling()

if __name__ == '__main__':
    while True:
        try:
            print("Bot is running")
            bot.polling(non_stop=True)
        except Exception as e:
            print(f"Error occurred: {e}")
            bot.send_message(admin_chat_id, f"*Error occurred in bot polling:*\n\n`{str(e)}`", parse_mode="markdown")
            time.sleep(5)