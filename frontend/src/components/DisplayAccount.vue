<script setup>
const props = defineProps({
    account: {
        type: Object,
        required: true
    }
});
</script>

<template>
    <main class="container-md d-flex flex-column align-items-center">
        <h1 class="text-center">{{ props.account.name }}</h1>
        <h2 class="text-center">Skuld 123</h2>
    </main>
</template>