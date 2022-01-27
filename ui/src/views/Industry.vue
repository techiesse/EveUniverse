<template>
    <div class="home container">
        <IndustryTable :data="prices" />
    </div>
</template>

<script>
// @ is an alias to /src
import IndustryTable from '@/components/IndustryTable/IndustryTable.vue'
import {fetchResource, fetchTrackingList} from "@/fetch.js"


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
        this.prices = await fetchResource('http://localhost:8000/main/api/industry/monitoring/1/')
    }
}
</script>

<style scoped>
    .link-list {
        text-align: left;
    }
</style>
