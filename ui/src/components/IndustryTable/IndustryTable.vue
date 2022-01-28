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
            header: HEADER,
            tableData: []
        }
    },

    methods: {
        sort(key) {
            this.tableData.sort((a, b) => a[key] < b[key] ? -1 : 1)
        }
    },

    async created() {

    },

    computed: {
        tableData() {
            return this.data
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
