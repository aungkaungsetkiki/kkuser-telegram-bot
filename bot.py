import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token (Hardcoded)
TOKEN = "8137695051:AAEpjJo-IV-nzHOXA_pt0cFCWyHBn03Doyg"

# မှတ်တမ်းများသိမ်းဆည်းခြင်း
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# အကြွေးများသိမ်းဆည်းမည့် dictionary
debts = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f'မင်္ဂလာပါ {user.first_name}!\n'
        'အကြွေးစာရင်းဘော့ထ်ကို အသုံးပြုရန်။\n\n'
        'အသုံးပြုနည်း:\n'
        '/add_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ] - အကြွေးထည့်ရန်\n'
        '/pay_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ] - အကြွေးဆပ်ရန်\n'
        '/list_debts - လက်ရှိအကြွေးစာရင်းကြည့်ရန်'
    )

def add_debt(update: Update, context: CallbackContext) -> None:
    try:
        debtor = context.args[0]
        amount = float(context.args[1])
        
        if debtor in debts:
            debts[debtor] += amount
        else:
            debts[debtor] = amount
            
        update.message.reply_text(f'✅ {debtor} ထံ {amount} ကျပ် အကြွေးထည့်ပြီးပါပြီ။\nစုစုပေါင်း: {debts[debtor]} ကျပ်')
        
    except (IndexError, ValueError):
        update.message.reply_text('❌ အသုံးပြုနည်း: /add_debt [နာမည်] [ငွေပမာဏ]')

def pay_debt(update: Update, context: CallbackContext) -> None:
    try:
        debtor = context.args[0]
        amount = float(context.args[1])
        
        if debtor not in debts:
            update.message.reply_text(f'❌ {debtor} နှင့် ပတ်သက်သော အကြွေးစာရင်း မရှိပါ။')
            return
            
        if debts[debtor] < amount:
            update.message.reply_text(f'❌ ဆပ်လိုသော ငွေပမာဏ ကျန်ငွေထက် များနေပါသည်။\nကျန်ငွေ: {debts[debtor]} ကျပ်')
            return
            
        debts[debtor] -= amount
        
        if debts[debtor] == 0:
            del debts[debtor]
            update.message.reply_text(f'✅ {debtor} ၏ အကြွေးအားလုံး ဆပ်ပြီးပါပြီ!')
        else:
            update.message.reply_text(f'✅ {debtor} ထံ {amount} ကျပ် ဆပ်ပြီးပါပြီ။\nကျန်ငွေ: {debts[debtor]} ကျပ်')
            
    except (IndexError, ValueError):
        update.message.reply_text('❌ အသုံးပြုနည်း: /pay_debt [နာမည်] [ငွေပမာဏ]')

def list_debts(update: Update, context: CallbackContext) -> None:
    if not debts:
        update.message.reply_text('လက်ရှိတွင် မှတ်တမ်းတင်ထားသော အကြွေးများ မရှိပါ။')
        return
        
    message = "📜 အကြွေးစာရင်း:\n"
    for debtor, amount in debts.items():
        message += f"- {debtor}: {amount} ကျပ်\n"
        
    update.message.reply_text(message)

def main() -> None:
    # Bot ကို initialize လုပ်ခြင်း
    updater = Updater(TOKEN)
    
    # Command handlers များ ချိတ်ဆက်ခြင်း
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_debt", add_debt))
    dispatcher.add_handler(CommandHandler("pay_debt", pay_debt))
    dispatcher.add_handler(CommandHandler("list_debts", list_debts))
    
    # Bot ကို စတင်အလုပ်လုပ်စေခြင်း
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
