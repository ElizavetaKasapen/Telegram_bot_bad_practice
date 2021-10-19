from telegram.ext import Updater, CommandHandler,CallbackQueryHandler
import requests
import re
from telegram import ReplyKeyboardMarkup

import sqlite3
import logging

from datetime import datetime
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup,InlineKeyboardButton,PollOption
from datetime import datetime

class Answers: 
    privat_url='https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    all_url='http://resources.finance.ua/ru/public/currency-cash.json'
    def get_url_privat(self):
        self.contents = requests.get(self.privat_url).json() 
        return self.contents
    def get_url_all(self):
        self.contents = requests.get(self.all_url).json() 
        return self.contents
    def toFixed(self,numObj, digits=0):
        return f"{numObj:.{digits}f}"
    #Privat
    def privat_USD(self):
        self.content=self.get_url_privat()
        self.usd=self.content[0]['buy']+'uah    '+ self.content[0]['sale']+'uah \n'
        return self.usd
    def privat_EUR(self):
        self.content=self.get_url_privat()
        self.usd=self.content[1]['buy']+'uah    '+ self.content[1]['sale']+'uah \n'
        return self.usd
    def privat_RU(self):
        self.content=self.get_url_privat()
        self.usd=self.content[2]['buy']+'uah    '+ self.content[2]['sale']+'uah \n'
        return self.usd
    #Alfa
    def alfa_USD(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][6]['currencies']['USD']['bid']
        self.sale=self.content['organizations'][6]['currencies']['USD']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd
    def alfa_EUR(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][6]['currencies']['EUR']['bid']
        self.sale=self.content['organizations'][6]['currencies']['EUR']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    def alfa_RU(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][6]['currencies']['RUB']['bid']
        self.sale=self.content['organizations'][6]['currencies']['RUB']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    #Oshad
    def oshad_USD(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][39]['currencies']['USD']['bid']
        self.sale=self.content['organizations'][39]['currencies']['USD']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd
    def oshad_EUR(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][39]['currencies']['EUR']['bid']
        self.sale=self.content['organizations'][39]['currencies']['EUR']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    def oshad_RU(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][39]['currencies']['RUB']['bid']
        self.sale=self.content['organizations'][39]['currencies']['RUB']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
     #Pumb
    def pumb_USD(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][45]['currencies']['USD']['bid']
        self.sale=self.content['organizations'][45]['currencies']['USD']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd
    def pumb_EUR(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][45]['currencies']['EUR']['bid']
        self.sale=self.content['organizations'][45]['currencies']['EUR']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    def pumb_RU(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][45]['currencies']['RUB']['bid']
        self.sale=self.content['organizations'][45]['currencies']['RUB']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    #agrikol
    def agrikol_USD(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][26]['currencies']['USD']['bid']
        self.sale=self.content['organizations'][26]['currencies']['USD']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd
    def agrikol_EUR(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][26]['currencies']['EUR']['bid']
        self.sale=self.content['organizations'][26]['currencies']['EUR']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 
    def agrikol_RU(self):
        self.content=self.get_url_all()
        self.buy=self.content['organizations'][26]['currencies']['RUB']['bid']
        self.sale=self.content['organizations'][26]['currencies']['RUB']['ask']
        self.usd=self.buy+'uah    '+ self.sale+'uah \n'
        return self.usd 

