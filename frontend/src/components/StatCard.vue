<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
    <p class="mt-2 text-3xl font-semibold text-gray-900">{{ value }}</p>
    <p class="mt-1 text-sm text-gray-500">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  description: {
    type: String,
    required: true
  }
})
</script>