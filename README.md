[![Build Status](https://avatars1.githubusercontent.com/u/35299314?s=200&v=4)](https://github.com/balemessenger)

# 1-Bale bot **CURL** Step by Step instruction (NEW 2023)

   Hello, Welcome to PRACTICAL step by step beginners instruction to use Bale bot send first message to a Bale group.
in the Bale developer network there is a very poor description about it and here a nice and sweet description for you.

> [!NOTE]
>This is simple one line command to send a text message
>

#### get ready! and go...!

1. Open bale application
2. Search for a **botfother**
3. Add a bot in bot father with given structions
4. Get bot **tocken** from bot father
5. Create a group
6. Add created bot (in step 3) to that group
7. Add chat bot getchatid -  **@Fgetchatbot** to that group
8. Chatbot give's you a chat_id of that group (a number)
9. Replace the:
    - tocken (**in step 4**) 
    - chat_id (**in step 8**)
    - replace text = Hello... in url below (also delete {} ) hit enter key ! BoooM ;) :

  ```curl  https://tapi.bale.ai/{bot-token-paste-here}/sendMessage --data "chat_id={chat_id_paste_here}&text=HelloAll" ```

## Finish !
فارسی
# 1-آموزش گام به گام برای ارسال متن در CURL پیام رسان بله توسط ربات به صورت ساده و کاربردی
سلام با توجه به توضیح مستندات ناقص در سایت توسعه دهندگان بله در اینجا آموزش کاربردی و گام به گام خصوصاً درباره نحوه بدست آوردن chat_id در بله در یک گروه رو به شما آموزش داده میشه. باتوجه به اینکه بله پیغام داده که نام های ربات که به مدت شش ماه غیرفعال باشند را حذف خواهد کرد به این فکر افتادم که برای استفاده از بات ها این آموزش را قرار بدهم. گاهی اوقات این ربات ها خیلی می تونن مفید باشن مخصوصا اگه بخوایین یک پیغام ساده ارسال کنین از وضعیت سرورهاتون - هشدار آبیاری باغچه و... 
حالا اگه آماده هستین بزنین بریم....!

> [!NOTE]
> این آموزش فقط برای ارسال ساده یک رشته حرف و عدد مناسب است
>

1. پیام رسان بله را باز کنین
2. این عبارت را جستجو کنین **botfother** و داخلش بشین
3. در گزینه هایی که به شما میده افزودن یک ربات را کلیک کنین
4. از رباتی که ساختین یک کد به نام  **tocken**  دریافت کنین
5. بعد یک گروه بسازین
6. رباتی رو که در مرحله 3 ساختین به گروه اضافه کنین
7.  حالا وقته این هست که آی دی گروه اتاق گفتگوی بله را استخراج کنین - یک کاربر به نام **@Fgetchatbot** به گروه اضافه کنین
8. این کاربر که ربات رسمی خود تلگرام هست یک آی دی عددی به شما میده
9. موارد زیر را در لینک زیر اضافه کنین :
    - tocken (**مرحله 4**) 
    - chat_id (**در مرحله 8**)
    -   text = Hello... را تغییر بدین (راستی {} رو هم پاک کنین) بعدش این لینک را در کنسول / برنامه وارد کنین و بوووووم! ;) :

  ```curl  https://tapi.bale.ai/{bot-token-paste-here}/sendMessage --data "chat_id={chat_id_paste_here}&text=HelloAll" ```

## کار تمام شد شما حالا باید پیغام را مشاهده نمایید !

  
> [!IMPORTANT]
> متاسفانه این لینکی که در سایت توسعه دهندگان بله داده شده در برخی کنسول ها کار نمیکنه و پیغام text خالی است را می دهد
> ```
>curl -X POST   https://tapi.bale.ai/bot{token}/sendMessage  -d '{"chat_id": 12343, "text": "Hello World!"}'
> ```


  
# 2- Python user in Bale bot

Python samples for [Bale messenger](https://bale.ai).

### About

This Samples are in five parts:

* simple_hear
* text_conversion
* photo_voice_conversion
* document_conversion
* purchase_conversion


The functions return the full JSON body of the actual API call to Bale.

### Register for an Access Token

You'll need to create your bot by [@Bot_Father](https://web.bale.ai/), Bot_Father, give you a Token.

### Installation

```bash
pip install -r requirements.txt
``` 
# DEPRECATED 
use [new api exmaples](https://github.com/balemessenger/bale-bot-samples/tree/master/new_api_example) 
### Usage

```python
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

updater = Updater(token="Your_Bot_Token_You_Give_from_BotFather",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

```

__Note__: you need set Config.py if you want to get logger


##### Sending a generic simple message:

__Note__:Simple bot hear function
> allows you to hear and answer the client.


```python
@dispatcher.message_handler(filters=TextFilter(keywords=["hello"]))  # filter text the client enter to bot
def hear(bot, update):
    message = TextMessage('Hello')
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
```

Output:

![Generic Bot Output](image_9390.png)

##### Sending a simple voice message:
__Note__:You should upload it first!

> allows you to send voice message(you can send a document in a same way).


```python
def send_voice(bot, update):
    user_peer = update.get_effective_user()
    v_message = VoiceMessage(file_id=file_id, access_hash=access_hash, name="Hello", file_size='259969',
                                 mime_type="audio/mpeg",
                                 duration=20, file_storage_version=1)
    bot.send_message(v_message, user_peer, success_callback=success, failure_callback=failure)
```

Output:

![Generic Bot Output](https://github.com/balemessenger/blob/master/assets/logo.png)
##### Sending a generic template message:

__Note__:Generic Template Messages 
> allows you to add cool text buttons, to a general text message.


```python
def ask_question(bot, update):
    general_message = TextMessage("a message")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
```

Output:

##### Sending a generic purchase message:

> allows you send purchase message that clint can pay it by press "pay" button.

```python

@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = "your message"
    user_peer = update.get_effective_user()
    first_purchase_message = PurchaseMessage(msg=message, account_number="your cart number", amount="how much do you want to ask",
                                             money_request_type=MoneyRequestType.normal)
    bot.send_message(first_purchase_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation()
```
Thanks!