class DB:
    currencies={'USD':False,'EUR':False,'RUB':False}#список выбранных валют
    banks = {'ПриватБанк':False,'Альфа-Банк':False,'Ощадбанк':False,'ПУМБ':False,'Креді Агріколь':False}
    __connection=None
    def get_connection(self):
        #if self.__connection is None:
        self.__connection=sqlite3.connect('properties.db')
        return self.__connection
    def init_db(self,force:bool=False):
        self.con=self.get_connection()
        self.c=self.con.cursor()
        #user info
        if force:
            self.c.execute('DROP TABLE IF EXISTS account_prop')
        self.c.execute('''CREATE TABLE IF NOT EXISTS account_prop(
             id INTEGER PRIMARY KEY,
             user_id TEXT NOT NULL,
             banks TEXT NOT NULL,
             currencies TEXT NOT NULL,
             language_ TEXT,
             time_ TEXT
             )''')
        self.con.commit()
    def add_user(self,user_id:str,banks:str,currencies:str,language:str='ukr',time:str='9:00'):
        con=self.get_connection()
        c= con.cursor()
        if(not  self.if_this_user_exist(user_id)):
            c.execute('INSERT INTO account_prop(user_id,banks,currencies,language_,time_) VALUES(?,?,?,?,?);',(user_id,banks,currencies,language,time))
        else:
            c.execute("""Update account_prop set banks = ?,currencies=?,language_=?,time_=? where user_id = ?;""",(banks,currencies,language,time,user_id))
        con.commit()
    def select_language(self,user_id):
          con=  self.get_connection()
          c=  con.cursor()
          c.execute('select language_ from account_prop where user_id=?;',(user_id,))
          results =   c.fetchall()
          con.commit()  
          return results[0][0]
    def select_time(self,user_id):
          con=  self.get_connection()
          c=  con.cursor()
          c.execute('select time_ from account_prop where user_id=?;',(user_id,))
          results =   c.fetchall()
          con.commit()  
          return results[0][0]
    def select_banks(self,user_id):
          self.con=  self.get_connection()
          self.c=  self.con.cursor()
          self.c.execute('select banks from account_prop where user_id=?;',(user_id,))
          self.results =   self.c.fetchall()
          self.curr=  self.convert_banks(self.results[0][0])
          self.con.commit()  
          return self.curr
    def select_currencies(self,user_id):
          con=  self.get_connection()
          c=  con.cursor()
          c.execute('select currencies from account_prop where user_id=?;',(user_id,))
          results =   c.fetchall()
          curr= self.convert_currencies(results[0][0])
          con.commit()  
          return curr
    def convert_banks(self,res):
        for b_key, b_value in   self.banks.items():
            if b_key in res:self.banks[b_key]=True
            else: self.banks[b_key]=False
        return   self.banks
    def convert_currencies(self,res):
        for b_key, b_value in   self.currencies.items():
            if b_key in res:
               self.currencies[b_key]=True
            else: self.currencies[b_key]=False
        return   self.currencies
    def select(self):
        self.con=self.get_connection()
        self.c=self.con.cursor()
        self.c.execute('select * from account_prop;')
        results = self.c.fetchall()
        self.con.commit()
    # true if exsist
    def if_this_user_exist(self,user_id:str):
        self.con=self.get_connection()
        self.c=self.con.cursor()
        self.c.execute('SELECT * FROM account_prop WHERE user_id = ?;',(user_id,))
        results = self.c.fetchall()
        if(len(results)==0):res= False
        else:res= True
        self.con.commit()
        return res

    def bank_statistics(self):
          bank_statistics= {'ПриватБанк':0,'Альфа-Банк':0,'Ощадбанк':0,'ПУМБ':0,'Креді Агріколь':0}
          self.con=  self.get_connection()
          self.c=  self.con.cursor()
          self.c.execute("select * from account_prop ;")
          res=self.c.fetchall()
          for key,value in bank_statistics.items():
            like='%'+key+'%'
            self.c.execute("select count(*) from account_prop where banks like ?;",(like,))
            res=self.c.fetchall()
            bank_statistics[key] =  res[0][0]
          self.con.commit()  
          return bank_statistics

    def time_statistics(self):
          bank_statistics= {'9:00':0,'15:00':0,'21:00':0}
          self.con=  self.get_connection()
          self.c=  self.con.cursor()
          self.c.execute("select * from account_prop ;")
          res=self.c.fetchall()
          for key,value in bank_statistics.items():
            like='%'+key+'%'
            self.c.execute("select count(*) from account_prop where time_ like ?;",(like,))
            res=self.c.fetchall()
            bank_statistics[key] =  res[0][0]
          self.con.commit()  
          return bank_statistics
    def currencies_statistics(self):
          currencies_statistics={'USD':0,'EUR':0,'RUB':0}
          self.con=  self.get_connection()
          self.c=  self.con.cursor()
          self.c.execute("select * from account_prop ;")
          res=self.c.fetchall()
          for key,value in currencies_statistics.items():
            like='%'+key+'%'
            self.c.execute("select count(*) from account_prop where currencies like ?;",(like,))
            res=self.c.fetchall()
            currencies_statistics[key] =  res[0][0]
          self.con.commit()  
          return currencies_statistics
    def select_all_users_id(self):
        self.con=  self.get_connection()
        self.c=  self.con.cursor()
        self.c.execute("select user_id from account_prop ;")
        res=self.c.fetchall()
        self.con.commit()  
        return res
