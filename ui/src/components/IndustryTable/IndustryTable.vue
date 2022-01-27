<template>
    <div>
        <AddItem :labels="header" />
        <button class="btn btn-secondary" @click="sort('dailyProfitPerSlot')">Sort</button>
        <table class="industry-table">
            <IndustryTableHeader :data="header" />
            <tbody>
                <template v-for="item in tableData" :key="item.id">
                    <IndustryTableRow :data="item" />
                </template>
            </tbody>
        </table>
    </div>
</template>


<script>
import IndustryTableHeader from '@/components/IndustryTable/IndustryTableHeader.vue'
import IndustryTableRow from '@/components/IndustryTable/IndustryTableRow.vue'
import AddItem from '@/components/IndustryTable/AddItem.vue'
import {fetchResource, fetchTrackingList} from "@/fetch.js"


const HEADER = {
    name: 'Item',
    type: 'Tipo',
    materialsCost: 'Materiais',
    instalationCost: 'Instalação',
    productionCost: 'Custo de Produção',
    minSellPrice: 'Valor Mínimo de Venda',
    marketPrice: 'Valor Atual em Jita',
    profit: 'Lucro Atual',
    quantityInStock: 'Estoque Atual',
    maxDailyQuantityPerSlot: 'Qtd / dia / slot',
    dailyProfitPerSlot: 'Lucro / dia  /slot',
    dailyBatchCost: 'Custo Lote (1 dia)',
    profitOverCost: 'Lucro / Custo',
}

export default {
    name: 'IndustryTable',

    components: {
        AddItem,
        IndustryTableRow,
        IndustryTableHeader,
    },

    props: {
        data: Array,
    },

    data() {
        return {
            materialPrices: {},
            modulePrices: {},
            tableData: [],
            header: HEADER,
        }
    },

    methods: {
        sort(key) {
            console.log("Funciona !!!", key); //<<<<<
            this.tableData.sort((a, b) => a[key] < b[key] ? -1 : 1)
        }
    },

    async created() {
        try {
            const modules = await fetchTrackingList('items')
            for (const m of modules.items)
            {
                this.modulePrices[m.esiId] = m
            }
        }
        catch(err){
            console.log(err); //<<<<<
        }

        try{
            const materials = await fetchTrackingList('materials')
            for (const m of materials.items)
            {
                this.materialPrices[m.esiId] = m
            }
        }
        catch(err){
            console.log(err); //<<<<<
        }


        for (let i = 0; i < this.data.length; ++i)
        {
            const item = this.data[i]

            const materialsCost = 0 // Calcular o custo dos materiais requeridos com base em "materialPrices"
            const instalationCost = item.instalationCost
            const productionCost = 0 // Calcular a partir dos valores dos materiais usando as Blueprints
            const minSellPrice = 0 // productionCost + taxes
            const marketPrice = parseFloat(this.modulePrices[item.item.esiId].price)
            const profit = marketPrice - productionCost // - taxes
            const quantityInStock = item.quantityInStock
            const maxDailyQuantityPerSlot = 0 // (pegar da blueprint e calcular o percentual)
            const dailyProfitPerSlot = 0
            const dailyBatchCost = 0
            const profitOverCost = 0 // profit / productionCost

            this.tableData[i] = {
                name: item.item.name,
                type: item.item.type,
                materialsCost,
                instalationCost,
                productionCost,
                minSellPrice,
                marketPrice,
                profit,
                quantityInStock,
                maxDailyQuantityPerSlot,
                dailyProfitPerSlot,
                dailyBatchCost,
                profitOverCost,
            }
        }
    }
}

</script>


<style scoped>
    table.industry-table {
        table-layout: fixed;
        width: 100%;
    }

    table, th, td {
        font-size: 10pt;
        border-style: solid;
        border-collapse: collapse;
        border-width: 2pt;
        border-color: silver;
    }

    td.fmt-number{
        text-align: right;
    }

    td.fmt-text{
        text-align: left;
    }



</style>
