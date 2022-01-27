<template>
    <div class="container">
        <h1>Items</h1>
        <div class="row">
            <div class="col-6">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>ESI ID</th>
                            <th>Tipo</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr :key="item.id" v-for="item in items">
                            <td>{{item.name}}</td>
                            <td>{{item.esiId}}</td>
                            <td>{{item.type}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import {fetchJson} from "@/fetch.js"


export default {
    name: 'ItemList',

    components: {
    },

    data(){
        return {
            items: [],
        }
    },

    async created(){
        this.items = await fetchJson('http://localhost:8000/main/api/items/1/list/')
    }
}
</script>