class Keyboards: 
    banks = ['privat','alfa','oshad','pumb','agrikol']
    def language_board(self):
        self.keyboard = [[InlineKeyboardButton("Українська", callback_data='ukr'),
                 InlineKeyboardButton("Російська", callback_data='rus')]]
        return self.keyboard
    def save_board(self):
        self.keyboard = [[InlineKeyboardButton("✔", callback_data='save')]]
        return self.keyboard
    def currency_board(self,curr):
        txt1="USD" if  not curr["USD"] else "USD✔"
        txt2="EUR" if  not curr["EUR"] else "EUR✔"
        txt3="RUB" if not curr["RUB"] else "RUB✔"
        self.keyboard = [[InlineKeyboardButton(txt1, callback_data='USD'),
                 InlineKeyboardButton(txt2, callback_data='EUR'),
                 InlineKeyboardButton(txt3, callback_data='RUB')],[InlineKeyboardButton('✔', callback_data='done_curr')]]
        return self.keyboard
    def banks_board(self,banks):
        txt0="ПриватБанк✔" if  banks["ПриватБанк"] else "ПриватБанк"
        txt1="Альфа-Банк✔" if  banks["Альфа-Банк"] else "Альфа-Банк"
        txt2="Ощадбанк✔" if  banks["Ощадбанк"] else "Ощадбанк"
        txt3="ПУМБ✔" if  banks["ПУМБ"] else "ПУМБ"
        txt4="Креді Агріколь✔" if  banks["Креді Агріколь"] else "Креді Агріколь"

        self.keyboard = [[InlineKeyboardButton(txt0, callback_data='ПриватБанк')],
                 [InlineKeyboardButton(txt1, callback_data='Альфа-Банк')],
                 [InlineKeyboardButton(txt2, callback_data='Ощадбанк')],
                 [InlineKeyboardButton(txt3, callback_data='ПУМБ')],
                 [InlineKeyboardButton(txt4, callback_data='Креді Агріколь')],
                 [InlineKeyboardButton('✔', callback_data='done_banks')]]
        return self.keyboard
    def time_board(self):
        self.keyboard = [[InlineKeyboardButton('9:00', callback_data='9:00')],
                 [InlineKeyboardButton('15:00', callback_data='15:00')],
                 [InlineKeyboardButton('21:00', callback_data='21:00')]]
        return self.keyboard
   


from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup,InlineKeyboardButton

db_=DB()

answ = Answers()

class Handlers: 
    def choose_language(self,choose_language):
        if choose_language=='ukr': 
            properties.set_language('ukr')
            return "Ви обрали українську мову"
        if choose_language=='rus': 
            properties.set_language('rus')
            return "Вы выбрали русский язык"
    def choose_currency(self,choose_currency):
        txt='Ви обрали такі валюти:\n'
        for key, value in choose_currency.items():
            if value==True:txt+=key+"\n"
        return txt
    def choose_banks(self,choose_banks):
        txt='Ви обрали такі банки:\n'
        for key, value in choose_banks.items():
            if value:txt+=key+"\n"
        return txt
    def choose_output(self,bank,currency,id):
        out=''
        if db_.select_language(id)=='ukr':out+="Купівля             Продаж\n" 
        if db_.select_language(id)=='rus':out+="Купля               Продажа\n" 
        if bank=='ПриватБанк':
            for key, value in currency.items():
                if value and key=='USD': out+='USD\n'+answ.privat_USD()
                if value and key=='EUR': out+='EUR\n'+answ.privat_EUR()
                if value and key=='RUB': out+='RUB\n'+answ.privat_RU()
        if bank=='Альфа-Банк':
            for key, value in currency.items():
                if value and key=='USD': out+='USD\n'+answ.alfa_USD()
                if value and key=='EUR': out+='EUR\n'+answ.alfa_EUR()
                if value and key=='RUB': out+='RUB\n'+answ.alfa_RU()
        if bank=='Ощадбанк':
            for key, value in currency.items():
                if value and key=='USD': out+='USD\n'+answ.oshad_USD()
                if value and key=='EUR': out+='EUR\n'+answ.oshad_EUR()
                if value and key=='RUB': out+='RUB\n'+answ.oshad_RU()       
        if bank=='ПУМБ':
            for key, value in currency.items():
                if value and key=='USD': out+='USD\n'+answ.pumb_USD()
                if value and key=='EUR': out+='EUR\n'+answ.pumb_EUR()
                if value and key=='RUB': out+='RUB\n'+answ.pumb_RU()          
        if bank=='Креді Агріколь':
            for key, value in currency.items():
                if value and key=='USD': out+='USD\n'+answ.agrikol_USD()
                if value and key=='EUR': out+='EUR\n'+answ.agrikol_EUR()
                if value and key=='RUB': out+='RUB\n'+answ.agrikol_RU()
        return out

