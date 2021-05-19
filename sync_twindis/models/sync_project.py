# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SyncProjectTwindis(models.Model):

    _inherit = "sync.project"
    eval_context = fields.Selection(
        selection_add=[
            ("twindis", "Twindis"),
        ]
    )

    @api.model
    def _eval_context_twindis(self, secrets, eval_context):
        import base64
        import csv
        from io import BytesIO, TextIOWrapper

        import requests

        log = eval_context["log"]
        params = eval_context["params"]
        if not all(
            [params.PRODUCTS_URL, params.PRICES_URL, secrets.LOGIN, secrets.PASSWORD]
        ):
            raise UserError(_("Credentials are not set"))

        def read_csv_attachment(attachment):
            """
            :attachment: ir.attachment record with csv data

            :return: tuple of csv fields and data
            """
            decoded_datas = base64.decodebytes(attachment.datas)
            encoding = "utf-8"
            f = TextIOWrapper(BytesIO(decoded_datas), encoding=encoding)
            reader = csv.reader(f, delimiter=";")
            fields = next(reader)
            data = [row for row in reader]
            return fields, data

        def get_file(url, ref, update=False):
            if not ref.datas:
                update = True
            if update:
                r = requests.get(url, auth=(secrets.LOGIN, secrets.PASSWORD))
                ref.datas = base64.b64encode(r.content or "\n")

            return ref

        def fetch_image_from_url(url):
            """
            :param url: The URL to fetch.
            :return: Returns a base64 encoded string.
            """
            data = ""
            try:
                data = base64.b64encode(requests.get(url.strip()).content).replace(
                    b"\n", b""
                )
            except Exception:
                log(
                    "There was a problem requesting the image from URL {}".format(url),
                    level="debug",
                )
            return data

        # def create_pricelist(prices):
        #     prices_fields, prices_data = prices
        #     productid = prices_fields.index("productid")
        #     price = prices_fields.index("price")
        #     min_qty = prices_fields.index("quantityamount")
        #     # problem: Lead time is written by default to 1 day.
        #     # problem: after each run of this function a new record in pricelist is created instead of updated
        #     for prices in prices_data:
        #         if (
        #             prices[productid]
        #             == self.env["product.template"]
        #             .search([("default_code", "=", prices[productid])])
        #             .default_code
        #         ):
        #             self.env["product.supplierinfo"].create(
        #                 [
        #                     {
        #                         "name": self.env.ref(
        #                             "sync_twindis.res_partner_twindis"
        #                         ).id,
        #                         "product_code": prices[productid],
        #                         "min_qty": prices[min_qty],
        #                         "product_tmpl_id": self.env["product.template"]
        #                         .search([("default_code", "=", prices[productid])])
        #                         .id,
        #                         "price": float(prices[price]),
        #                     }
        #                 ]
        #             )

        return {
            "get_file": get_file,
            "read_csv_attachment": read_csv_attachment,
            "safe_eval": safe_eval,
            "fetch_image_from_url": fetch_image_from_url,
            # "create_pricelist": create_pricelist,
        }
