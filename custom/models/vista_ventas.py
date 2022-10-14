# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.exceptions import UserError

class ctt_vista_factura(models.Model):
      _name = 'custom_insoltecsa.vista_ventas'
      _auto = False

      id_invoice = fields.Integer(string="id_invoice")
      pedido= fields.Char(string="pedido")
      tipo= fields.Char(string="tipo")
      factura = fields.Char(string="factura")
      fecha_factura = fields.Date(string="fecha_factura")
      referencia= fields.Char(string="Referencia")
      equipo_ventas = fields.Char(string="equipo_ventas")
      pais = fields.Char(string="pais")
      codigo_cliente = fields.Char(string="codigo_cliente")
      cliente = fields.Char(string="cliente")
      nit = fields.Char(string="Nit")
      sku = fields.Char(string="sku")
      ean = fields.Char(string="ean")
      nombre_sku = fields.Char(string="nombre_sku")
      categoria = fields.Char(string="categoria")
      cantidad = fields.Float(string="cantidad")
      precio_unitario = fields.Float(string="precio_unitario")
      descuento_p = fields.Float(string="descuento_p")
      total_linea = fields.Float(string="total_linea")
      sub_total = fields.Float(string="sub_total")
      usuario = fields.Char(string="Usuario")  


      def init(self):
        tools.drop_view_if_exists(self._cr, 'custom_insoltecsa_vista_factura')
        self._cr.execute("""
    CREATE VIEW custom_insoltecsa_vista_factura AS (
    SELECT row_number() OVER () as id,
    t1.id AS id_invoice,
    t1.invoice_origin AS pedido,
    t1.move_type AS tipo,
    t1.name AS factura,
    t1.date AS fecha_factura,
    t1.ref AS referencia,
    t4.name AS equipo_ventas,
    concat(t6.code, '-', t6.name) AS pais,
    COALESCE(t5.vat, t1.partner_id::character varying) AS codigo_cliente,
    t1.invoice_partner_display_name AS cliente,
	t5.vat as nit,
    t3.default_code AS sku,
    COALESCE(t3.barcode, 'N/A'::character varying) AS ean,
    t7.name AS nombre_sku,
    t8.name AS categoria,
        CASE
            WHEN t1.move_type::text = 'out_refund'::text THEN t2.quantity * '-1'::integer::numeric
            ELSE t2.quantity
        END AS cantidad,
    t2.price_unit AS precio_unitario,
    t2.discount AS descuento_p,
        CASE
            WHEN t1.move_type::text = 'out_refund'::text THEN t2.price_total * '-1'::integer::numeric
            ELSE t2.price_total
        END AS total_linea,
        CASE
            WHEN t1.move_type::text = 'out_refund'::text THEN t2.price_subtotal * '-1'::integer::numeric
            ELSE t2.price_subtotal
        END AS sub_total,
		t9.login as usuario
   FROM account_move t1
     JOIN account_move_line t2 ON t2.move_id = t1.id
     JOIN product_product t3 ON t3.id = t2.product_id
     JOIN crm_team t4 ON t4.id = t1.team_id
     JOIN res_partner t5 ON t5.id = t1.partner_id
     JOIN res_country t6 ON t6.id = t5.country_id
     JOIN product_template t7 ON t7.id = t3.product_tmpl_id
     JOIN product_category t8 ON t8.id = t7.categ_id
	 JOIN res_users t9 on t9.id = t1.invoice_user_id
     WHERE (t1.move_type::text = ANY (ARRAY['out_invoice'::character varying::text, 'out_refund'::character varying::text])) AND t1.state::text <> 'cancel'::text
            )""")