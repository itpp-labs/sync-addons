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
