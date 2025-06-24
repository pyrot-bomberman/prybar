<script setup>
    const navLinks = [
        { name: 'Edit Accounts', path: 'edit-accounts' },
        { name: 'Edit Items', path: 'edit-items' }
    ];
</script>

<template>
    <div class="container-fluid p-0 row vh-100">
        <nav class="col-1 text-bg-secondary p-0">
            <router-link
            v-for="link in navLinks"
                :to="`/admin/${link.path}`"
                class="w-100 d-flex justify-content-center align-items-center my-1"
                style="height: 3rem;"
            >
                {{ link.name }}
            </router-link>
        </nav>
        <main class="col-5 container-fluid p-0 m-0">
            <router-view />
        </main>
    </div>
</template>