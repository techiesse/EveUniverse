<template>
    <div class="item-add">
        <form>
            <div class="row">
                <div class="col-4">
                    <form-input :label="labels.name" v-model="item.name"/>
                </div>
                <div class="col-4">
                    <form-input :label="labels.type" v-model="item.type"/>
                </div>
                <div class="col-4">
                    <form-input :label="labels.instalationCost" v-model="item.instalationCost"/>
                </div>
            </div>

            <div class="row">
                <div class="col-4">
                    <form-input :label="labels.marketPrice" v-model="item.marketPrice"/>
                </div>
                <div class="col-4">
                    <form-input :label="labels.quantityInStock" v-model="item.quantityInStock"/>
                </div>
                <div class="col-4">
                    <form-input :label="labels.maxDailyQuantityPerSlot" v-model="item.maxDailyQuantityPerSlot"/>
                </div>
            </div>

            <button class="btn btn-primary" @click="onSubmit()">Enviar</button>
        </form>
    </div>
</template>

<script>
const FormInput = {
    props:{
        label: String,
        value: String,
    },
    template: `
    <div class="form-group row">
        <label for="" class="col-4">{{label}}</label>
        <div class="col-8">
            <input class="form-control" type="text" :value="value">
        </div>
    </div>
`
}

export default {
    name: 'AddItem',
    components: {
        'form-input': FormInput,
    },
    data() {
        return {
            item: {
                name: '',
                type: '',
                instalationCost: '',
                marketPrice: '',
                quantityInStock: '',
                maxDailyQuantityPerSlot: '',
            },
        }
    },

    props: {
        labels: Object,
    },

    methods: {
        async onSubmit() {
            // Enviar os dados novos para atualizar no backend
            const response = await fetch(`url de criação ou update de um dos itens`)
            const retrievedItem = response.data

            this.item.name = retrievedItem.name
            this.item.type = retrievedItem.type
            this.item.instalationCost = retrievedItem.instalationCost
            this.item.marketPrice = retrievedItem.marketPrice
            this.item.quantityInStock = retrievedItem.quantityInStock
            this.item.maxDailyQuantityPerSlot = retrievedItem.maxDailyQuantityPerSlot
        }
    }
}
</script>

<style scoped>
    .item-add {
        font-size: 10pt;
        text-align: left;
        border-style: solid;
        border-color: silver;
        padding: 10px;
    }

    .item-add .row {
        margin-bottom: 10px;
    }

    .form-control input[type="text"] {
        font-size: 10pt;
        height: 25%;
    }
</style>