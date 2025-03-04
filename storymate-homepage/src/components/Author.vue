<!-- <span class="author-block">
  <a href="https://shuyanzhou.github.io/">Shuyan Zhou</a><sup>1*</sup>,
</span> -->
<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  author: string
  sup?: string
  href?: string
}>()
</script>

<template>
  <span class="author-block">
    <a
      :href="href"
      :class="{ 'text-blue-500': !!href, 'text-lg': true, 'subpixel-antialiased': true }"
      >{{ author }}</a
    >
    <sup v-if="sup">{{ sup }}</sup>
  </span>
</template>

<style scoped lang="scss">
.author-block {
  padding-left: 16px;
  display: inline-block;
  font-size: 1.25rem;
}
.text-blue-500 {
    color: oklch(.623 .214 259.815);
    --font-sans: ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
    --font-mono: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
}
</style>