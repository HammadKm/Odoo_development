/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component,useState,onWillStart } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import {_t} from "@web/core/l10n/translation";
import { jsonrpc } from "@web/core/network/rpc_service";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

class SystrayIcon extends Component {
 setup() {
   super.setup(...arguments);
   this.action = useService("action");
   this.state = useState({weather_data :[],weather:{} })
   this.dialogService = useService("dialog");
    onWillStart(async()=>{
        this.state.weather = await this.env.services.orm.call('res.config.settings','get_weather',[[]])
    });
 }

 async _onClick() {
      await jsonrpc('/weather/check',{}).then((data) =>{
        this.data = data
        if (data.name){
            var weather_dict={}
            weather_dict['name'] = data.name
            weather_dict['desc'] = data.weather[0].main
            weather_dict['main'] = data.weather[0].description
            weather_dict['temp'] = Math.round(data.main['temp'] - 273.15)
            this.state.weather_data = weather_dict
        }
        else{
            this.dialogService.add(AlertDialog, {
            body: _t("please enter valid location"),
        });
        }
      })
 }
}
SystrayIcon.template = "systray_icon";
SystrayIcon.components = {Dropdown};
export const systrayItem = {
 Component: SystrayIcon,
};
 registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });


