# Copyright 2021-2022 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import SUPERUSER_ID

LOG_DEBUG = "debug"


# Wrapped functions to safely pass as eval context.
# Mostly for Sync Studio
def get_multi_livechat_eval_context(env, channel_type, eval_context):
    get_link = eval_context["get_link"]
    odoobot_id = env.user.browse(SUPERUSER_ID).partner_id.id
    log = eval_context["log"]

    def get_channel(relation, ref, channel_name, partner_ids):
        link = get_link(relation, ref)
        is_new = False
        if not link:
            is_new = True
            vals = env["mail.channel"]._prepare_multi_livechat_channel_vals(
                channel_type, channel_name, partner_ids
            )
            channel = env["mail.channel"].sudo().create(vals)
            link = channel.set_link(relation, ref)
            log("Channel created: %s" % channel)

        return link.odoo, is_new

    def get_partner(relation, ref, callback_vals, callback_kwargs):
        link = get_link(relation, ref)
        is_new = False
        if not link:
            is_new = True
            vals = callback_vals(**callback_kwargs)
            partner = env["res.partner"].sudo().create(vals)
            link = partner.set_link(relation, ref)
            log("Partner created: %s" % partner)
        return link.odoo, is_new

    def get_thread(
        relation, ref, callback_vals, callback_kwargs, model, record_message
    ):
        link = get_link(relation, ref)
        is_new = False
        if not link:
            is_new = True
            vals = callback_vals(**callback_kwargs)
            record = env[model].sudo().create(vals)
            link = record.set_link(relation, ref)

            if record_message:
                record.message_post(
                    body=record_message,
                    author_id=odoobot_id,
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )
            log("Record created: %s" % record)

        return link.odoo, is_new

    def get_channel_url(channel):
        return "/web#action=%s&active_id=mail.channel_%s" % (
            env.ref("mail.action_discuss").id,
            channel.id,
        )

    def get_record_url(record):
        return "/web#id=%s&model=%s" % (
            record.id,
            record._name,
        )

    def message_post(record, message, author=None, **kwargs):
        log("Post message to %s:\n%s" % (record, message), LOG_DEBUG)
        record.message_post(
            body=message,
            author_id=author or odoobot_id,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
            **kwargs,
        )

    return {
        "get_channel": get_channel,
        "get_partner": get_partner,
        "get_thread": get_thread,
        "get_record_url": get_record_url,
        "get_channel_url": get_channel_url,
        "message_post": message_post,
        "channel_type": channel_type,
        "odoobot_id": odoobot_id,
    }
