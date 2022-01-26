<template>
    <div class="home container">
        <AppMenu />
    </div>

</template>

<script>
import AppMenu from '@/partials/AppMenu.vue'


export default {
    name: 'Home',

    components: {
        AppMenu
    },

    data() {
        return {
        }
    },
}
</script>

<style scoped>
    .link-list {
        text-align: left;
    }
</style>
