from odoo.tests.common import TransactionCase
from odoo import fields

class TestRepair(TransactionCase):

    # crear 5 órdenes de seguimiento
    def setUp(self, *args, **kwargs):
        super(TestRepair, self).setUp(*args, **kwargs)


        self.time_ids_demiurg = self.env['mrp.repair.time_tracking_repairs']
        self.time_ids01 = self.time_ids_demiurg.create({
            'date_start': fields.Datetime.from_string("2019-02-18 10:19:01"),
            'date_end': fields.Datetime.from_string("2019-02-18 11:19:01")
        })

        self.time_ids02 = self.time_ids_demiurg.create({
            'date_start': fields.Datetime.from_string("2019-02-18 10:19:01"),
            'date_end': fields.Datetime.from_string("2019-02-18 11:19:01")
        })

        self.repair01 = self.env.ref('mrp_repair_resp.repair01')



        self.repair02 = self.env.ref('mrp_repair_resp.repair02')






    # checks if:
    ## repair01.time_ids' duration is equal to 60.0
    ## repair01's duration and repair01.time_ids' duration are equal
    def test_duration_repair01(self):
        self.repair01.time_ids = [(4, self.time_ids01.id)]
        self.assertEqual(self.repair01.time_ids.duration, 60)
        self.assertEqual(self.repair01.duration, self.repair01.time_ids.duration)

    def test_duration_repair02(self):
        self.repair02.time_ids = [(6, 0, [self.time_ids01.id, self.time_ids02.id])]
        self.assertEqual(len(self.repair02.time_ids), 2)
