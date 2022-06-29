<template>
    <div class="home container">
        <IndustryTable :data="prices" />
    </div>
</template>

<script>
// @ is an alias to /src
import IndustryTable from '@/components/IndustryTable/IndustryTable.vue'
import {fetchJson} from "@/fetch.js"


export default {
    name: 'Industry',

    components: {
        IndustryTable
    },

    data(){
        return {
            prices: [],
        }
    },

    async created(){
        this.prices = await fetchJson('http://localhost:8000/main/api/industry/monitoring/1/')
        /*
        this.prices = [
            {
                name: 'Item 1',
                type: 'Módulo',
                materialsCost: 10000,
                instalationCost: 13500,
                productionCost: 30,
                minSellPrice: 50,
                marketPrice: 200,
                profit: 100,
                quantityInStock: 360,
                maxDailyQuantityPerSlot: 180,
                dailyProfitPerSlot: 20000,
                dailyBatchCost: 1000000,
                profitOverCost: 0.50,
            },
            {
                name: 'Item 2',
                type: 'Rig',
                materialsCost: 10000,
                instalationCost: 13500,
                productionCost: 30,
                minSellPrice: 50,
                marketPrice: 200,
                profit: 100,
                quantityInStock: 360,
                maxDailyQuantityPerSlot: 180,
                dailyProfitPerSlot: 20000,
                dailyBatchCost: 1000000,
                profitOverCost: 0.50,
            }
        ]
        */
    }
}
</script>

<style scoped>
    .link-list {
        text-align: left;
    }
</style>