class Commands: 
    currencies={'USD':False,'EUR':False,'RUB':False}#список выбранных валют
    banks = {'ПриватБанк':False,'Альфа-Банк':False,'Ощадбанк':False,'ПУМБ':False,'Креді Агріколь':False}
    
    def banks_statistics(self,update, context):
        self.bank=db_.bank_statistics()
        self.out=''
        self.user=''
        if db_.select_language(properties.get_adm())=='ukr':self.user+=" користувачів\n" 
        if db_.select_language(properties.get_adm())=='rus':self.user+=" пользователей\n" 
        for key,value in self.bank.items():
            self.out+=key+": "+str(value)+self.user
        context.bot.send_message(chat_id=update.message.chat_id, text=self.out)
    def start(self,update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="""Вітаю!\nБудь ласка, перед початком роботи оберіть комфортні для вас налаштування.
Обов'язково оберить валюти і банки!
Після цього надішліть команду /save_information.
Приємного користування!""")
        curr_markup = InlineKeyboardMarkup(boards.currency_board(self.currencies))
        update.message.reply_text('Оберіть валюту/валюти:', reply_markup=curr_markup)
        banks_markup = InlineKeyboardMarkup(boards.banks_board(self.banks))
        update.message.reply_text('Оберіть банк(и):', reply_markup=banks_markup)
        time_markup = InlineKeyboardMarkup(boards.time_board())
        update.message.reply_text('Оберіть час для відправлення повідомлення:', reply_markup=time_markup)
        language_markup = InlineKeyboardMarkup(boards.language_board())
        update.message.reply_text('Оберіть мову:', reply_markup=language_markup)
 
    def save(self,update, context):
        id_ = str(update.message.from_user.id)
        ban=srt_db.srt_for_curr(properties.get_bank())
        cur=srt_db.srt_for_curr(properties.get_currency())
        lang=properties.get_language()
        tim=properties.get_time()
        logging.info("Saving person with "+id_+" ID")
        db_.add_user(id_,ban,cur,lang,tim)
        context.bot.send_message(chat_id=update.message.chat_id, text="Ok!😄")
    def get_currencies(self,update, context):
        txt=''
        banks_=db_.select_banks(update.message.from_user.id)
        currencies_=db_.select_currencies(update.message.from_user.id)
        for b_key, b_value in banks_.items():
            if b_value:
                txt+="\n"+b_key+"\n"
                txt+=handler.choose_output(b_key,currencies_,update.message.from_user.id)
        context.bot.send_message(chat_id=update.message.chat_id, text=txt)
        logging.info(txt)
    def button(self,update, context):
        query = update.callback_query
        if query.data=='ukr'or query.data=='rus': 
            answ = handler.choose_language(query.data)
            properties.set_language(query.data)
            query.edit_message_text(text=answ)
        if query.data=='USD':
            self.currencies['USD']=not self.currencies['USD']
            self.change_buttons_curr(update,self.currencies)
        if query.data=='EUR':
            self.currencies['EUR']=not self.currencies['EUR']
            self.change_buttons_curr(update,self.currencies)
        if query.data=='RUB':
            self.currencies['RUB']=not self.currencies['RUB']
            self.change_buttons_curr(update,self.currencies)
        if query.data=='done_curr':
            answ=handler.choose_currency(self.currencies)
            query.edit_message_text(text=answ)
            properties.set_currency(self.currencies)
        if query.data=='ПриватБанк':
            self.banks['ПриватБанк']=not self.banks['ПриватБанк']
            self.change_buttons_banks(update,self.banks)
        if query.data=='Альфа-Банк':
            self.banks['Альфа-Банк']=not self.banks['Альфа-Банк']
            self.change_buttons_banks(update,self.banks)
        if query.data=='Ощадбанк':
            self.banks['Ощадбанк']=not self.banks['Ощадбанк']
            self.change_buttons_banks(update,self.banks)
        if query.data=='Креді Агріколь':
            self.banks['Креді Агріколь']=not self.banks['Креді Агріколь']
            self.change_buttons_banks(update,self.banks)
        if query.data=='ПУМБ':
            self.banks['ПУМБ']=not self.banks['ПУМБ']
            self.change_buttons_banks(update,self.banks)
        if query.data=='done_banks':
            answ=handler.choose_banks(self.banks)
            properties.set_bank(self.banks)
            query.edit_message_text(text=answ)  
        if query.data=='9:00':
            properties.set_time('9:00')
            query.edit_message_text(text="Повідомлення буде надсилатись щодня о 9:00")  
        if query.data=='15:00':
            properties.set_time('15:00')
            query.edit_message_text(text="Повідомлення буде надсилатись щодня о 15:00")  
        if query.data=='21:00':
            properties.set_time('21:00')
            query.edit_message_text(text="Повідомлення буде надсилатись щодня о 21:00") 

            
    def change_buttons_curr(self,update,curr):
        query = update.callback_query
        curr_markup = InlineKeyboardMarkup(boards.currency_board(curr))
        query.edit_message_text('Оберіть валюту/валюти:', reply_markup=curr_markup)
    def change_buttons_banks(self,update,banks):
        query = update.callback_query
        banks_markup = InlineKeyboardMarkup(boards.banks_board(banks))
        query.edit_message_text('Оберіть банк(и):', reply_markup=banks_markup)
    def help(self,update, context):
        out=''
        id_=update.message.from_user.id
        if db_.select_language(properties.get_adm())=='ukr':
            self.out+="""Вітаю у розділі "допомога"!
Для того, щоб користуватись ботом, Вам необхідно:
1. Пройти стартову реєстрацію (/start), де ОБОВ'ЯЗКОВО вказати банки та валюти про які Ви хочете отримувати інформацію.
   Якщо Ви не оберете час та мову, система зробить це за Вас. За замовчуванням: українська мова та час відправлення о 9:00.
2. Після реєстрації ОБОВ'ЯЗКОВО викличе команду /save_information, щоб система Вас запам'ятала та виводила необхідну Вам інформацію.
Для отримання інформації щодо поточного курсу валют введіть команду /get_currencies.
Щоб відправити повідомлення адміністратору введіть команду /message_to_administrator та в цьому ж повідомленні напишіть своє питання або повідомлення про помилку.
Приємного користування!""" 
            if id_==properties.get_adm():
                self.out+="""Оскільки Ви адміністратор цього боту, для Вас є окремі команди:
/banks_statistics - виведення статистики про кількість користувачів, які обрали доступні банки
/time_statistics - виведення статистики про кількість користувачів, які обрали доступний час для відправлення повідомлень
/currencies_statistics - виведення статистики про кількість користувачів, які обрали доступні курси валют
/message_to_users - відправлення повідомлення всім користувачам (напишіть ваше повідомлення в одному повідомленні з командою)"""
        if db_.select_language(properties.get_adm())=='rus':
            self.out+="""Приветствую в разделе "помощь"!
Чтобы пользоваться ботом, Вам необходимо:
1. Пройти стартовую регистрации (/start), где ОБЯЗАТЕЛЬНО указать банки и валюты о которых Вы хотите получать информацию.
   Если не выбраны время и язык, система сделает это за Вас. По умолчанию: украинский язык и время отправления в 9:00.
2. После регистрации ОБЯЗАТЕЛЬНО вызовете команду /save_information, чтобы система Вас запомнила и выводила необходимую Вам информацию.
Для получения информации о текущем курсе валют введите команду /get_currencies.
Чтобы отправить сообщение администратору введите команду /message_to_administrator и в этом же сообщении напишите свой вопрос или сообщение об ошибке.
Приятного использования! """
        if id_==properties.get_adm():
            self.out+= """Поскольку Вы администратор этого бота, для Вас есть отдельные команды:
/banks_statistics - вывод статистики о количестве пользователей, которые доступны банки
/time_statistics - вывод статистики о количестве пользователей, которые доступное время для отправки сообщений
/currencies_statistics - вывод статистики о количестве пользователей, которые доступны курсы валют
/message_to_users - отправка сообщения всем пользователям (напишите ваше сообщение в одном сообщении с командой) """
        context.bot.send_message(chat_id=update.message.chat_id, text=out)

