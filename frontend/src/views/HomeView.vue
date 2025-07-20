<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router'
import RecentPurchases from '@/components/RecentPurchases.vue';
import DisplayItem from '@/components/DisplayItem.vue';

const router = useRouter();
const sales = ref([]);
const inputData = ref('');
const currentItem = ref(null);

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
        currentItem.value = null;
    }
}

async function handleInput() {
    console.log('Input: ' + inputData.value);
    try {
        console.log('Fetching barcode lookup...');
        const response = await api.get('/get-barcode', { params: { barcode: inputData.value } });
        const barcodeLookup = response.data;
        console.log('Barcode lookup result:', barcodeLookup);

        if (barcodeLookup) {
            if (barcodeLookup.type === 'item') {
                currentItem.value = barcodeLookup;
            } else if (barcodeLookup.type === 'account') {
                router.push({ path: `/account/${barcodeLookup.id}` });
            } else {
                console.error('Unknown type:', barcodeLookup.type);
            }
        } else {
            console.warn('No barcode lookup result found.');
        }

    } catch (error) {
        console.error('Error fetching barcode lookup:', error);
    }
    inputData.value = '';
}

</script>

<template>
    <main class="container-md mx-auto mt-5">
        <input type="text" class="d-block w-100 text-center" v-model="inputData" @keyup.enter="handleInput" autofocus
            placeholder="---> Sikta här <---" />
        <DisplayItem v-if="currentItem" :item="currentItem" />
        <RecentPurchases v-show="!currentItem" :mode="all" />
    </main>

    <router-link to="/admin" class="position-fixed bottom-0 end-0 btn btn-secondary">
        Admin
    </router-link>
</template>