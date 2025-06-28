<script setup>
    import { ref, onMounted } from 'vue';
    import api from '@/api';
    
    const props = defineProps({
        id: String
    })

    const account = ref({});
    const sales = ref([]);

    onMounted(async () => {
        try {
            console.log('Fetching sales...');
            const salesResponse = await api.get('/get-latest-sale', { params: { count: 20, account: props.id } });
            sales.value = salesResponse.data;
            console.log('Status:', salesResponse.status);

            console.log('Fetching account');
            const accountResponse = await api.get('/get-account', { params: { account_id: props.id } });
            account.value = accountResponse.data;
            console.log('Status: ', accountResponse.status);

            sales.value = sales.value.map(sale => ({
                ...sale,
                text: getSaleText(sale)
            }));
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        // Helper to generate sale text
        function getSaleText(sale) {
            if (!Array.isArray(sale.items)) return '';
            const itemTexts = sale.items.map(item => `${item.quantity} x ${item.name}`);
            let text = '';
            if (itemTexts.length === 1) {
                text = itemTexts[0];
            } else if (itemTexts.length === 2) {
                text = itemTexts.join(' och ');
            } else if (itemTexts.length > 2) {
                text = itemTexts.slice(0, -1).join(', ') + ' och ' + itemTexts[itemTexts.length - 1];
            }
            if (text.length > 150) {
                text = itemTexts[0] + ` och ${itemTexts.length - 1} artiklar till`;
            }
            return text;
        }
    });

</script>

<template>
    <main class="container-md d-flex flex-column align-items-center">
        <h1 class="text-center">{{ account.name }}</h1>
        <h2 class="text-center">Skuld 123</h2>
        <table class="table w-auto">
            <thead>
                <tr>
                    <th>Purchase</th>
                    <th>Time</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="sale in sales" :key="sale.id">
                    <td>{{ sale.text }}</td>
                    <td>{{ new Date(sale.created_at).toLocaleString() }}</td>
                    <td>{{ sale.total }} kr</td>
                </tr>
            </tbody>
        </table>
    </main>
</template>