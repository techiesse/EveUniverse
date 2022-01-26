<template>
    <div class="row">
        <div class="col-6">
            <table class="table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Preço</th>
                    </tr>
                </thead>
                <tbody>
                    <tr :key="item.id" v-for="item in items" >
                        <td>{{item.name}}</td>
                        <td style="text-align: right;"> {{item.price}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>


export default {
    name: 'ItemPriceList',

    props: {
        items: Array
    },
}
</script>
