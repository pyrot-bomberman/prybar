<script setup>
    const navLinks = [
        { name: 'Edit Accounts', path: 'edit-accounts' },
        { name: 'Edit Items', path: 'edit-items' }
    ];
</script>

<template>
    <div class="container-fluid p-0 vh-100 d-flex flex-row" style="height: 100vh;">
        <nav class="text-bg-secondary p-0 position-fixed h-100" style="width: 160px; min-width: 160px;">
            <router-link
            v-for="link in navLinks"
                :to="`/admin/${link.path}`"
                class="w-100 d-flex justify-content-center align-items-center my-1"
                style="height: 3rem;"
            >
                {{ link.name }}
            </router-link>
        </nav>
        <main class="container-fluid p-0 m-0 flex-grow-1 d-flex flex-column">
            <router-view />
        </main>
    </div>
</template>