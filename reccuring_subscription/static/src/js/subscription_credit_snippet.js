/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToFragment } from "@web/core/utils/render";

export function _chunk(array,size){
    const result=[];

    for(let i=0; i < array.length; i+=size){
        result.push(array.slice(i, i+size));
        }
        return result;
    }

publicWidget.registry.SubscriptionCreditSnippet = publicWidget.Widget.extend({
    selector: '.dynamic_snippet_blog',
    willStart: async function() {
        var self = this;
        await jsonrpc('/customer_credits',{}).then((data) => {
            this.data = data;
        })
    },
    start: function() {
        var chunks = _chunk(this.data, 4)
        chunks[0].is_active = true
        this.$el.find('#top_products_carousel').html(
            renderToFragment('reccuring_subscription.subscription_credit_snippet', {
                chunks
            })
        )
    },
});
