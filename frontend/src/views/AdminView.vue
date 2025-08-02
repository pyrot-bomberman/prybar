<script setup>
    const navLinks = [
        { name: 'Edit Accounts', path: 'edit-accounts' },
        { name: 'Edit Items', path: 'edit-items' }
    ];
</script>

<template>
    <div class="container m-0 p-0 min-vh-100 min-vw-100">
        <div class="row">
            <nav class="col-1 mx-50 bg-secondary min-vh-100" style="width: 160px; min-width: 160px;">
                <router-link
                v-for="link in navLinks"
                    :to="`/admin/${link.path}`"
                    class="w-100 d-flex justify-content-center align-items-center my-1"
                    style="height: 3rem;"
                >
                    {{ link.name }}
                </router-link>
            </nav>
            <main class="col-10 mx-50">
                <router-view />
            </main>
        </div>
    </div>
</template>