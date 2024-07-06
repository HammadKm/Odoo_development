/** @odoo-module **/


import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";

patch(Orderline.prototype, {
    getDisplayData() {
//    console.log(this.product.product_owner_id[1])
        return{
            ...super.getDisplayData(),
            owner: this.product.product_owner_id[1]
        }
    }
});