class Account_properties:
    def get_adm (self): 
        return self.adm
    def set_adm(self, adm): 
        self.adm = adm
    #Выбор языка
    def get_language (self): 
        return self.language
    def set_language(self, language): 
        self.language = language 
    #Выбор банка 
    def get_bank(self): 
        return self.bank
    def set_bank(self, bank): 
        self.bank = bank
    #Выбор валют 
    def get_currency(self): 
        return self.currency
    def set_currency(self, currency): 
        self.currency = currency 
    #Выбор времени 
    def get_time(self): 
        return self.time
    def set_time(self, time): 
        self.time = time 

class Str_for_DB:
    def srt_for_banks(self,banks):
        txt=''
        for b_key, b_value in banks.items():
            if b_value==True:
                txt+=b_key+" "
        return txt
    def srt_for_curr(self,curr):
        txt=''
        for b_key, b_value in curr.items():
            if b_value==True:
                txt+=b_key+" "
        return txt

handler=Handlers()
properties=Account_properties()
boards = Keyboards()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot_activity.log')
global admin_id 
admin_id ='344587463'
com = Commands()
updater = Updater('1120461749:AAF_gXcuweGZFpUJ_SdFQesGUxwWcZu0O-M',use_context=True)

srt_db=Str_for_DB()

