def price_read(name, n, j = 0): # j - это сдвиг для медианной цены
    C = [0] * n
    file1 = open(name, "r") #name должно быть в формате "sample.txt"
    for i in range(0, n):
        price = file1.readline(-n+i-j)
        C[i] = price[:-2]
        C[i] = float(C[i])
    file1.close()
    return C
  
  def SMA(name, n): #Простое скользящее среднее (Simple Moving Average)
    C = price_read(name, n, 0)
    sma = sum(C) / n
    return sma
  
  def SIG_MACD(name):
    sig = SMA(name, 9)
    return sig
