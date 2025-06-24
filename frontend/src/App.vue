<script setup>
    import { onMounted, onBeforeUnmount } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()

    function handleEscape(event) {
        if (event.key === 'Escape') {
            router.push('/')
        }
    }

    onMounted(() => {
        window.addEventListener('keydown', handleEscape)
    })

    onBeforeUnmount(() => {
        window.removeEventListener('keydown', handleEscape)
    })
</script>

<template>
    <RouterView />
</template>