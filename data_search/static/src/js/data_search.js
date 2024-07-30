/** @odoo-module **/
import { Component, useRef, useExternalListener, useState} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
let nextItemId = 1;

export class DataSearchDialog extends Component {
    setup() {
        // Set up the initial state and services.
        this.state = useState({
          focusedIndex: 0,
          menu_list: [],
          result: null,
          query: "",
          isSearchVisible: false,
        });
        this.orm = useService("orm");
        this.inputRef = !this.props.autofocus ? useRef("autofocus") : useAutofocus();
        this.items = useState([]);
        this.rpc = useService("rpc");
        this.menuService = useService("menu");
        this.actionService = useService("action");
        this.dialogService = useService("dialog")
        useExternalListener(window, "click", this.onWindowClick);
        useExternalListener(window, "keydown", this.onWindowKeydown);
    }