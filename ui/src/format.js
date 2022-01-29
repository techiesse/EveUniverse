
import {splitSL} from "./string.js"

export function money(value)
{
    let sValue = value
    if (typeof value == 'number')
    {
        sValue = value.toFixed(2)
    }
    const [_, sign, absValue] = sValue.match(/(-?)(.+)/)
    let [ipart, dpart] = absValue.split('.')
    dpart = dpart || "00"
    const parts = splitSL(ipart, 3)
    const p1 = sign + parts.join('.')
    const ret = [p1, dpart].join(',')
    return ret
}
