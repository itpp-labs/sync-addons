======================
 Telegram Integration
======================

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/14.0/sync/>`__ Documentation


Telegram configuration
======================
Send message /new to @BotFather and follow further instructions to create bot and get the bot token

Odoo Configuration
=============
В первую очередь нужно задать токен бота "TELEGRAM_BOT_TOKEN"
Sync Studio -> Sync Projects -> Telegram Integration -> Parameters

Вы можете изменить модель (карточку) которая будет создана после первичного запуска пользователем бота,
изменив значение параметра 'MODEL' на crm.lead или подобную

**Какой пользователь запускает бота и что значит "запустить"?)**

Usage
=====

In Telegram, send "/start" message to the created bot. 
Теперь в Odoo у появился диалог через который вы можете общаться с пользователем от имени бота



+Ссылка на карточку отправляется в переписку.



