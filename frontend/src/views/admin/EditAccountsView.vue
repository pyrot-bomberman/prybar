<script setup>
    import { ref, onMounted } from 'vue'
    import api from '@/api'

    const accounts = ref([]);

    onMounted(async () => {
        try {
            console.log('Fetching accounts...');
            // const fullUrl = (api.defaults.baseURL || '') + '/';
            // console.log('Full URL:', fullUrl);

            const response = await api.get('/accounts');
            accounts.value = response.data;

            console.log('Status:', response.status);
            console.log('Accounts fetched:', accounts.value);
        } catch (error) {
            console.error('Error fetching accounts:', error);
        }
    });
</script>

<template>
    <div class="container-md mt-5 d-flex justify-content-center">
        <div style="width: 100%;">
            <h1 class="text-center">Edit Accounts View</h1>
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Personal ID</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="account in accounts" :key="account.id">
                        <td>{{ account.id }}</td>
                        <td>{{ account.name }}</td>
                        <td>{{ account.personal_id }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>