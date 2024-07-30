/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(Order.prototype, {
    async pay() {
      const order = this.get_orderlines();
      let disc_amt = 0;
      const [maxDiscount,is_limit] = await this.pos.orm.call('pos.session','get_discount_limit',[[this.session_id]]);
      order.forEach(values => {
        const disc = (values.getUnitDisplayPriceBeforeDiscount() * values.quantity) * (values.discount/100);
        disc_amt += disc;
      });
      if (disc_amt > maxDiscount && is_limit){
        await this.env.services.popup.add(ErrorPopup, {
          title: _t("Exceed Discount Limit!"),
          body: _t("Sorry, Discount is not allowed. the discount limit for this session has been exceeded balance is %s ",maxDiscount),
        });
      }
      else{
        if(is_limit && disc_amt>0){
          var balance = maxDiscount - disc_amt
          await this.pos.orm.call('pos.session','update_discount_limit',[[this.session_id]],{balance:balance})
        }
        return super.pay(...arguments);
      }

    }
});



