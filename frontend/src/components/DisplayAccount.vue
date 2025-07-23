<script setup>
import { ref, watch } from 'vue';
import api from '@/api';

const props = defineProps({
    account: {
        type: Object,
        required: true
    }
});

const debt = ref("");

// Watch for changes in the account prop to fetch the debt for new accounts
// This could be implemented on the backend to return the debt when fetching account details instead
watch(props, async (newProps) => {
    if (newProps.account.id) {
        try {
            console.log('Fetching account debt for ID:', newProps.account.id);
            const response = await api.get('/get-account-debt', { params: { account_id: newProps.account.id } });
            if (response.status === 200) {
                debt.value = response.data.total_debt;
            } else {
                debt.value = null;
                console.error('Failed to fetch account debt:', response.status);
            }
        } catch (error) {
            console.error('Error fetching account debt:', error);
            debt.value = null;
            return;
        }
    } else {
        debt.value = null;
        console.error('Account ID is not provided');
    }
}, { immediate: true });
</script>

<template>
    <main class="container-md d-flex flex-column align-items-center">
        <h1 class="text-center">{{ props.account.name }}</h1>
        <h2 class="text-center">Skuld: {{ debt }}kr</h2>
    </main>
</template>