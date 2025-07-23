<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router'
import RecentPurchases from '@/components/RecentPurchases.vue';
import DisplayItems from '@/components/DisplayItems.vue';
import DisplayAccount from '@/components/DisplayAccount.vue';
import Error from '@/components/Error.vue';

const recentPurchases = ref(null);
const router = useRouter();
const sales = ref([]);
const inputData = ref('');
const currentItems = ref([]);
const currentAccount = ref(null);
const keywords = ['admin', 'avbryt', 'exit'];
const e = ref(false);

onMounted(async () => {
    window.addEventListener('keydown', handleEscape)
    try {
        console.log('Fetching sales...');
        const response = await api.get('/get-latest-sale', { params: { count: 20 } });
        sales.value = response.data;

        console.log('Status:', response.status);
        console.log('Sales fetched:', sales.value);
    } catch (error) {
        console.error('Error fetching sales:', error);
    }
});

onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleEscape)
})

function handleEscape(event) {
    if (event.key === 'Escape') {
        console.log('Escape pressed, resetting state.');
        resetState();
    }
}

function resetState() {
    currentItems.value = [];
    currentAccount.value = null;
    inputData.value = '';
    recentPurchases.value?.getLatestSales();
}

async function lookupBarcode(barcode) {
    try {
        console.log('Fetching barcode lookup...');
        const response = await api.get('/get-barcode', { params: { barcode: barcode } });
        const barcodeLookup = response.data;
        console.log('Barcode lookup result:', barcodeLookup);
        return barcodeLookup;
    } catch (error) {
        console.warn('Error fetching barcode lookup:', error);
        return null;
    }
}

async function handleInput() {
    console.log('Input: ' + inputData.value);
    const input = inputData.value.toLowerCase()
    inputData.value = '';
    console.log(currentItems.value);

    if (keywords.includes(input)) {
        if (input === 'admin') {
            router.push({ path: '/admin' });
        } else if (input === 'exit' || input === 'avbryt') {
            currentItem.value = null;
        }
        return;
    }
    else {
        const result = await lookupBarcode(input);
        if (!result) {
            e.value = true;
            setTimeout(() => {
                e.value = false;
            }, 1000);
            return;
        }
        if (result.type === 'item') {
            //if the item already exists in currentItems, add 1 to the quantity
            const existingItem = currentItems.value.find(item => item.id === result.id);
            if (existingItem) {
                existingItem.quantity += 1;
                return;
            } else {
                result.quantity = 1; // Set initial quantity
                currentItems.value.push(result);
            }
        } else if (result.type === 'account') {
            if (currentItems.value.length > 0) {
                try {
                    console.log('Adding sale...');
                    const items = currentItems.value.map(item => ({
                        item_id: item.id,
                        quantity: item.quantity
                    }));
                    const saleResponse = await api.post('/add-sale', { 
                        account_id: result.id, 
                        items: items 
                    });
                    console.log('Sale added:', saleResponse.data);
                    resetState();
                } catch (error) {
                    console.error('Error adding sale:', error);
                }
            } else {
                currentAccount.value = result;
                recentPurchases.value?.getLatestAccountSales(result.id);
            }
        } else {
            console.error('Unknown type:', result.type);
        }
    }
}

</script>

<template>
    <main class="container-md mx-auto mt-5">
        <input type="text" class="d-block w-100 text-center" v-model="inputData" @keyup.enter="handleInput" autofocus
            placeholder="---> Sikta här <---" />
        <div v-if="!e">
            <DisplayItems v-if="currentItems.length > 0" :items="currentItems" />
            <DisplayAccount v-if="currentAccount" :account="currentAccount" />
            <RecentPurchases v-show="currentItems.length < 1" :mode="currentAccount ? 'account' : 'all'" ref="recentPurchases" />
        </div>
        <Error v-if="e"></Error>
    </main>

    <router-link to="/admin" class="position-fixed bottom-0 end-0 btn btn-secondary">
        Admin
    </router-link>
</template>