/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
    selector: "#wrap",
    events: {
        'change #operation_type': '_onChangeType',
        'click .add_total_project': '_onClickAdd_total_project',
        'click .remove_line': '_onClickRemove_line',
        'click .custom_create': '_onClickSubmit',

    },
    _onClickSubmit: async function(ev){
            var self = this;
            var partner = $('#customer').val()
            var date = $('#date').val()
        	var material_data = [];
        	var rows = $('.total_project_costs > tbody > tr.material_order_line');
        	for(var i=0;i<rows.length;i++){
        	var values=rows[i]
        	    let product = $(values).find('select[name="product"]').val();
        	    let quantity = $(values).find('input[name="quantity"]').val();
        	    let operation = $(values).find('select[name="operation"]').val();
        	    let src_loc = $(values).find('select[name="source"]').val();
        	    let dest_loc = $(values).find('select[name="destination"]').val();
        	    material_data.push({
        	            'material':product,
        	            'quantity':quantity,
        	            'operation':operation,
        	            'source':src_loc,
        	            'destination':dest_loc,
        	    });
        	    console.log(material_data)
        	}
        	if (material_data && partner && date){
        	    await jsonrpc('/material/submit',{'data':material_data,'partner':partner,'date':date}).then(result=>{
        	    console.log(result)
        	    window.location.href=`/thank-you/${result}`
        	})
        	}


    },

    _onClickAdd_total_project: function(ev){
            	var $new_row = $('.add_extra_project').clone(true);
            	$new_row.removeClass('d-none');
            	$new_row.removeClass('add_extra_project');
            	$new_row.addClass('material_order_line');
            	$new_row.insertBefore($('.add_extra_project'));
    },
    _onChangeType: function(ev){
        if ($(ev.target).closest('tr').find('.operation').val()=="purchase order"){
            console.log("fresh")
            $(ev.target).closest('tr').find('.fields').attr('disabled',true);
        } else{
             console.log("iuy")
            $(ev.target).closest('tr').find('.fields').attr('disabled',false);
        }
    },
    _onClickRemove_line: function(ev){
        $(ev.target).parent().parent().remove();
    },

});