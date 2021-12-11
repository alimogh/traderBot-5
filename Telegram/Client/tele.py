""""
Mr.Kataei 11/23/2021

"""
from time import sleep
from telebot import types
from telebot import apihelper
from Auth.register import register
from Inc import functions
from Account.clients import User, BitfinexClient, DemoClient
from Interfaces.telegram import Telegram
import numpy as np
from Conf import analysis_settings
from Analysis.emerald import Emerald
from Analysis.diamond import Diamond
from Analysis.ruby import Ruby
from Libraries.data_collector import get_candle_binance as candles
from Test.strategy_tester import StrategyTaster
from binance import Client
Client(api_key='',api_secret='').get_klines()

apihelper.ENABLE_MIDDLEWARE = True

# @testkourosh2bot -> address // use this bot for test your code
API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

timeframe_binance_dictionary = {
    '30min': ['30m', 1],
    '1hour': ['1h', 2],
    '4hour': ['4h', 3],
    '1day': ['1d', 4],
    '1min': ['1m', 5],
}


def get_analysis_class(analysis: str, symbol: str, timeframe_id: int, timeframe: str):
    coin_id = functions.get_coin_id(symbol)
    if analysis == 'emerald':
        data = candles(symbol=symbol, timeframe=timeframe, limit=400)
        if data[0]:
            return Emerald(data=data[1], coin_id=coin_id, timeframe_id=timeframe_id, bot_ins=1).get_recommendations()
        else:
            return None
    if analysis == 'diamond':
        setting = analysis_settings.get_analysis_setting(coin_id=coin_id, timeframe_id=timeframe_id, analysis_id=3)
        if setting:
            data = candles(symbol=symbol, timeframe=timeframe, limit=400)
            if data[0]:
                return Diamond(data=data[1], coin_id=coin_id, timeframe_id=timeframe_id,
                               bot_ins=1, setting=setting).get_recommendations()
            else:
                return None
        else:
            return None

    if analysis == 'ruby':
        setting = analysis_settings.get_analysis_setting(coin_id=coin_id, timeframe_id=timeframe_id, analysis_id=2)
        if setting:
            data = candles(symbol=symbol, timeframe=timeframe, limit=400)
            if data[0]:
                return Ruby(data=data[1], coin_id=coin_id, timeframe_id=timeframe_id,
                            bot_ins=1, setting=setting).get_recommendations()
            else:
                return None
        else:
            return None


def get_exchange_class(exchange_id: int, public: str, secret: str, chat_id: str = None):
    if exchange_id == 1:
        return BitfinexClient(public=public, secret=secret)
    elif exchange_id == 2:
        return DemoClient(chat_id=chat_id)
    else:
        return None


def start_keyboard():
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_add_account = types.KeyboardButton('🏛 add exchange')
    key_add_strategy = types.KeyboardButton('📊 add strategy')
    key_tutorials = types.KeyboardButton('📚 tutorials')
    key_plans = types.KeyboardButton('💳 plans')
    key_profile = types.KeyboardButton('🙍🏻‍♂️profile')
    key_back_test = types.KeyboardButton('🧭 back test')
    key_social = types.KeyboardButton('📬 social media')
    key_help = types.KeyboardButton('🤔 help')
    key_markup.add(key_add_account, key_add_strategy, key_tutorials,
                   key_plans, key_profile, key_back_test, key_social, key_help)
    return key_markup


def analysis_keyboard():
    """
    :return:
    """
    analysis = np.array(functions.get_analysis())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*analysis[:, 1])
    return key_markup


def coins_keyboard():
    """
    :return:
    """
    coins = np.array(functions.get_coins())
    key_markup = types.ReplyKeyboardMarkup(row_width=3)
    key_markup.add(*coins[:, 1])
    return key_markup


def tut_cat_keyboard():
    """
    :return:
    """
    categories = np.array(functions.get_tutorials_categories())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*categories[:, 1])
    return key_markup


