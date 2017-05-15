# -*- coding: utf-8 -*-
from openerp import http

# class MarketPrice(http.Controller):
#     @http.route('/market_price/market_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/market_price/market_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('market_price.listing', {
#             'root': '/market_price/market_price',
#             'objects': http.request.env['market_price.market_price'].search([]),
#         })

#     @http.route('/market_price/market_price/objects/<model("market_price.market_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('market_price.object', {
#             'object': obj
#         })