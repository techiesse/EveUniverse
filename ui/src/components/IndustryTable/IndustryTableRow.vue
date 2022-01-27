<template>
    <tr>
        <td class="no-wrap" style="width: 200px;">{{data.name}}</td>
        <td>{{data.type}}</td>
        <td class="fmt-number">{{fmtMoney(data.materialsCost)}}</td>
        <td class="fmt-number">{{fmtMoney(data.instalationCost)}}</td>
        <td class="fmt-number">{{fmtMoney(data.productionCost)}}</td>
        <td class="fmt-number">{{fmtMoney(data.minSellPrice)}}</td>
        <td class="fmt-number">{{fmtMoney(data.marketPrice)}}</td>
        <td class="fmt-number">{{fmtMoney(data.profit)}}</td>
        <td class="fmt-number">{{data.quantityInStock}}</td>
        <td class="fmt-number">{{data.maxDailyQuantityPerSlot}}</td>
        <td class="fmt-number">{{fmtMoney(data.dailyProfitPerSlot)}}</td>
        <td class="fmt-number">{{fmtMoney(data.dailyBatchCost)}}</td>
        <td class="fmt-number">{{fmtMoney(data.profitOverCost)}}</td>
    </tr>
</template>


<script>

import {money} from "@/format"

export default {
    name: 'IndustryTableRow',
    props: {
        data: Object,
    },
    methods: {
        fmtMoney: money
    },

/*
    mounted(){
        const elems = document.getElementsByClassName('fmt-number')
        for (let elem of elems)
        {
            elem.innerText = money(elem.innerText)
        }
    }
 */
}
</script>


<style scoped>
    td{
        border-style: solid;
        border-collapse: collapse;
        border-width: 2pt;
        border-color: silver;
        width: 10%;
    }

    .no-wrap{
        white-space: nowrap;
    }

</style>