def back_home_tut():
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add('categories', 'back home')
    return key_markup


def tut_medias_keyboard(category: str):
    """
    :return:
    """
    medias = np.array(functions.get_tutorials_with_category(category=category))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keys = []
    for media in medias:
        keys.append(types.InlineKeyboardButton(text=media[0], url=media[1]))
    keyboard.add(*keys)
    return keyboard


def social_keyboard():
    """
    :return:
    """
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text='instagram', url='instagram.com'),
                 types.InlineKeyboardButton(text='telegram', url='telegram.com'),
                 types.InlineKeyboardButton(text='twitter', url='twitter.com'),
                 types.InlineKeyboardButton(text='linkedin', url='linkedin.com'), )
    return keyboard


def timeframe_keyboard():
    """
    :return:
    """
    timeframes = np.array(functions.get_timeframes())
    key_markup = types.ReplyKeyboardMarkup(row_width=3)
    key_markup.add(*timeframes[:, 1])
    return key_markup


def user_exchanges_account_keyboard(message):
    """
    :return:
    """
    exchanges = functions.get_user_exchanges(message.chat.id)
    if exchanges:
        exchanges = np.array(exchanges)
        key_markup = types.ReplyKeyboardMarkup(row_width=1)
        key_markup.add(*exchanges[:, 0])
        return key_markup
    else:
        return False


def exchanges_keyboard():
    """
    :return:
    """
    exchanges = np.array(functions.get_exchanges())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*exchanges[:, 1])
    return key_markup


