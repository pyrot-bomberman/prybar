<script setup>
import { ref, onMounted, defineExpose, watch } from 'vue';
import api from '@/api';

const props = defineProps({
    mode: {
        type: String,
        default: 'all'
    },
    id: {
        type: String,
        default: null
    }
});

const sales = ref([]);

onMounted(async () => {
    if (props.mode == 'all') {
        try {
            sales.value = await getLatestSales();
        } catch (error) {
            console.error('Error fetching sales:', error);
        }
    } else if (props.mode == 'account' && props.id) {
        try {
            sales.value = await getLatestAccountSales(props.id);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
});

defineExpose({
    getLatestSales,
    getLatestAccountSales
})

async function getLatestSales() {
    console.log('Fetching sales...');
    const response = await api.get('/get-latest-sale', { params: { count: 20 } });
    var latestSales = response.data;

    console.log('Status:', response.status);

    latestSales = latestSales.map(sale => ({
        ...sale,
        text: getSaleText(sale)
    }));

    sales.value = latestSales;
    return latestSales;
}

async function getLatestAccountSales(accountId) {
    console.log('Fetching sales...');
    const response = await api.get('/get-latest-sale', { params: { count: 20, account: accountId } });
    var latestSales = response.data;

    console.log('Status:', response.status);

    latestSales = latestSales.map(sale => ({
        ...sale,
        text: getSaleText(sale)
    }));
    sales.value = latestSales;
    return latestSales;
}

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

</script>

<template>
    <table class="table">
        <thead>
            <tr>
                <th v-if="props.mode === 'all'">Account</th>
                <th>Item</th>
                <th>Time</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="sale in sales" :key="sale.id">
                <td v-if="props.mode === 'all'">{{ sale.account }}</td>
                <td>{{ sale.text }}</td>
                <td>{{ new Date(sale.created_at).toLocaleString() }}</td>
                <td>{{ sale.total }} kr</td>
            </tr>
        </tbody>
    </table>
</template>