<script setup>
import { ref, defineExpose, watch } from 'vue';
import api from '@/api';

const props = defineProps({
    mode: {
        type: String,
        default: 'all'
    },
    id: {
        type: Number,
        default: null
    }
});

const sales = ref([]);

// Fetch sales when component is mounted or props change
watch(props, (newProps) => {
    console.log('Props updated to:', newProps);
    updateSales();
}, { immediate: true });

defineExpose({
    updateSales
});

async function updateSales() {
    if (props.mode == 'all') {
        sales.value = await getLatestSales();
    } else if (props.mode == 'account' && props.id) {
        console.log('Fetching sales for account ID:', props);
        sales.value = await getLatestSales(props.id);
    }
}

// Fetch the latest sales from the API
// If accountId is provided, fetch sales for that account
async function getLatestSales(accountId = null) {
    try {
        console.log('Fetching sales...');
    
        let response;
        if (accountId) {
            response = await api.get('/get-latest-sale', { params: { count: 20, account: accountId } });
        } else {
            response = await api.get('/get-latest-sale', { params: { count: 20 } });
        }
    
        console.log('Get sale status:', response.status);
    
        let latestSales = response.data;
        latestSales = latestSales.map(sale => ({
            ...sale,
            text: getSaleText(sale)
        }));
        return latestSales;
    }
    catch (error) {
        console.error('Error fetching sales:', error);
        return [];
    }
}

// This function is used to create a readable text representation of the sale
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