def generate_profile_show_message(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    plan, valid = functions.get_user_plan_profile(chat_id=chat_id)
    strategies = functions.get_user_exchanges_strategies_profile(chat_id=chat_id)
    accounts = functions.get_user_exchange(chat_id=chat_id)
    accounts_dict = "\n\n"
    strategies_dict = "\n\n"
    for i, strategy in enumerate(strategies, 1):
        strategies_dict += f"{i}-\n 🪙Coin : {strategy[0]}\n📊Analysis: {strategy[1]}\n" \
                           f"💰Amount: {strategy[2]}\n🏛Exchange: {strategy[3]}\n\n"

    for account in accounts:
        accounts_dict += f"🔹 {account[0]}"

    return plan, valid, strategies_dict, accounts_dict


class ClientBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)
        self.exchanges = np.array(functions.get_exchanges())
        self.coins = np.array(functions.get_coins())
        self.analysis = np.array(functions.get_analysis())
        self.timeframes = np.array(functions.get_timeframes())
        self.tut_cat = np.array(functions.get_tutorials_categories())

    def is_valid_user(self, message):
        user = functions.get_user(message.chat.id)
        if not user:
            self.bot.send_message(message.chat.id, 'Sorry\n 😥You should signup')
            return False
        else:
            result = functions.check_expire_plan(chat_id=message.chat.id)
            if result:
                self.bot.send_message(message.chat.id, 'Your plan is expire!😪\n'
                                                       'Recharge your plan please.')
                return False
            else:
                return True

    def can_start_bot(self, message):
        if message.chat.id in self.user_dict:
            return False
        else:
            self.bot.send_message(message.chat.id, '⚠️ Please /start Bot')
            return True

    def is_valid_command(self, message):
        if not self.can_start_bot(message=message) and self.is_valid_user(message=message):
            return True
        else:
            return False

    def check_add_command(self, message):
        if message.text == '📊 add strategy':
            if self.is_valid_command(message=message):
                user = self.user_dict[message.chat.id]
                user.update_user_plan_limit()
                if user.strategy > len(functions.get_user_watchlist(username=user.username)):
                    return True
                else:
                    self.bot.send_message(message.chat.id, '❌ Your strategies is full\n'
                                                           '🤓 Upgrade your plan or edit it in your profile')
                    return False
            else:
                return False
        else:
            return False

    def check_setup_command(self, message):
        if message.text == '🏛 add exchange':
            if self.is_valid_command(message=message):
                user = self.user_dict[message.chat.id]
                user.update_user_plan_limit()
                if user.account > len(functions.get_user_exchange(chat_id=message.chat.id)):
                    return True
                else:
                    self.bot.send_message(message.chat.id, '❌ Your exchange accounts is full\n'
                                                           '🤓 Upgrade your plan or edit it in your profile')
                    return False
            else:
                return False
        else:
            return False

    def tutorial_command(self, message):
        if message.text == '📚 tutorials':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def profile_command(self, message):
        if message.text == '🙍🏻‍♂️profile':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def back_test_command(self, message):
        if message.text == '🧭 back test':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def plan_command(self, message):
        if message.text == '💳 plans':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def bot_actions(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):

            if call.data == "profile_edit_strategies":
                strategies = functions.get_user_exchanges_strategies_profile(chat_id=call.message.chat.id)
                for strategy in strategies:
                    strategies_option = types.InlineKeyboardMarkup(row_width=2)
                    strategies_option.add(types.InlineKeyboardButton('edit',
                                                                     callback_data=str(strategy[4]) +
                                                                                   "_edit_strategy"),
                                          types.InlineKeyboardButton('delete',
                                                                     callback_data=str(strategy[4]) +
                                                                                   "_delete_strategy")
                                          )
                    self.bot.send_message(chat_id=call.message.chat.id, text=f'🪙Coin : {strategy[0]}\n'
                                                                             f'📊Analysis: {strategy[1]}\n'
                                                                             f'💰Amount: {strategy[2]}\n'
                                                                             f'🏛Exchange: {strategy[3]}\n',
                                          reply_markup=strategies_option)

            elif call.data == "profile_edit_exchanges":
                accounts = functions.get_user_exchange(chat_id=call.message.chat.id)

                for account in accounts:
                    # for show asset each exchange
                    public, secret = functions.get_user_api(int(account[1]))
                    exchange_client = get_exchange_class(exchange_id=int(account[2]), public=public, secret=secret,
                                                         chat_id=call.message.chat.id)
                    result_message = '💰Your assets:\n'
                    if exchange_client is not None:
                        assets = exchange_client.get_assets()
                        if assets is not None:
                            for asset in assets:
                                result_message += f'🪙 {asset[1]}\n 💎 {str(asset[2])}\n'

                    accounts_option = types.InlineKeyboardMarkup(row_width=1)
                    accounts_option.add(types.InlineKeyboardButton('edit',
                                                                   callback_data=str(account[1]) +
                                                                                 "_edit_account"))
                    self.bot.send_message(chat_id=call.message.chat.id, text=f"🔹 {account[0]}\n{result_message}",
                                          reply_markup=accounts_option)

            elif call.data == "profile_show_history":
                histories = functions.get_user_trade_history(chat_id=call.message.chat.id)
                result_message = '🔹Your last 10 trade history\n\n'
                for history in histories:
                    result_message += f'🔹Date: {history[0]}\n 🏛Exchange: {history[1]}\n ' \
                                      f'📊Analysis: {history[2]}\n🪙Coin: {history[3]}\n' \
                                      f'💵Price: {history[4]}\n' \
                                      f'🔑Position: {history[5]}\n' \
                                      f'☢️Order status: {history[6]}\n' \
                                      f'☢️Status: {history[7]}\n' \
                                      f'💰 Amount: {history[8]}% of asset\n' \
                                      f'⏰Submit order time: {history[9]}\n' \
                                      f'⏰Signal receive time: {history[10]}\n\n'

                self.bot.send_message(chat_id=call.message.chat.id, text=result_message,
                                      reply_markup=start_keyboard())

            elif "_delete_strategy" in call.data:
                query = str(call.data).split('_')
                functions.delete_strategy(strategy_id=int(query[0]))
                self.bot.send_message(chat_id=call.message.chat.id, text='✅ Done',
                                      reply_markup=start_keyboard())

            elif "_edit_strategy" in call.data:
                query = str(call.data).split('_')
                add_strategy(message=call.message, watchlist_id=int(query[0]))

            elif "_edit_account" in call.data:
                query = str(call.data).split('_')
                add_exchange(message=call.message, user_setting_id=int(query[0]))

            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        @self.bot.message_handler(commands=['start'], func=self.can_start_bot)
        def welcome(message):
            user = functions.get_user(message.chat.id)
            markup = start_keyboard()
            self.user_dict[message.chat.id] = User(chat_id=message.chat.id)  # create object for register user session
            if not user:
                # is typing bot ..
                self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                sleep(1)

                self.bot.send_message(message.chat.id, '🙋🏽‍♂️ Hey ' + message.chat.first_name + "!\n" +
                                      'I am AI Trader, your trade assistance\n /help to show what can i do for you😎',
                                      reply_markup=markup)
                # if user deleted telegram account need develop
                keyboard = types.ReplyKeyboardMarkup()
                reg_button = types.KeyboardButton(text="📞 Share your phone number", request_contact=True)
                keyboard.add(reg_button)
                self.bot.send_message(message.chat.id, "You should sign up with your phone number 🙄",
                                      reply_markup=keyboard)
            else:
                self.user_dict[message.chat.id].username = user[0][0]
                if self.is_valid_user(message=message):
                    functions.update_user_online(username=user[0][0], online=True)
                    self.bot.send_message(message.chat.id, '🤓 How can i help you', reply_markup=markup)

        @self.bot.message_handler(content_types=['contact'],
                                  func=lambda message: functions.is_user_signup(message.chat.id))
        def register_handler(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            self.bot.send_message(message.chat.id, '🙍🏻‍♂️ Please enter your username', reply_markup=markup)
            self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                phone=message.contact.phone_number)

        def reg_step_1(message, phone: str):
            user = self.user_dict[message.chat.id]
            username = str(message.text).lower()
            try:
                if message.content_type != 'text':
                    self.bot.send_message(message.chat.id, '⛔️ Invalid username!\nTry again!')
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)
                if functions.check_username_exist(username=username):
                    self.bot.send_message(message.chat.id, '⛔️ Username already exist!\nTry again!')
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)
                else:
                    user.username = username
                    error, detail = register(username=username, chat_id=user.chat_id, phone=phone)
                    if error:
                        self.bot.reply_to(message, '⛔️ Try again')
                    else:
                        functions.update_user_online(username=user.username, online=True)
                        markup = start_keyboard()
                        self.bot.send_message(message.chat.id, '🥳 Welcome!\n'
                                                               'Your account created!\n'
                                                               '⚠️ Free plan is available for 30 day\n'
                                                               'Enjoy!', reply_markup=markup)
            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)

        @self.bot.message_handler(func=self.check_setup_command)
        def add_exchange(message, user_setting_id: int = 0):
            try:
                key_markup = exchanges_keyboard()
                self.bot.send_message(message.chat.id, '🏛  Please Select your exchange account',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1,
                                                    user_setting_id=user_setting_id)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def add_exchange_step_1(message, user_setting_id: int):
            if message.text == 'demo':
                user = self.user_dict[message.chat.id]
                markup = start_keyboard()
                if user_setting_id == 0:
                    error, result = functions.set_user_setting(username=str(user.username),
                                                               exchange_id=2,
                                                               public='public', secret='secret')
                    functions.create_demo_account(str(user.username))
                    if error:
                        self.bot.send_message(message.chat.id, '😥 You already have demo', reply_markup=markup)
                    else:
                        self.bot.send_message(message.chat.id, 'your exchange demo account successfully created\n'
                                                               'and you can watch your assets in your profile',
                                              reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, '✅ success',
                                          reply_markup=markup)

            else:
                try:
                    exchanges_id = np.where(self.exchanges[:, 1] == message.text)[0][0]
                    key_markup = types.ReplyKeyboardRemove(selective=False)
                    self.bot.send_message(message.chat.id, '🔐 Enter your public API', reply_markup=key_markup)
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                        exchange_id=self.exchanges[exchanges_id][0],
                                                        user_setting_id=user_setting_id)
                except IndexError:
                    self.bot.send_message(message.chat.id, '⛔️ wrong exchange')
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1,
                                                        user_setting_id=user_setting_id)

        def add_exchange_step_2(message, exchange_id: int, user_setting_id: int):
            if message.content_type == 'text':
                self.bot.send_message(message.chat.id, '🔐 Enter your secret API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=message.text,
                                                    user_setting_id=user_setting_id)
                self.bot.delete_message(message.chat.id, message.message_id)
            else:
                self.bot.send_message(message.chat.id, '⛔️ wrong API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                    exchange_id=exchange_id,
                                                    user_setting_id=user_setting_id)

        def add_exchange_step_3(message, exchange_id: int, public: str, user_setting_id: int):
            if message.content_type == 'text':
                exchange_client = get_exchange_class(exchange_id=int(exchange_id), public=public, secret=message.text,
                                                     chat_id=message.chat.id)
                if exchange_client is not None:
                    assets = exchange_client.get_assets()
                    if assets is None:
                        self.bot.send_message(message.chat.id, '⛔️ wrong API\nTry again!')
                        welcome(message=message)
                    else:
                        result_message = '💰Your assets:\n'
                        for asset in assets:
                            result_message += f'🪙 {asset[1]}\n 💎 {str(asset[2])}\n\n'
                        self.bot.send_message(message.chat.id, result_message)
                        user = self.user_dict[message.chat.id]
                        markup = start_keyboard()
                        # insert database
                        if user_setting_id == 0:
                            error, result = functions.set_user_setting(username=str(user.username),
                                                                       exchange_id=int(exchange_id),
                                                                       public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if error:
                                self.bot.send_message(message.chat.id, '😥 Something is wrong\n Try again! ', markup)
                            else:
                                self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)
                        else:
                            result = functions.update_user_exchange(user_setting_id=int(user_setting_id),
                                                                    exchange_id=int(exchange_id),
                                                                    public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if result is None:
                                self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)
                            else:
                                self.bot.send_message(message.chat.id, '😥 You cant have same exchange account! ',
                                                      markup)
                else:
                    self.bot.send_message(message.chat.id, '⛔️ unfortunately this exchange not supported for now')
                    welcome(message=message)
            else:
                self.bot.send_message(message.chat.id, '⛔️ wrong API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=public,
                                                    user_setting_id=user_setting_id)

        @self.bot.message_handler(func=self.back_test_command)
        def back_test(message):
            try:
                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, '📊 Please Select analysis',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def back_test_step_1(message):
            try:
                analysis_id = np.where(self.analysis[:, 1] == message.text)[0][0]
                description = functions.get_analysis(analysis_id=int(self.analysis[analysis_id][0]))[0][2]
                self.bot.send_message(message.chat.id, description)
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, '🪙 Choose Coin',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis=self.analysis[analysis_id][1])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong analysis')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

        def back_test_step_2(message, analysis: str):
            try:
                coin_id = np.where(self.coins[:, 1] == message.text)[0][0]
                key_markup = timeframe_keyboard()
                self.bot.send_message(message.chat.id, '⏱ Choose timeframe',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis=analysis, coin=self.coins[coin_id][1])

            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong coin')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis=analysis)

        def back_test_step_3(message, analysis: str, coin: str):
            try:
                timeframe_id = np.where(self.timeframes[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, '💰 Please enter amount of founds initially available for'
                                                       ' the strategies for trade(⚠️ greater than 0)',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis=analysis, coin=coin,
                                                    timeframe=self.timeframes[timeframe_id][1])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong timeframe')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis=analysis, coin=coin)

        def back_test_step_4(message, analysis: str, coin: str, timeframe: str):
            # try:
            amount = float(message.text)
            if not 0 < amount:
                self.bot.send_message(message.chat.id, '⚠️ Amount must be greater than 0')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis=analysis, coin=coin,
                                                    timeframe=timeframe)
            else:
                timeframe_data = timeframe_binance_dictionary[timeframe]
                timeframe_id = timeframe_data[1]
                timeframe = timeframe_data[0]
                self.bot.send_message(message.chat.id, 'just a moment,processing ...')
                recommendation = get_analysis_class(analysis=analysis, symbol=coin,
                                                    timeframe_id=timeframe_id, timeframe=timeframe)
                markup = start_keyboard()
                if recommendation is None:
                    result = '⛔️This strategy doesnt work with this timeframe and coin'
                else:
                    recommendation.to_csv('test.csv')
                    result = StrategyTaster(name='telegram', symbol=coin, timeframe=timeframe,
                                            intial_value=int(amount), dataframe=recommendation).result.values[0]
                    result = f'🪙 *{result[1]}*\n⏰ *{result[2]}*\n⏲Start time: *{result[3]}*\n' \
                             f'⏲End time: *{result[4]}*\n' \
                             f'🟢Positive trades: *{result[5]}*\n' \
                             f'🟢total trades: *{result[6]}*\n' \
                             f'✅Total trade accuracy percent: *{result[7]}*%\n' \
                             f'✅Net profit percent: *{result[8]}*%\n✅Average trade profit: *{result[9]}*%\n' \
                             f'✅Profit per coin percent: *{result[10]}*%'
                self.bot.send_message(message.chat.id, result, reply_markup=markup, parse_mode='Markdown')

            # except (ValueError, TypeError):
            #     self.bot.send_message(message.chat.id, '⚠️ Amount must be greater than 0')
            #     self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
            #                                         analysis=analysis, coin=coin,
            #                                         timeframe=timeframe)

        @self.bot.message_handler(func=self.check_add_command)
        def add_strategy(message, watchlist_id: int = 0):
            try:
                key_markup = user_exchanges_account_keyboard(message=message)
                if key_markup:
                    self.bot.send_message(message.chat.id, '🏛  Please Select your exchange account',
                                          reply_markup=key_markup)
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1,
                                                        watchlist_id=watchlist_id)
                else:
                    self.bot.send_message(message.chat.id, '⛔️ Please set your exchange account first')

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def add_strategy_step_1(message, watchlist_id: int = 0):
            try:
                exchanges_id = np.where(self.exchanges[:, 1] == message.text)[0][0]

                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, '📊 Please Select analysis',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=self.exchanges[exchanges_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong exchange')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1,
                                                    watchlist_id=watchlist_id)

        def add_strategy_step_2(message, exchange_id: int, watchlist_id: int = 0):
            try:
                analysis_id = np.where(self.analysis[:, 1] == message.text)[0][0]
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, '🪙 Choose Coin',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, analysis_id=self.analysis[analysis_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong analysis')

                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=exchange_id, watchlist_id=watchlist_id)

        def add_strategy_step_3(message, exchange_id: int, analysis_id: int, watchlist_id: int = 0):
            try:
                coin_id = np.where(self.coins[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, '💰 Please enter percent of coin \n'
                                                       'You want to trade (⚠️ between 0 - 100)',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, analysis_id=analysis_id,
                                                    coin_id=self.coins[coin_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong coin')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, analysis_id=analysis_id,
                                                    watchlist_id=watchlist_id)

        def add_strategy_step_4(message, exchange_id: int, coin_id: int, analysis_id: int, watchlist_id: int = 0):
            user = self.user_dict[message.chat.id]
            try:
                percent = float(message.text)
                if not 0 < percent < 100:
                    self.bot.send_message(message.chat.id, '⚠️ Percent must be between 0 - 100')
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                        exchange_id=exchange_id, coin_id=coin_id,
                                                        analysis_id=analysis_id, watchlist_id=watchlist_id)
                else:
                    markup = start_keyboard()
                    setting_id = functions.get_user_settings_id(chat_id=message.chat.id,
                                                                exchange_id=exchange_id)[0][0]
                    if watchlist_id == 0:
                        error, result = functions.set_watchlist(user_setting_id=int(setting_id), coin_id=int(coin_id),
                                                                username=user.username, analysis_id=int(analysis_id),
                                                                amount=percent)
                        if error:
                            self.bot.send_message(message.chat.id, '😥You already have this strategy '
                                                                   'with selected coin and analysis',
                                                  reply_markup=markup)
                        else:
                            self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)
                    else:
                        result = functions.update_user_strategy(user_setting_id=int(setting_id), coin_id=int(coin_id),
                                                                analysis_id=int(analysis_id), amount=percent,
                                                                watchlist_id=watchlist_id)
                        if result is None:
                            self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)
                        else:
                            self.bot.send_message(message.chat.id, '😥You already have this strategy '
                                                                   'with selected coin and analysis',
                                                  reply_markup=markup)
            except (ValueError, TypeError):
                self.bot.send_message(message.chat.id, '⚠️ percent must be between 0 - 100')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, coin_id=coin_id,
                                                    analysis_id=analysis_id, watchlist_id=watchlist_id)

        @self.bot.message_handler(func=self.profile_command)
        def profile(message):
            profile_option = types.InlineKeyboardMarkup(row_width=2)
            plan, valid, strategies_dict, accounts_dict = generate_profile_show_message(chat_id=message.chat.id)
            profile_option.add(types.InlineKeyboardButton('strategies',
                                                          callback_data="profile_edit_strategies"),
                               types.InlineKeyboardButton('exchanges',
                                                          callback_data="profile_edit_exchanges"),
                               types.InlineKeyboardButton('trade history',
                                                          callback_data="profile_show_history")
                               )
            self.bot.send_message(chat_id=message.chat.id, text=f'💳 Plan:\n🔹{plan}\n⏱ Valid date:  {valid}\n\n'
                                                                f'📊 Strategies: \t{strategies_dict}\n'
                                                                f'🏛 Exchanges: \t{accounts_dict}',
                                  reply_markup=profile_option)

        @self.bot.message_handler(func=self.tutorial_command)
        def tutorials(message):
            try:
                key_markup = tut_cat_keyboard()
                self.bot.send_message(message.chat.id, '📚  Please Select tutorial category',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=show_tutorial_step_1)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def show_tutorial_step_1(message):
            try:
                category_id = np.where(self.tut_cat[:, 1] == message.text)[0][0]
                key_markup = tut_medias_keyboard(category=self.tut_cat[category_id][1])
                self.bot.send_message(message.chat.id, '📼  Download any tutorial you want',
                                      reply_markup=key_markup)
                back_tut_keyboard = back_home_tut()
                self.bot.send_message(message.chat.id, '🤓  Enjoy',
                                      reply_markup=back_tut_keyboard)
                self.bot.register_next_step_handler(message=message, callback=back_tut)

            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong category')
                self.bot.register_next_step_handler(message=message, callback=show_tutorial_step_1)

        def back_tut(message):
            if message.text == 'back home':
                welcome(message=message)
            elif message.text == 'categories':
                self.bot.register_next_step_handler(message=message, callback=tutorials)

            else:
                self.bot.register_next_step_handler(message=message, callback=back_tut)

        @self.bot.message_handler(func=lambda message: message.text == '📬 social media')
        def help_me(message):
            try:
                key_markup = social_keyboard()
                self.bot.send_message(message.chat.id, '📬 Follow us on social media',
                                      reply_markup=key_markup)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)

        @self.bot.message_handler(func=lambda message: message.text == '🤔 help')
        def help_me(message):
            try:
                self.bot.reply_to(message, 'Some help')

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)

        @self.bot.message_handler(func=self.plan_command)
        def plan_charge(message):
            try:
                self.bot.reply_to(message, 'contact admin to upgrade your plan')

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)
