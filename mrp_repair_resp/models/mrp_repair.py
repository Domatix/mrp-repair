from odoo import models, fields, api, _, exceptions


class Repairs(models.Model):
    _inherit = "mrp.repair"

    resp = fields.Many2one(comodel_name="res.users", string="Responsible")

    date_planned_start = fields.Datetime(
        "Scheduled Date Start",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
    )
    date_planned_finished = fields.Datetime(
        "Scheduled Date Finished",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
    )
    date_start = fields.Datetime(
        "Effective start date",
        compute="_compute_date_start",
        readonly=True,
        store=True
    )
    date_finished = fields.Datetime(
        "Effective finish date",
        compute="_compute_date_finished",
        readonly=True,
        store=True,
    )
    duration_expected = fields.Float(
        "Expected Duration",
        digits=(16, 2),
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        help="Expected duration (in minutes)",
    )

    duration = fields.Float(
        "Real Duration", compute="_compute_duration", readonly=True, store=True
    )
    duration_unit = fields.Float(
        "Duration Per Unit", compute="_compute_duration", readonly=True,
        store=True
    )
    duration_percent = fields.Integer(
        "Duration Deviation (%)",
        compute="_compute_duration",
        group_operator="avg",
        readonly=True,
        store=True,
    )

    time_ids = fields.One2many(
        "mrp.repair.time_tracking_repairs",
        "time_tracking_id")

    @api.depends("time_ids.date_start")
    def _compute_date_start(self):
        for record in self:
            if record.time_ids:
                start = fields.Datetime.from_string(
                    record.time_ids[0]["date_start"])
                for block in record.time_ids:
                    x = fields.Datetime.from_string(block["date_start"])
                    if x < start:
                        start = fields.Datetime.from_string(
                            block["date_start"])

                record.date_start = start

    @api.depends("time_ids.date_end")
    def _compute_date_finished(self):
        for record in self:
            if record.time_ids:
                end = fields.Datetime.from_string(
                    record.time_ids[0]["date_end"])
                for block in record.time_ids:
                    y = fields.Datetime.from_string(block["date_end"])
                    if y > end:
                        end = fields.Datetime.from_string(block["date_end"])
                record.date_finished = end

    @api.depends("time_ids.duration")
    def _compute_duration(self):
        for record in self:
            record.duration = sum(record.time_ids.mapped("duration"))


class TimeTrackingRepairs(models.Model):
    _name = "mrp.repair.time_tracking_repairs"
    date_end = fields.Datetime("End date")
    date_start = fields.Datetime("Start date")
    time_tracking_id = fields.Many2one(
        "mrp.repair",
        "Repair order")
    duration = fields.Float(
        "Duration",
        compute="_compute_duration",
        store=True)

    resp = fields.Many2one(
        comodel_name="res.users",
        string="Responsible")

    @api.depends("date_end", "date_start")
    def _compute_duration(self):
        for blocktime in self:
            if blocktime.date_end:
                d1 = fields.Datetime.from_string(blocktime.date_start)
                d2 = fields.Datetime.from_string(blocktime.date_end)
                diff = d2 - d1
                dur = round(diff.total_seconds() / 60.0, 2)
                if dur > 0:
                    blocktime.duration = dur
                else:
                    raise exceptions.ValidationError(
                        _("Warning! End date is already due."))
