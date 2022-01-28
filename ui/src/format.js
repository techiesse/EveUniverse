
import {splitSL} from "./string.js"

export function money(value)
{
    let sValue = value
    if (typeof value == 'number')
    {
        sValue = value.toFixed(2)
    }
    let [ipart, dpart] = sValue.split('.')
    dpart = dpart || "00"
    const parts = splitSL(ipart, 3)
    const p1 = parts.join('.')
    const ret = [p1, dpart].join(',')
    return ret
}
