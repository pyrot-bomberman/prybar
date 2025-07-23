<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router'
import RecentPurchases from '@/components/RecentPurchases.vue';
import DisplayItems from '@/components/DisplayItems.vue';
import DisplayAccount from '@/components/DisplayAccount.vue';
import Error from '@/components/Error.vue';

const router = useRouter();
const keywords = ['admin', 'avbryt', 'exit'];

const recentPurchases = ref(null);
const inputData = ref('');
const currentItems = ref([]);
const currentAccount = ref(null);
const e = ref(false);

// Add event listeners for key presses
onMounted(() => {
    window.addEventListener('keydown', handleKeypress)
});

onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleKeypress)
})

function handleKeypress(event) {
    if (event.key === 'Escape') {
        resetState();
    }
}

// Reset the state of the view
function resetState() {
    currentItems.value = [];
    currentAccount.value = null;
    inputData.value = '';
    recentPurchases.value?.updateSales();
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

async function addSale(id, items) {
    try {
        console.log('Adding sale...');
        items = items.map(item => ({
            item_id: item.id,
            quantity: item.quantity
        }));
        const saleResponse = await api.post('/add-sale', {
            account_id: id,
            items: items
        });
        console.log('Sale added:', saleResponse.data);
        resetState();
        return saleResponse.data;
    } catch (error) {
        console.error('Error adding sale:', error);
        return null;
    }
}

async function handleInput() {
    console.log('Input: ' + inputData.value);
    const input = inputData.value.toLowerCase()
    inputData.value = '';
    console.log(currentItems.value);

    // Check if the input is a keyword
    if (keywords.includes(input)) {
        if (input === 'admin') {
            router.push({ path: '/admin' });
        } else if (input === 'exit' || input === 'avbryt') {
            resetState();
        }
        return;
    }
    else {
        // Find what the barcode is and if it exists
        const result = await lookupBarcode(input);
        if (!result) {
            e.value = true;
            setTimeout(() => {
                e.value = false;
            }, 1000);
            return;
        }
        // If it is an item, add it to the current items
        if (result.type === 'item') {
            const existingItem = currentItems.value.find(item => item.id === result.id);
            if (existingItem) {
                existingItem.quantity += 1;
                return;
            } else {
                currentAccount.value = null;
                result.quantity = 1;
                currentItems.value.push(result);
            }
        } 
        // If products are selected, add the sale to the account
        // Else display the account information
        else if (result.type === 'account') {
            if (currentItems.value.length > 0) {
                addSale(result.id, currentItems.value);
            } else {
                currentAccount.value = result;
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
            <RecentPurchases v-show="currentItems.length < 1" :mode="currentAccount ? 'account' : 'all'"
                :id="currentAccount ? currentAccount.id : null" ref="recentPurchases" />
        </div>
        <Error v-if="e"></Error>
    </main>

    <router-link to="/admin" class="position-fixed bottom-0 end-0 btn btn-secondary">
        Admin
    </router-link>
</template>