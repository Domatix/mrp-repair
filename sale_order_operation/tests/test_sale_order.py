from odoo.tests.common import TransactionCase


class TestSale(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestSale, self).setUp(*args, **kwargs)

        self.sale_order_1 = self.env.ref('sale.sale_order_1')
        self.sale_order_line1 = self.env.ref('sale.sale_order_line_1')
        self.sale_order_line2 = self.env.ref('sale.sale_order_line_2')
        self.sale_order_line3 = self.env.ref('sale.sale_order_line_4')
        self.sale_order_1.order_line = [
            (6, 0, {self.sale_order_line1.id, self.sale_order_line3.id})]

        self.soo_demiurg = self.env['sale.order.operation']
        self.soo_1 = self.soo_demiurg.create({
            'product_id': self.sale_order_line1.product_id.id,
            'operation_id': self.sale_order_line3.product_id.id
        })
        self.sale_order_1.operation_ids = [(4, self.soo_1.id)]
        self.sale_order_1.action_confirm()

    def test_order_line_length(self):
        self.assertEqual(2, len(self.sale_order_1.order_line))

    def test_order_ids_creation(self):
        self.assertEqual(1, len(self.sale_order_1.operation_ids))

    def test_mrp_repair_ids(self):
        self.assertEqual(1, len(self.sale_order_1.repair_ids))

    def test_origin_document(self):
        self.assertEqual(
            self.sale_order_1.name,
            self.sale_order_1.repair_ids[0].origin_document)
