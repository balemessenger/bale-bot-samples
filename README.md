# Bale bot python samples [![Build Status](https://travis-ci.org/davidchua/pymessenger.svg?branch=master)](https://travis-ci.org/davidchua/pymessenger)

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

You'll need to create your bot by [@Bot_Father](https://web.bale.ai/#/im/u85515032), Bot_Father, give you a Token.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

updater = Updater(token="Your_Bot_Token_You_Give_from_BotFather",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher

```

__Note__: you need set Config.py if you want to get logger


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

![Generic Bot Output](https://cloud.githubusercontent.com/assets/68039/14519266/4c7033b2-0250-11e6-81a3-f85f3809d86c.png)

##### Sending an image/video/file using an URL:

```python
from pymessenger.bot import Bot
bot = Bot(<access_token>)
image_url = "http://url/to/image.png"
bot.send_image_url(recipient_id, image_url)
```

### Todo

* Structured Messages
* Receipt Messages
* Quick Replies
* Airlines
* Tests!

### Example

![Screenshot of Echo Facebook Bot](https://cloud.githubusercontent.com/assets/68039/14516627/905c84ae-0237-11e6-918e-2c2ae9352f7d.png)

You can find an example of an Echo Facebook Bot in ```examples/```

