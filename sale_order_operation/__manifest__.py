# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Sale Order Operations",
    "version": "11.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "Domatix",
    "website": "https://domatix.com",
    "depends": ["sale", "mrp_repair"],
    'data': [
        'views/sale_order_view.xml',
        'views/mrp_repair_order_view.xml',
        'security/ir.model.access.csv'],
    "application": True,
    "installable": True
}
