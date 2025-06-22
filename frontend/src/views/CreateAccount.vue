<script>
    const API_BASE_URL = import.meta.env.API_BASE_URL

    import axios from 'axios';

    console.log('CreateAccount loaded');

    export default {
        name: 'CreateAccount',
        data() {
            return {
                name: null,
                pid: null,
                message: null
            };
        },
        methods: {
            async createAccount() {
                console.log('Creating new account');
                try {
                    const response = await axios.post(`${API_BASE_URL}/accounts`, {
                        name: this.name,
                        pid: this.pid
                    })
                    this.message = `Account created with Name: ${response.data.name} and PID: ${response.data.pid}`;
                    this.name = ''
                    this.pid = ''
                } catch (err) {
                    this.message = err.response?.data?.error || 'Failed to create account'
                }
            }
        }
    };
</script>

<template>
    <main class="container">
        <div>
            <h1>Add User</h1>
            <!-- name, pid -->
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" v-model="name" id="name" placeholder="Enter name">
            </div>
            <div class="mb-3">
                <label for="pid" class="form-label">Personal ID</label>
                <input type="text" class="form-control" v-model="pid" id="pid" placeholder="Enter Personal ID">
            </div>
            <button @click="createAccount" class="btn btn-primary">Add</button>
        </div>
        <p> {{ message }}</p>
    </main>
</template>