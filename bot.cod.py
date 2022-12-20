import telebot
import threading
import pause
from datetime import datetime
from datetime import timedelta
import datetime
import yfinance as yf


class Bot:
    Token = ""
    bot = 0
    commands = []
    def init(self, token): # конструктор
        self.Token = token
        self.bot = telebot.TeleBot(self.Token)
        #self.commands = commandList
    def start(self):
        self.background_funs()
        self.bot.polling(none_stop=True)
    def background_funs(self):
        pass

class FinanceBot(Bot):
    bb = 0
    #bot = 0

    def price_check(self, name, n, period): #эта функция создаёт файл с ценами акции (считывание каждые 5 минут каждый час), где "name" это код акции
            file_name = str(name + '.txt')
            while 1:
                #C = [0] * n #n -- это количество считываний за период. Например, 12 (за период час)
                j = 0
                k = period / n  # оп нынешним преположениям = 5
                now = datetime.now()
                while j <= period:  # period это время (в минутах), за которое создаётся массив значений, например, час (60)
                    for i in range(0, n):
                        tickers = [name]
                        for ticker in tickers:
                            ticker_yahoo = yf.Ticker(ticker)
                            data = ticker_yahoo.history()
                            price = data['Close'].iloc[-1]
                        file1 = open("3.txt", "a")
                        file1.write(str(price))
                        file1.write('\n')
                        file1.close()
                        # C[i] = price
                        j += k
                        now_aam = now + timedelta(minutes=k)
                        pause.until(now_aam)

    def price_read(self, name, n, j):  # j - это сдвиг для медианной цены
        C = [0] * n
        file1 = open(name, "r")  # name должно быть в формате "sample.txt"
        for i in range(0, n):
            price = file1.readline(-n + i - j)
            C[i] = price[:-2]
            C[i] = float(C[i])
        file1.close()
        return C

    def median_price(self, name):
        n = 12
        M = [0] * n
        for i in range(0, n):
            j = n - i
            C = price_read(self,name, n, j)  # предположим в час будет 12 считываний
            high = max(C)
            low = min(C)
            median = (float(high) + float(low)) / 2
            M[i] = median
        return M

    def SMMA(self, name, M, n, shift=1):  # сглаженное скользящее среднее
        if shift == 1:
            smma = sum(M) / n
        else:
            smma = (sum(M) - SMMA(self, name, M, n, shift - 1) + M[0]) / n
        return smma

    def SMA(self, name, n):  # Простое скользящее среднее (Simple Moving Average)
        C = price_read(self, name, n, 0)
        sma = sum(C) / n
        return sma

    def EMA(self, name, n):  # функця ситает экспоненцальное скользящее среднее
        a = 0.02
        if n == 1:
            ema = SMA(self, name, n)
            return ema
        else:
            ema = EMA(self, name, n - 1) + a * (price_read(self, name, n, 0)[-1] - EMA(self, name, n - 1))
            return ema

    def MACD(self, name):  # индикатор MACD
        macd = EMA(name, 12) - EMA(name, 26)
        return macd

    def SIG_MACD(self, name):
        sig = SMA(self, name, 9)
        return sig

    def monotonicity(self, name):  # вот с этой функцией больше всего проблем, я не придумала, как отпределить возрастает цена или убывает, чтобы результат был актуалень для периода, а не для поледних секунд
        C = price_read(self, name, 5, 0)  # тут нулевой элемент это последнне значение цены
        if C[0] >= C[4]:
            return 1
        else:
            return 0

    def SAR(self, name, period, high, low):
        a = 2  # a - фактор ускорения, можно будет потом отдельно высчитывать для более точных результатов
        if period == 0:
            sar = price_read(self, name, 12, 0)[-1]
            return sar
        elif monotonicity(self, name) == 1:
            sar = SAR(self, name, period - 1, high, low) + a * (high - SAR(self, name, period - 1, high, low))
        else:
            sar = SAR(self, name, period - 1, high, low) + a * (low - SAR(self, name, period - 1, high, low))
        return sar

    def Williams_Alligator(self, name):  # позже нужно сделать более точным
        A = [0] * 3
        # mp = (high + low) / 2
        M = median_price(self, name)
        A[0] = SMMA(self, name, M, 13, 8)  # jaw
        A[1] = SMMA(self, name, M, 8, 5)  # teeth
        A[2] = SMMA(self, name, M, 5, 3)  # lips
        if A[0] != A[1] and A[0] != A[2] and A[1] != A[2]:
            return 1
        else:
            return 0

    def RSI(self, name):
        period_tipe = 168  # 168 - в лучае 14-ти часового варианта
        n = 14 * period_tipe
        minn14 = min(price_read(self, name, n, 0))
        maxx14 = max(price_read(self, name, n, 0))
        K = (price_read(self, name, 3, 0)[-1] - minn14) / (maxx14 - minn14 + 0.001)
        D = SMA(self, name, 864)  # 864 = n для трёх дней
        # rsi_locaton1 = 1  # чтобы не было ошибки нужно как-то сохранять старое значение
        rsi_locaton2 = 1
        if K < D:
            rsi_locaton1 = rsi_locaton2
            rsi_locaton2 = 0
        else:
            rsi_locaton1 = rsi_locaton2
            rsi_locaton2 = 1
        if (
                rsi_locaton1 != rsi_locaton2 and rsi_locaton1 < rsi_locaton2) or K > D:  # потом можно будет учесть стремление
            return 1
        else:
            return 0

    def buy(self, name):
        while 1:
            n = 12  # эквивалентно часу
            period = 0
            #name = 'NFLX'  # это пока для примера
            macd = MACD(self, name)
            sig = SIG_MACD(self, name)
            #macd_locaton1 = 1
            macd_locaton2 = 1
            if macd < sig:
                macd_locaton1 = macd_locaton2
                macd_locaton2 = 0
            else:
                macd_locaton1 = macd_locaton2
                macd_locaton2 = 1
            if macd_locaton1 != macd_locaton2 and macd_locaton1 < macd_locaton2:
                low = min(price_read(self, name, n, 0))
                high = max(price_read(self,name, n, 0))
                current_price = price_read(self, name, 1, 0)
                if SAR(self, name, period, high, low) < current_price:
                    if Williams_Alligator(self, name, high, low) == 1:
                        if RSI(self, name) == 1:
                            global bb
                            bb = 1
            elif macd_locaton1 != macd_locaton2 and macd_locaton1 > macd_locaton2:
                low = min(price_read(self, name, n, 0))
                high = max(price_read(self,name, n, 0))
                current_price = price_read(self, name, 1, 0)
                if SAR(self, name, period, high, low) > current_price:
                    if Williams_Alligator(self, name, high, low) == 1:
                        if RSI(self, name) == 0:
                            global bb
                            bb = 2


    def background_funs(self):
        stocks = ['NLFX', 'MSFT', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'F', 'INTC', 'UBER'] # F = ford motor company, INTC = intel corporation
        for i in stocks:
            th = threading.Thread(target=self.price_check(i, 12, 60))
            th.start()
        #th2 = threading.Thread(target=self.buy(self))
        #th2.start()

    def init(self, token):
        Bot.init(self, token)
        self.background_funs()


    @self.bot.message_handler(commands=["/start_m"])
    def start_m(message):
        bot.send_message(message.chat.id, "Добрый день! Теперь этот бот будет присылать вам информацию потенцавльной ползе покупки/продажи акций")
        #self.bot.send_message(message.chat.id, str(self.count))

    def start(self):
        Bot.start(self)

TelegramToken = "5761508185:AAGIMlqEXbnwCYcnwF4HuxUSfZega7pSUqc"
Fb = FinanceBot(TelegramToken)
Fb.start()
