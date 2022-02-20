<template>
    <div class="container">
        <h1>{{title}}</h1>
        <ItemPriceList :items="items"></ItemPriceList>
        <button class="btn btn-primary" @click="updateButtonClick()">Atualizar</button>
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
        //'list-name': String, // Vue router does not recognize this syntax
        listName: String,
        title: String
    },

    data() {
        return {
            items: []
        }
    },

    async created() {
        this.items = await this.fetchData()
    },

    methods: {
        async updateList() {
            const itemType = this.$props.listName
            return await fetch(`http://localhost:8000/main/api/item-prices/1/${itemType}/update/`, {
                method: 'POST',
                headers: {
                      'Content-Type': 'application/json',
                },
            })
        },

        async fetchData() {
            const itemType = this.$props.listName
            const url = `http://localhost:8000/main/api/item-prices/1/${itemType}/`
            return await fetchJson(url)
        },

        async updateButtonClick() {
            await this.updateList()
            this.items = await this.fetchData()
        }
    }
}
</script>
