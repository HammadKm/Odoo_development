/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

class BusTest extends Component {
    setup() {
        this.state = useState({
            busVal: ""
        })
        this.busService = this.env.services.bus_service
        this.channel = "your_channel"
        this.busService.addChannel(this.channel)
        this.busService.addEventListener("notification", this.onMessage.bind(this))
    }

    onMessage({detail: notifications}) {
        notifications = notifications.filter(item => item.payload.channel === this.channel)
        notifications.forEach(item => {
            console.log(item, 'items')
            this.state.busVal = item.payload.value.data
        })
    }
}

BusTest.template = 'bus_test';
registry.category("actions").add("bus_test_action", BusTest)