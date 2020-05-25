import telebot
from telebot import types

token = ""
liqpay_token = ""
bot = telebot.TeleBot(token)

#for example
#also can use db
items = {
	"coffee": {
		"description": "Robust coffee",
	},
	"tea": {
		"description": "Robust tea",
	}
}
prices = {
	"coffee": [types.LabeledPrice(label="coffee", amount=1000)],
	"tea": [types.LabeledPrice(label="tea", amount=2000)],
}


#start
#and help
@bot.message_handler(commands=["start", "help"])
def start_command(message):
	bot.send_message(message.chat.id, "Hi!\nI am demo shop bot!\nYou can see menu using '/menu'")


#main menu
#show items and other
@bot.message_handler(commands=["menu"])
def menu_command(message):
	keyboard = types.ReplyKeyboardMarkup()
	button_help = types.KeyboardButton(text="/help")
	keyboard.add(button_help)

	for i in items.keys():
		button_item = types.KeyboardButton(text="/item " + i)
		keyboard.add(button_item)

	bot.send_message(message.chat.id, "Ok, look at menu!", reply_markup=keyboard)

#start buying item
#show description
@bot.message_handler(commands=["item"])
def shopitem_command(message):

	if(len(message.text.split(" "))<2):
		bot.send_message(message.chat.id, "please, select item")
		return

	#get item name
	item_name = message.text.split(" ")[1]#/item someitem

	if(item_name not in items.keys()):
		bot.send_message(message.chat.id, "please, select valid item")
		return

	#get item description
	item = items[item_name]

	#send invoice with specified item
	bot.send_invoice(message.chat.id, title=item_name, 
		description=item["description"], currency="uah", 
		provider_token=liqpay_token, prices=prices[item_name], 
		start_parameter=item_name+'-example',
		invoice_payload='test_payload')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
	bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
	bot.send_message(message.chat.id, "Thank you for payment")

if __name__ == "__main__":
	bot.polling()