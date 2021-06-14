# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
import requests
from facebook_business.adobjects.application import Application
from facebook_business.adobjects.lead import Lead
from facebook_business.api import FacebookAdsApi
from facebook_business.session import FacebookSession

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.sync.models.ir_logging import LOG_WARNING
from odoo.addons.sync.models.sync_project import AttrDict


class SyncProjectFacebook(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(
        selection_add=[("facebook", "Facebook")],
        ondelete={"facebook": "cascade"},
    )

    def _eval_context_facebook(self, secrets, eval_context):
        """Adds Facebook SDK classes:
        * FB.Application
        * FB.Lead
        Docs:
        * https://github.com/facebook/facebook-python-business-sdk/tree/master/facebook_business/adobjects

        The classes use App Access Token. To switch to other access levels, pass api= parameter on class instance initialization.
        * FB_TOKEN.page
        * FB_TOKEN.user

        Token generation tools.
        * FB_EXCHANGE_TOKEN.user2page
        Docs:
        * https://developers.facebook.com/docs/facebook-login/access-tokens
        * https://developers.facebook.com/docs/pages/access-tokens

        General methods for graph API:
        * FB_GRAPH_API.app(method, url, **kwargs)
        * FB_GRAPH_API.page(method, url, **kwargs)
        * FB_GRAPH_API.user(method, url, **kwargs)
        Docs:
        * https://developers.facebook.com/docs/graph-api/
        * https://docs.python-requests.org/en/latest/api/#requests.request
        """
        log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        LOG_INFO = eval_context["LOG_INFO"]
        LOG_ERROR = eval_context["LOG_ERROR"]
        LOG_CRITICAL = eval_context["LOG_CRITICAL"]
        params = eval_context["params"]
        if not all([params.APP_ID, secrets.APP_SECRET]):
            raise UserError(_("Facebook Credentials are not set"))

        access_token_app = params.APP_ID + "|" + secrets.APP_SECRET
        access_token_page = secrets.PAGE_ACCESS_TOKEN
        access_token_user = secrets.USER_ACCESS_TOKEN

        def _graph_api(token_type, access_token, method, path, **kwargs):
            url = f"https://graph.facebook.com/{params.GRAPH_API_VERSION}/" + path
            log_transmission(
                "Facebook Graph API (%s)" % token_type, "{}\n{}".format(path, kwargs)
            )
            kwargs.setdefault("timeout", 5)
            if access_token:
                kwargs.setdefault("data", {}).setdefault("access_token", access_token)
            response = requests.request(method, url, **kwargs)
            log_level = LOG_INFO
            try:
                data = response.json()
                if "error" in data:
                    log_level = LOG_ERROR
            except Exception:
                log_level = LOG_CRITICAL
            log("Graph API RESPONSE:\n{}".format(response.text), log_level)
            return response

        def graph_api_app(method, path, **kwargs):
            return _graph_api(
                "App",
                access_token_app,
                method,
                "%s/%s" % (params.APP_ID, path),
                **kwargs,
            )

        def graph_api_page(method, path, **kwargs):
            return _graph_api(
                "Page",
                access_token_page,
                method,
                "%s/%s" % (params.PAGE_ID, path),
                **kwargs,
            )

        def graph_api_user(method, path, **kwargs):
            return _graph_api(
                "User",
                access_token_user,
                method,
                "%s/%s" % (params.USER_ID, path),
                **kwargs,
            )

        # Patch FacebookAdsApi class to add transmission logs
        class Api(FacebookAdsApi):
            def call(
                self,
                method,
                path,
                params=None,
                headers=None,
                files=None,
                url_override=None,
                api_version=None,
            ):
                session_name = "unknown session"
                if self._session == session_app:
                    session_name = "App"
                elif self._session == session_app:
                    session_name = "Page"
                elif self._session == session_user:
                    session_name = "User"

                log_transmission(
                    "Facebook (%s)" % session_name,
                    "{} {}\nparams: {}\nheaders: {}\nfiles: {}\nurl_override: {}\napi_version: {}".format(
                        method,
                        path,
                        params,
                        headers,
                        files.keys() if files else None,
                        url_override,
                        api_version,
                    ),
                )
                fb_response = super().call(
                    method,
                    path,
                    params=params,
                    headers=headers,
                    files=files,
                    url_override=url_override,
                    api_version=api_version,
                )
                log("RESPONSE:\n{}".format(fb_response.json()))
                return fb_response

        session_app = FacebookSession(
            params.APP_ID,
            secrets.APP_SECRET,
            access_token_app,
        )
        session_page = FacebookSession(
            params.APP_ID,
            secrets.APP_SECRET,
            access_token_page
            or access_token_app,  # TODO: if page token is not available, then page api should not be available
        )
        session_user = FacebookSession(
            params.APP_ID,
            secrets.APP_SECRET,
            access_token_user,
        )

        api_app = Api(session_app)
        api_page = Api(session_page)
        api_user = Api(session_user)
        FacebookAdsApi.set_default_api(api_app)

        def _user2user():
            res = _graph_api(
                "User",
                None,
                "GET",
                "oauth/access_token",
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": params.APP_ID,
                    "client_secret": secrets.APP_SECRET,
                    "fb_exchange_token": secrets.USER_ACCESS_TOKEN,
                },
            )
            return res.json()["access_token"]

        def user2page():
            user_token = _user2user()
            res = _graph_api(
                "User",
                None,
                "GET",
                "%s" % params.PAGE_ID,
                params={
                    "fields": "access_token",
                    "access_token": user_token,
                },
            )
            page_token = res.json()["access_token"]
            secret_param = self.env["sync.project.secret"].search(
                [("key", "=", "PAGE_ACCESS_TOKEN"), ("project_id", "=", self.id)]
            )
            if not secret_param:
                log("secret PAGE_ACCESS_TOKEN is not found", LOG_WARNING)
            else:
                secret_param.sudo().write({"value": page_token})
                log("secret PAGE_ACCESS_TOKEN is successfully updated")

        return {
            "FB": AttrDict(
                Application=Application,
                Lead=Lead,
            ),
            "FB_TOKEN": AttrDict(
                page=api_page,
                user=api_user,
            ),
            "FB_EXCHANGE_TOKEN": AttrDict(
                user2page=user2page,
            ),
            "FB_GRAPH_API": AttrDict(
                app=graph_api_app,
                page=graph_api_page,
                user=graph_api_user,
            ),
        }
