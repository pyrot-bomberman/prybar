<script setup>
    import { ref, onMounted } from 'vue'
    import api from '@/api'

    const items = ref([]);

    onMounted(async () => {
        try {
            console.log('Fetching items...');
            // const fullUrl = (api.defaults.baseURL || '') + '/';
            // console.log('Full URL:', fullUrl);

            const response = await api.get('/items');
            items.value = response.data;

            console.log('Status:', response.status);
            console.log('Items fetched:', items.value);
        } catch (error) {
            console.error('Error fetching items:', error);
        }
    });
</script>

<template>
    <div class="container-md mt-5 d-flex justify-content-center">
        <div style="width: 100%;">
            <h1 class="text-center">Edit items View</h1>
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Time</th>
                        <th>Barcode</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in items" :key="item.id">
                        <td>{{ item.id }}</td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.created_at }}</td>
                        <td>{{ item.barcode }}</td>
                        <td>{{ item.category }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>