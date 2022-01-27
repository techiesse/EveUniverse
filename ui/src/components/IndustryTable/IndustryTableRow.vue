<template>
    <tr>
        <td class="no-wrap" style="width: 200px;">{{data.name}}</td>
        <td>{{data.type}}</td>
        <td class="fmt-number">{{data.materialsCost.toFixed(2)}}</td>
        <td class="fmt-number">{{data.instalationCost.toFixed(2)}}</td>
        <td class="fmt-number">{{data.productionCost.toFixed(2)}}</td>
        <td class="fmt-number">{{data.minSellPrice.toFixed(2)}}</td>
        <td class="fmt-number">{{data.marketPrice.toFixed(2)}}</td>
        <td class="fmt-number">{{data.profit.toFixed(2)}}</td>
        <td class="fmt-number">{{data.quantityInStock}}</td>
        <td class="fmt-number">{{data.maxDailyQuantityPerSlot}}</td>
        <td class="fmt-number">{{data.dailyProfitPerSlot.toFixed(2)}}</td>
        <td class="fmt-number">{{data.dailyBatchCost.toFixed(2)}}</td>
        <td class="fmt-number">{{data.profitOverCost.toFixed(2)}}</td>
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
        width: 10%;
    }

    .no-wrap{
        white-space: nowrap;
    }

</style>
