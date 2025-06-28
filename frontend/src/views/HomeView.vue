<script setup>
    import { ref, onMounted } from 'vue';
    import api from '@/api';
    import { useRouter } from 'vue-router'

    const router = useRouter();
    const sales = ref([]);
    const inputData = ref('');

    onMounted(async () => {
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

    async function handleInput() {
        console.log('Input: ' + inputData.value);
        try {
            console.log('Fetching barcode lookup...');
            const response = await api.get('/get-barcode', { params: { barcode: inputData.value } });
            const barcodeLookup = response.data;
            console.log('Barcode lookup result:', barcodeLookup);

            if (barcodeLookup) {
                if (barcodeLookup.type === 'item') {
                    // Handle item lookup
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
        <input 
            type="text" 
            class="d-block w-100 text-center"
            v-model="inputData"
            @keyup.enter="handleInput"
            autofocus
            placeholder="---> Sikta här <---" />
        <table class="table">
            <thead>
                <tr>
                    <th>Vem</th>
                    <th>Vad</th>
                    <th>När</th>
                    <th>Hur mycket</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>A</td>
                    <td>Bunch</td>
                    <td>Of</td>
                </tr>
            </tbody>
        </table>
    </main>
    
    <router-link 
        to="/admin" 
        class="position-fixed bottom-0 end-0 btn btn-secondary">
        Admin
    </router-link>
</template>