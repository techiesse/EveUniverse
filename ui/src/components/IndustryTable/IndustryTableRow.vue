<template>
    <tr>
        <td class="fmt-text">{{data.name}}</td>
        <td class="fmt-text">{{data.type}}</td>
        <td>{{data.materialsCost.toFixed(2)}}</td>
        <td>{{data.instalationCost.toFixed(2)}}</td>
        <td>{{data.productionCost.toFixed(2)}}</td>
        <td>{{data.minSellPrice.toFixed(2)}}</td>
        <td>{{data.marketPrice.toFixed(2)}}</td>
        <td>{{data.profit.toFixed(2)}}</td>
        <td>{{data.quantityInStock}}</td>
        <td>{{data.maxDailyQuantityPerSlot}}</td>
        <td>{{data.dailyProfitPerSlot.toFixed(2)}}</td>
        <td>{{data.dailyBatchCost.toFixed(2)}}</td>
        <td>{{data.profitOverCost.toFixed(2)}}</td>
    </tr>
</template>


<script>

export default {
    name: 'IndustryTableRow',
    props: {
        data: Object,
    },
}
</script>


<style scoped>
    td{
        border-style: solid;
        border-collapse: collapse;
        border-width: 2pt;
        border-color: silver;
        text-align: right;
    }

    td.fmt-text{
        text-align: left;
    }
</style>