##########################################
def get_connection():
        __connection=sqlite3.connect('properties.db')
        return __connection

def msg_to_adm(update, context):
        username=update.message.from_user.username
        id_=update.message.from_user.id
        out=''
        if username==None: out+='\nUser id:'+str(id_)
        else:out+='\nUser name: @'+str(username)
        text = update.message.text  #ПОЛУЧИТЬ СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯ
        context.bot.send_message(chat_id=properties.get_adm(), text=text+out)
        logging.info('Msg to adm:'+text+out)
def get_user_id(update):                                                        
        id_=update.message.from_user.id
        return id_
##########################################

def banks_statistics(update, context):
        bank=db_.bank_statistics()
        out=''
        user=''
        if db_.select_language(properties.get_adm())=='ukr':user+=" користувачів\n" 
        if db_.select_language(properties.get_adm())=='rus':user+=" пользователей\n" 
        for key,value in bank.items():
            out+=key+": "+str(value)+user
        context.bot.send_message(chat_id=update.message.chat_id, text=out)
        logging.info('banks statistics:'+out)
def time_statistics(update, context):
        bank=db_.time_statistics()
        out=''
        user=''
        if db_.select_language(properties.get_adm())=='ukr':user+=" користувачів\n" 
        if db_.select_language(properties.get_adm())=='rus':user+=" пользователей\n" 
        for key,value in bank.items():
            out+=key+": "+str(value)+user
        context.bot.send_message(chat_id=update.message.chat_id, text=out)
        logging.info('time statistics:'+out)
def currencies_statistics(update, context):
        bank=db_.currencies_statistics()
        out=''
        user=''
        if db_.select_language(properties.get_adm())=='ukr':user+=" користувачів\n" 
        if db_.select_language(properties.get_adm())=='rus':user+=" пользователей\n" 
        for key,value in bank.items():
            out+=key+": "+str(value)+user
        context.bot.send_message(chat_id=update.message.chat_id, text=out)  
        logging.info('currencies statistics:'+out)     
