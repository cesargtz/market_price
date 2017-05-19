# -*- coding: utf-8 -*-
from openerp import models, fields, api

class market_price(models.Model):
     _name = 'market.price'

     date = fields.Date()
     price_ton = fields.Float()
     price_mx = fields.Float(compute="_compute_mx", store=True)

     @api.one
     @api.depends('price_ton','date')
     def _compute_mx(self):
         if self.date:
             self.usd = self.env['market.usd'].search([("date","=",self.date)],limit=1)
             self.price_mx = self.price_ton * self.usd.exchange_rate


class market_price(models.Model):
     _name = 'market.usd'

     date = fields.Date()
     exchange_rate = fields.Float()

     _sql_constraints = [
            ('date_unique',
             'UNIQUE(date)',
             "Solo se permite un tipo de cambio por dia"),
    ]
