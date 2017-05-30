# -*- coding: utf-8 -*-
from openerp import models, fields, api
import feedparser
import logging, datetime, pytz

_logger = logging.getLogger(__name__)
#  _logger.erro()

class market_price(models.Model):
     _name = 'market.price'

     _defaults = {'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'reg_code_mp'), }

     date = fields.Date(required=True, default=fields.Date.today)
     price_ton = fields.Float(required=True)
     price_mx = fields.Float(compute="_compute_mx", store=True)
     hour_create = fields.Char(compute="_compute_hour", store=True)

     @api.one
     @api.depends('price_ton','date')
     def _compute_hour(self):
         local = pytz.timezone("America/Chihuahua")
         utc = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"%Y-%m-%d %H:%M")
         local_hr = local.localize(utc,is_dst=None)
         utc_hr = local_hr.astimezone(pytz.utc)
         self.hour_create = utc_hr.strftime("%Y-%m-%d %H:%M")[10:16]

     @api.one
     @api.depends('price_ton','date')
     def _compute_mx(self):
         if self.date:
            self.usd = self.env['market.usd'].search([("date","=",self.date)],limit=1)
            self.price_mx = self.price_ton * self.usd.exchange_rate

     _sql_constraints = [
         ('not_price_mx',
          'CHECK(price_mx > 0)',
          "No se encontro el tipo de cambio"),
     ]

class market_price(models.Model):
    _name = 'market.usd'

    date = fields.Date(required=True, default=fields.Date.today)
    exchange_rate = fields.Float()

    @api.one
    def banxico(self):
        rss_url = "http://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es"
        feeds = feedparser.parse(rss_url)
        for feed in feeds["items"]:
            title = feed["title"]
        self.exchange_rate = float(title[4:11])

    @api.model
    def banxico_auto(self):
        date = datetime.date.today()
        rss_url = "http://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es"
        feeds = feedparser.parse(rss_url)
        for feed in feeds["items"]:
            title = feed["title"]
        self.env['market.usd'].create({
                                'date':date,
                                'exchange_rate':float(title[4:11])
        })
        # _logger.info("ok")

    _sql_constraints = [
        ('date_unique',
        'UNIQUE(date)',
        "Solo se permite un tipo de cambio por dia"),
    ]
