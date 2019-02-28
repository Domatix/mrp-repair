from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    type = fields.Selection(
        [('consu', 'Consumible'),
            ('service', 'Service'),
            ('product', 'Product')],
        string='Type')

    @api.onchange('product_id')
    def _onchange_function_name(self):
        self.type = self.product_id.type


class SaleOrder(models.Model):
    _inherit = "sale.order"

    operation_ids = fields.One2many(
        'sale.order.operation',
        'order_id',
        )

    repair_orders_count = fields.Integer(
            compute='_compute_repair_orders_count',
            string='Repair Orders')

    repair_ids = fields.One2many(
        comodel_name='mrp.repair',
        inverse_name='order_id',
        string='Repairs')

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for order_line in self.operation_ids:
                mrp = self.env['mrp.repair'].create({
                    'product_id': order_line.product_id.product_id.id,
                    'origin_document': self.name,
                    'partner_id': self.partner_id.id,
                    'product_qty': order_line.product_id.product_uom_qty,
                    'product_uom': order_line.product_id.product_uom.id,
                    'location_dest_id':
                        self.env['mrp.repair']._default_stock_location(),
                    'operations': [(0, 0, {
                        'type': 'add',
                        'product_id': order_line.product_id.id,
                        'name': order_line.product_id.product_id.name,
                        'product_uom_qty':
                            order_line.product_id.product_uom_qty,
                        'price_unit': order_line.product_id.price_unit,
                        'product_uom': order_line.product_id.product_uom.id,
                        'location_id':
                            self.env['mrp.repair']._default_stock_location(),
                        'location_dest_id':
                            self.env['mrp.repair']._default_stock_location()
                    })],
                    'fees_lines': [(0, 0, {
                        'product_id': order_line.operation_id.product_id.id,
                        'name': order_line.operation_id.name,
                        'price_unit': order_line.operation_id.price_unit,
                        'product_uom': order_line.operation_id.product_uom.id
                        })],
                })
                self.repair_ids = [(4, mrp.id)]
        return res

    @api.multi
    @api.depends('repair_ids')
    def _compute_repair_orders_count(self):
        self.repair_orders_count = len(self.repair_ids)

    def action_view_repair_orders(self):
        active_ids = self.repair_ids.ids
        return {
            'name': self.name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.repair',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', active_ids)],
            'context': self.env.context,

        }


class RepairOrder(models.Model):
    _inherit = "mrp.repair"

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order')

    origin_document = fields.Char(
        string='Origin Document')


class Operation(models.Model):
    _name = "sale.order.operation"
    _description = "Sale order operation"

    operation_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Operation',
        )

    product_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Product',
        )

    def _get_default_order_id(self):
        return self._context.get('order_id')

    order_id = fields.Many2one(
        comodel_name="sale.order",
        string='',
        default=_get_default_order_id
    )
