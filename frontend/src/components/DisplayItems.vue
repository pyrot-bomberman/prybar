<script setup>
const props = defineProps({
    items: {
        type: Array,
        required: true
    }
});
</script>

<template>
    <main class="d-flex flex-column align-items-center text-center">
        <div v-if="props.items.length < 2 && props.items[0].quantity < 2">
            <h1>{{ props.items[0].name }}</h1>
            <h2>{{ props.items[0].price_external }} kr</h2>
            <h4>{{ props.items[0].price_internal }} kr</h4>
        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>External Price (kr)</th>
                        <th>Internal Price (kr)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in props.items" :key="index">
                        <td>{{ item.quantity }}x</td>
                        <td>{{ item.name }}x</td>
                        <td>{{ item.price_external }}</td>
                        <td>{{ item.price_internal }}</td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="2">Total</td>
                        <td>{{ props.items.reduce((sum, item) => sum + item.price_external * item.quantity, 0) }} kr</td>
                        <td>{{ props.items.reduce((sum, item) => sum + item.price_internal * item.quantity, 0) }} kr</td>

                    </tr>
                </tfoot>
            </table>
        </div>
    </main>
</template>