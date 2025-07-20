<script setup>
    import { ref, onMounted } from 'vue';
    import api from '@/api';
    import RecentPurchases from '@/components/RecentPurchases.vue';
    
    const props = defineProps({
        id: String
    })

    const account = ref({});

    onMounted(async () => {
        try {
            console.log('Fetching account');
            const accountResponse = await api.get('/get-account', { params: { account_id: props.id } });
            account.value = accountResponse.data;
            console.log('Status: ', accountResponse.status);
        } catch (error) {
            console.error('Error fetching account:', error);
        }
    });

</script>

<template>
    <main class="container-md d-flex flex-column align-items-center">
        <h1 class="text-center">{{ account.name }}</h1>
        <h2 class="text-center">Skuld 123</h2>
        
        <RecentPurchases :mode="'account'" :id="props.id" />
    </main>
</template>