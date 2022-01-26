import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Industry from '../views/Industry.vue'
import ItemList from '../views/ItemList.vue'
import IndustryItemPrices from '../views/IndustryItemPrices.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/industry',
        name: 'Industry',
        component: Industry
    },
    {
        path: '/items',
        name: 'ItemList',
        component: ItemList
    },
    {
        path: '/industry/materials',
        name: 'IndustryMaterials',
        component: IndustryItemPrices,
        props: {
            listName: 'materials',
            title: 'Materiais'
        }
    },
    {
        path: '/industry/modules',
        name: 'IndustryModules',
        component: IndustryItemPrices,
        props: {
            listName: 'items',
            title: 'Módulos'
        }
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
