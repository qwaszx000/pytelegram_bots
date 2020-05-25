import requests
import time

global last_curse
last_course = 6728.78

url = "https://api.telegram.org/bot619218332:AAHo5xCiG5DcfvT_STEcHwdIT7YKiNQ09M/"

def get_upd_json(request):
    resp = requests.get(request+'getUpdates')
    return resp.json()

def last_upd(dat):
    res = dat['result']
    upds = (len(res) - 1) #приводим к счету с 0
    if(res[upds]):
        return res[upds] #последнее сообщение

def get_chat_id(msg):
    id_c = msg['message']['chat']['id']
    return id_c

def send_msg(chat, msg, params={}):
    if(params=={}):
     params = {'chat_id': chat, 'text': msg}
    rsp = requests.post(url + 'sendMessage', data = params)
    return rsp

def get_btc_in_usd():
    global last_curse
    resp = requests.get('https://blockchain.info/ru/ticker').json()
    usd = resp["USD"]['last']
    rub = resp["RUB"]['last']
    r={}
    r["RUB"] = float(rub)
    r["USD"] = float(usd)
    r['izm'] = float(usd) - last_curse
    last_curse = float(usd)
    print(r)
    return r

def news():
    r = get_btc_in_usd()
    idc = get_chat_id(last_upd(get_upd_json(url)))
    send_msg(idc,'Курс БИТКОИН:\nРубли:'+str(r["RUB"])+'\nДоллар США:'+str(r["USD"])+'\nИзменение на '+str(r['izm'])+' долларов\n')
    
while(1):
    news()
    time.sleep(10*60)
