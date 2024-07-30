/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.EditPublicTree = publicWidget.Widget.extend({
    selector: '#wrap',
    events: {
        'click .edit_btn': '_onEdit',
        'click .checkbox': '_onCheck',
        'click .billing': '_onBilling',
    },

    _onEdit: function(ev){
    var current_row = $(ev.target).parent().parent();
    var name = current_row.find("td:eq(1)").text();
    var product = current_row.find("td:eq(2)").text();
    var date = current_row.find("td:eq(3)").text();
    var amount = current_row.find("td:eq(5)").text();
    var val_id = current_row.attr("value")
    console.log(val_id)

    $('#editModalCenter').modal('show');
    $('#name').val(name);
    $('#values').val(val_id);
    $('#products_test').empty();
    $('#products_test').append('<option>'+product+'</option>');
    $('#dates_test').val(date.replace(/\s+/g, ""));
    $('#recurring_amounts').val(amount);
    jsonrpc('/edit',{}).then(result=>{
    for(var i = 0; i < result.product_name.length; i++){
        $('#products_test').append('<option>'+result.product_name[i]+'</option>');
    }
    })
    },

    _onCheck: function(ev){
    console.log('drtyui')
    var rows = ev.target.closest('.test')
    rows.setAttribute('data-checked',rows.getAttribute('data-checked')==='True'?'False':'True')
    },

    _onBilling: function(){
    var name_list=[]
    console.log('dfghjk')
    var data = $('[data-checked="True"]')
    console.log(data)
    for(var i = 0; i < data.length; i++){
    var values = data[i]
    console.log('dfgh',values)
    var invoice_id = values.getAttribute("value")
    var invoice_name = $(`[value=${invoice_id}]`).find("td:eq(1)").text()

    console.log('dfghjoiuy',invoice_name)
    name_list.push(invoice_name)
    console.log(name_list)
    }
    jsonrpc('/billing_schedule',{'name':name_list}).then(result=>{
    console.log(result)
    window.location.href='/recurring-subscription'
    })
    },
});

publicWidget.registry.SubscriptionCreditForm = publicWidget.Widget.extend({
    selector: '#credit_form',
    events: {
        'change #subscription': '_onChangeSubscription',
        'click #credit_submit': '_onSubmitCredit',
    },
    _onChangeSubscription: function(){
        console.log('dfghj')
        var cust = $('#subscription').val()
        console.log(cust)
        jsonrpc('/credit_cust',{'cust':cust}).then(result=>{
        console.log(result)
        $('#customer').attr('data-value',result.customer_id)
        $('#customer').val(result.customer)})
    },

    _onSubmitCredit:function(){
    var subscription = $('#subscription').val()
    var customer = $('#customer').attr('data-value')
    var credit = $('#credit').val()
    jsonrpc('/credit_customer',{'name':subscription,'customer':customer,'credit':credit}).then(result=>{
    window.location.href='/recurring-subscription'})
    console.log(subscription)
    console.log(customer)
    console.log(credit)
    console.log('sdfrg')
    }
});


