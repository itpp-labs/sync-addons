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
        import requests
        import base64
        import csv
        from io import BytesIO, TextIOWrapper
        import logging
        _logger = logging.getLogger(__name__)
        
        # log_transmission = eval_context["log_transmission"]
        log = eval_context["log"]
        params = eval_context["params"]
        if not all([params.PRODUCTS_URL, params.PRICES_URL, secrets.LOGIN, secrets.PASSWORD]):
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

        def get_file(url, ref):
            r = requests.get(url, auth=(secrets.LOGIN, secrets.PASSWORD))
            ref.datas = base64.b64encode((r.content or "\n"))
            return ref

        def fetch_image_from_url(url):
            """
            :param url: The URL to fetch.
            :return: Returns a base64 encoded string.
            """
            data = ""
            try:
                data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
            except Exception as e:
                log("There was a problem requesting the image from URL {}".format(url), level="debug")
            return data

        def create_products(products, group):
            products_fields, products_data = products
            product_name = products_fields.index("product_name")
            image_large = products_fields.index("image_large")
            productid = products_fields.index("productid")
            retail_price = products_fields.index("retail_price")
            ean = products_fields.index("ean")
            productgroup = products_fields.index("productgroup")
            for product in products_data:
                if product[productgroup] == group:
                    self.env["product.template"].create([{
                        "name": product[product_name],
                        "default_code": product[productid],
                        "image_1920": fetch_image_from_url(product[image_large]),
                        "list_price": float(product[retail_price]),
                        "barcode": product[ean]
                    }])

        def create_pricelist(prices):
            prices_fields, prices_data = prices
            productid = prices_fields.index("productid")
            price = prices_fields.index("price")
            min_qty = prices_fields.index("quantityamount")
            # problem: Lead time is written by default to 1 day.
            # problem: after each run of this function a new record in pricelist is created instead of updated
            for prices in prices_data:
                if prices[productid] == self.env['product.template'].search([('default_code', '=', prices[productid])]).default_code:
                    self.env["product.supplierinfo"].create([{
                        "name": self.env.ref('sync_twindis.res_partner_twindis').id,
                        "product_code": prices[productid],
                        "min_qty": prices[min_qty],
                        "product_tmpl_id": self.env['product.template'].search([('default_code', '=', prices[productid] )]).id,
                        "price": float(prices[price])
                    }])

        return {
            "get_file": get_file,
            "read_csv_attachment": read_csv_attachment,
            "create_products": create_products,
            "create_pricelist": create_pricelist,
        }