def help(update, context):
    out=''
    id_=update.message.from_user.id
    if db_.select_language(properties.get_adm())=='ukr':
            out+="""Вітаю у розділі "допомога"!
Для того, щоб користуватись ботом, Вам необхідно:
1. Пройти стартову реєстрацію (/start), де ОБОВ'ЯЗКОВО вказати банки та валюти про які Ви хочете отримувати інформацію.
   Якщо Ви не оберете час та мову, система зробить це за Вас. За замовчуванням: українська мова та час відправлення о 9:00.
2. Після реєстрації ОБОВ'ЯЗКОВО викличе команду /save_information, щоб система Вас запам'ятала та виводила необхідну Вам інформацію.
Для отримання інформації щодо поточного курсу валют введіть команду /get_currencies.
Щоб відправити повідомлення адміністратору введіть команду /message_to_administrator та в цьому ж повідомленні напишіть своє питання або повідомлення про помилку.
\n""" 
            if str(id_)==properties.get_adm():
                out+="""Оскільки Ви адміністратор цього боту, для Вас є окремі команди:
/banks_statistics - виведення статистики про кількість користувачів, які обрали доступні банки
/time_statistics - виведення статистики про кількість користувачів, які обрали доступний час для відправлення повідомлень
/currencies_statistics - виведення статистики про кількість користувачів, які обрали доступні курси валют
/message_to_users - відправлення повідомлення всім користувачам (напишіть ваше повідомлення в одному повідомленні з командою)"""
    if db_.select_language(properties.get_adm())=='rus':
        out+="""Приветствую в разделе "помощь"!
Чтобы пользоваться ботом, Вам необходимо:
1. Пройти стартовую регистрацию (/start), где ОБЯЗАТЕЛЬНО указать банки и валюты о которых Вы хотите получать информацию.
   Если не выбраны время и язык, система сделает это за Вас. По умолчанию: украинский язык и время отправления в 9:00.
2. После регистрации ОБЯЗАТЕЛЬНО вызовете команду /save_information, чтобы система Вас запомнила и выводила необходимую Вам информацию.
Для получения информации о текущем курсе валют введите команду /get_currencies.
Чтобы отправить сообщение администратору введите команду /message_to_administrator и в этом же сообщении напишите свой вопрос или сообщение об ошибке.
\n"""
        if str(id_)==properties.get_adm():
            out+= """Поскольку Вы администратор этого бота, для Вас есть отдельные команды:
/banks_statistics - вывод статистики о количестве пользователей, которые выбрали доступные банки
/time_statistics - вывод статистики о количестве пользователей, которые выбрали доступное время для отправки сообщений
/currencies_statistics - вывод статистики о количестве пользователей, которые выбрали доступные курсы валют
/message_to_users - отправка сообщения всем пользователям (напишите Ваше сообщение в одном сообщении с командой) """
    context.bot.send_message(chat_id=update.message.chat_id, text=out)
def message_to_users(update, context):
    users=db_.select_all_users_id()
    text = update.message.text  #ПОЛУЧИТЬ СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯ
    txt=text.split(' ', maxsplit=1)
    for val in users:
        itm=val[0]
        context.bot.send_message(chat_id=itm, text=txt[1])
    logging.info('Msg to users:'+txt[1])


def main():
    logging.info('Start bot')
    properties.set_adm(admin_id)
    db_.select()
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',com.start))
    dp.add_handler(CommandHandler('save_information',com.save))
    dp.add_handler(CommandHandler('get_currencies',com.get_currencies))
    dp.add_handler(CommandHandler('message_to_administrator',msg_to_adm))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('id',get_user_id))
    #if get_user_id(dp)==properties.get_adm():
    dp.add_handler(CommandHandler('banks_statistics',banks_statistics))
    dp.add_handler(CommandHandler('time_statistics',time_statistics))
    dp.add_handler(CommandHandler('currencies_statistics',currencies_statistics))
    dp.add_handler(CommandHandler('message_to_users',message_to_users))
    dp.add_handler(CallbackQueryHandler(com.button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    db_.init_db()
    main()

