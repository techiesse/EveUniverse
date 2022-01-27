<template>
    <div class="container">
        <h1>{{title}}</h1>
        <ItemPriceList :items="items"></ItemPriceList>
    </div>
</template>

<script>

import ItemPriceList from '@/components/ItemPriceList.vue'
import {fetchJson} from '@/fetch'

export default {
    name: 'IndustryItemPrices',

    components: {
        ItemPriceList
    },

    props: {
        //'list-name': String, // Desse jeito não está sendo possível passar no router
        listName: String,
        title: String
    },

    data() {
        return {
            items: []
        }
    },

    async created() {
        const itemType = this.$props.listName
        const url = `http://localhost:8000/main/api/item-prices/1/${itemType}`
        this.items = await fetchJson(url)
        console.log(this.items)
    }
}
</script>
