<script setup>

const props = defineProps({
    item: {
        type: Object,
        required: true
    }
});

</script>

<template>
    <main class="d-flex flex-column align-items-center text-center">
        <h1>{{ props.item.name }}</h1>
        <h2>{{ props.item.price_external }} kr</h2>
        <h4>{{ props.item.price_internal }} kr</h4>
    </main>
</template>