/** @odoo-module **/


import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/store/models";


patch(Orderline.prototype, {
    getDisplayData() {
    console.log(this)
        return{
            ...super.getDisplayData(),

        }
    }
});
//patch(Orderline.prototype, {
//    async set_discount(discount) {
//        var parsed_discount =
//            typeof discount === "number" ?
//            discount :
//            isNaN(parseFloat(discount)) ?
//            0 :
//            oParseFloat("" + discount);
//
//        var disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
//        var maxDiscount = this.config.discount_limit;
//        if (disc > maxDiscount) {
//            await this.env.services.popup.add(ErrorPopup, {
//                title: _t("Exceed Discount Limit!"),
//                body: _t("Sorry, Discount is not allowed. Maximum discount for this Product is %s %", maxDiscount),
//            });
//            this.discount = 0;
//            this.discountStr = "0";
//        } else {
//            this.discount = disc;
//            this.discountStr = "" + disc;
//        }
//    }




//patch(PosStore.prototype, {
//    // @Override
//    async _processData(loadedData) {
//        await super._processData(...arguments);
//        console.log(this)
//        }
//    });