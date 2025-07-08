import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary to store debts (in production, use a database)
debts = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'မင်္ဂလာပါ {user.first_name}!\nအကြွေးစာရင်းမှတ်တမ်းဘော့ထ်ကို အသုံးပြုရန်။\n\n'
                             'အသုံးပြုနည်း:\n'
                             '/add_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ] - အကြွေးထည့်ရန်\n'
                             '/pay_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ] - အကြွေးဆပ်ရန်\n'
                             '/list_debts - လက်ရှိအကြွေးစာရင်းကြည့်ရန်')

def add_debt(update: Update, context: CallbackContext) -> None:
    try:
        # Command format: /add_debt name amount
        if len(context.args) < 2:
            update.message.reply_text('ပုံစံမှန်: /add_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ]')
            return

        debtor = context.args[0]
        amount = float(context.args[1])

        if debtor in debts:
            debts[debtor] += amount
        else:
            debts[debtor] = amount

        update.message.reply_text(f'ထည့်သွင်းပြီးပါပြီ! {debtor} ၏ စုစုပေါင်းအကြွေး: {debts[debtor]:.2f}')

    except (ValueError, IndexError):
        update.message.reply_text('ငွေပမာဏကိန်းဂဏန်းဖြစ်ရပါမယ်။\nပုံစံ: /add_debt မောင်မောင် 5000')

def pay_debt(update: Update, context: CallbackContext) -> None:
    try:
        # Command format: /pay_debt name amount
        if len(context.args) < 2:
            update.message.reply_text('ပုံစံမှန်: /pay_debt [အကြွေးရှင်နာမည်] [ငွေပမာဏ]')
            return

        debtor = context.args[0]
        amount = float(context.args[1])

        if debtor not in debts:
            update.message.reply_text(f'{debtor} နှင့်ပတ်သက်သော အကြွေးစာရင်းမရှိပါ။')
            return

        if debts[debtor] < amount:
            update.message.reply_text(f'ဆပ်လိုသောငွေပမာဏ ကျန်ငွေထက် များနေပါသည်။\nကျန်ငွေ: {debts[debtor]:.2f}')
            return

        debts[debtor] -= amount
        if debts[debtor] == 0:
            del debts[debtor]
            update.message.reply_text(f'အကြွေးအားလုံးဆပ်ပြီးပါပြီ! {debtor} ၏ အကြွေးကျန်ငွေ 0 ဖြစ်ပါပြီ။')
        else:
            update.message.reply_text(f'ဆပ်ပြီးပါပြီ! {debtor} ၏ ကျန်ငွေ: {debts[debtor]:.2f}')

    except (ValueError, IndexError):
        update.message.reply_text('ငွေပမာဏကိန်းဂဏန်းဖြစ်ရပါမယ်။\nပုံစံ: /pay_debt မောင်မောင် 2000')

def list_debts(update: Update, context: CallbackContext) -> None:
    if not debts:
        update.message.reply_text('လက်ရှိအကြွေးစာရင်းမရှိပါ။')
        return

    message = "အကြွေးစာရင်း:\n"
    for debtor, amount in debts.items():
        message += f"- {debtor}: {amount:.2f}\n"

    update.message.reply_text(message)

def main() -> None:
    # Get bot token from environment variable
    TOKEN = os.getenv("BOT_TOKEN")
    if TOKEN is None:
        logger.error("BOT_TOKEN environment variable not set!")
        return

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add_debt", add_debt))
    dispatcher.add_handler(CommandHandler("pay_debt", pay_debt))
    dispatcher.add_handler(CommandHandler("list_debts", list_debts))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
