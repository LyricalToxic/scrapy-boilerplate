import OutputItem from "./item";
import InputItem from "../input-item/input-item";

export default class ErrorItem implements OutputItem {
    constructor(
        public exception: string,
        public traceback: string | null,
        public pageUrl: string | null,
        public pageStatusCode: number | null,
        public datetimeUTC: string | null,
        public inputMessage: InputItem | null,
    ) {
        if (!this.datetimeUTC) {
            this.datetimeUTC = new Date().toISOString().substring(0, 19).replace('T', ' ')
        }
    }
}
