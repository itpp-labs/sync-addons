================
 1c Integration
================

1c configuration
================

1c instance must have activated and configured OData. Check 1c documentation about how to configure it. For 1cfresh instances the configuration looks as following:

* Зайдите в меню ``Администрирование >> Синхронизация Данных >> Настройки стандартного интерфейса OData``
* Вкладка Состав
  * Нажмите кнопку ``Загрузить метаданые`` (может долго грузиться)
  * Поставьте галочку ``Справочники > Сотрудники``
* Вкладка Авторизация (необязательно)
  * Поставьте галочку ``[x] Создать для использования автоматического REST-сервиса отдельные имя пользователя и пароль``
  * Задайте логин и пароль
* Нажмите кнопку ``Сохранить``

OData must be accessable via internet. For 1cfresh instances ODATA_URL should be something like this: https://1cfresh.com/a/ea_demo/123456/odata/standard.odata/

To work with employee syncing:

* Зайдите в меню ``Quick Menu >> Настройки >> Организации``
* Выделите любую организацию
* Нажмите "Использовать как основную"

Installation
============

* Install this module in according to `Sync Studio <https://apps.odoo.com/apps/modules/12.0/sync/>`__ Documentation

Configuration
=============

* Open menu ``[[ Sync Studio ]] >> Projects``
* Choose ``1c`` project
* Click ``[Edit]``
* Set **Secrets**:

  * ``ODATA_URL``
  * ``ODATA_USERNAME``
  * ``ODATA_PASSWORD``

* For initial synchronization click ``[Run Now]`` on corresponding Manual Triggers that get records from one system and create on another. E.g. to sync employees there are 2 available buttons:

  * CREATE_EMPLOYEES_1C2ODOO
  * CREATE_EMPLOYEES_ODOO21C

* To schedule automatic updates open corresponding taks via  *Available Tasks* tab, configure and activate Cron Triggers

Usage
=====

Create updates in one system and click corresponding ``UPDATE_...`` button in
Manual Triggers. Note, that update buttons works only with previously linked
records (i.e. ones synced via ``CREATE_...`` button). RESULT: records are
synced.

Note: Employees in 1cfresh are available under menu ``Справочники >> Сотрудники``
