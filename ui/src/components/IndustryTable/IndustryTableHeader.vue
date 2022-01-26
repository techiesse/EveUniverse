<template>
    <thead>
        <tr class="align-top">
            <th>{{data.name}}</th>
            <th>{{data.type}}</th>
            <th>{{data.materialsCost}}</th>
            <th>{{data.instalationCost}}</th>
            <th>{{data.productionCost}}</th>
            <th>{{data.minSellPrice}}</th>
            <th>{{data.marketPrice}}</th>
            <th>{{data.profit}}</th>
            <th>{{data.quantityInStock}}</th>
            <th>{{data.maxDailyQuantityPerSlot}}</th>
            <th>{{data.dailyProfitPerSlot}}</th>
            <th>{{data.dailyBatchCost}}</th>
            <th>{{data.profitOverCost}}</th>
        </tr>
    </thead>
</template>


<script>

export default {
    name: 'IndustryTableHeader',
    props: {
        data: Object,
    },
}
</script>


<style scoped>
    th {
        border-style: solid;
        border-collapse: collapse;
        border-width: 2pt;
        border-color: silver;
    }
</style>
