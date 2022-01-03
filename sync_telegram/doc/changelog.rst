`4.1.2`
-------

- **Improvement:** handle case, where user blocked bot

`4.1.1`
-------

- **Improvement:** refactor to use common method to create channel

`4.1.0`
-------

- **Improvement:** set initial values on non-demo installation
- **Fix:** add missing dependency `multi_livechat`

`4.0.0`
-------

- **Improvement:** code refactoring to make it compatible with other messenger integration (facebook, viber, etc.)

`3.2.2`
-------

- **Improvement:** code clean up

`3.2.1`
-------

- **Improvement:** In cases when there are many subscribed partners channel name was too long


`3.2.0`
-------

- **New:** Add file sending from Telegram to Odoo and vice versa.
- **New:** The photo of the Telegram user is added to the partner's record

`3.1.1`
-------

**Fix:** get rid of archiving integration after each update

`3.1.0`
-------

- **New:** allow editing telegram chat

`3.0.1`
-------

- **Fix:** transfer customizable module settings to demo data to avoid overriding during the update

`3.0.0`
-------

- **Fix:** Separate text fields and params to avoid misleading when changing parameters

`2.0.0`
-------

- **New:** New folder "Telegram" in Discuss
- **New:** Allow sending messages to telegram chat via record chatter by adding
  Telegram channels to subscribers
- Use PARTNER_NAME_TEMPLATE instead fo PARTNER_NAME_PREFIX, CHAT_RECORD_PREFIX
  instead of CHAT_RECORD_TEMPLATE
- Use italic style in message signature
- Rename parameters: MAIL_CHAT to WEBHOOK_CHAT, RECORD_NAME_PREFIX to
  CHAT_RECORD_NAME_PREFIX, RECORD_MODEL to CHAT_MODEL; Rename relation name for
  links: CHANNEL_REL to TG_CHAT_CHANNEL_REL
- Improve docs

`1.0.0`
-------

- **Init version**
