<template>
  <div class="input-container">
    <n-input
      :value="modelValue"
      @update:value="handleInput"
      :round="round"
      :placeholder="currentPlaceholder"
      :status="(validateField && showError) ? 'error' : undefined"
      v-bind="$attrs"
    >
      <template #suffix v-if="$slots.suffix">
        <slot name="suffix"></slot>
      </template>
    </n-input>
    <div v-if="validateField && showError" class="error-message">
      This field is required
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { NInput } from 'naive-ui';

const props = defineProps({
  placeholder: {
    type: String,
    required: true
  },
  modelValue: {
    type: String,
    default: ''
  },
  round: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  validateField: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);
const currentPlaceholder = ref('');
const showError = ref(false);
let typewriterInterval = null;
let currentIndex = 0;
let isDeleting = false;
const TYPING_SPEED = 150;
const DELETING_SPEED = 50;
const PAUSE_BEFORE_DELETE = 2000;
const PAUSE_BEFORE_RESTART = 1000;

const handleInput = (value) => {
  emit('update:modelValue', value);
  if (props.required && props.validateField) {
    showError.value = !value?.trim();
  }
};

watch(() => props.validateField, (newValue) => {
  if (newValue && props.required) {
    showError.value = !props.modelValue?.trim();
  } else {
    showError.value = false;
  }
}, { immediate: true });

watch(() => props.modelValue, (newValue) => {
  if (props.required && props.validateField) {
    showError.value = !newValue?.trim();
  }
});

const typeWriter = () => {
  if (!isDeleting && currentIndex <= props.placeholder.length) {
    currentPlaceholder.value = props.placeholder.slice(0, currentIndex);
    currentIndex++;
    typewriterInterval = setTimeout(typeWriter, TYPING_SPEED);
  } else if (!isDeleting && currentIndex > props.placeholder.length) {
    typewriterInterval = setTimeout(() => {
      isDeleting = true;
      typeWriter();
    }, PAUSE_BEFORE_DELETE);
  } else if (isDeleting && currentIndex > 0) {
    currentIndex--;
    currentPlaceholder.value = props.placeholder.slice(0, currentIndex);
    typewriterInterval = setTimeout(typeWriter, DELETING_SPEED);
  } else if (isDeleting && currentIndex === 0) {
    isDeleting = false;
    typewriterInterval = setTimeout(typeWriter, PAUSE_BEFORE_RESTART);
  }
};

onMounted(() => {
  // Start with empty placeholder
  currentPlaceholder.value = '';
  currentIndex = 0;
  isDeleting = false;
  // Start the typewriter effect
  typeWriter();
});

onUnmounted(() => {
  // Clean up any existing interval
  if (typewriterInterval) {
    clearTimeout(typewriterInterval);
  }
});
</script>

<style scoped>
.input-container {
  position: relative;
  width: 100%;
  margin-bottom: 8px;
}

.n-input {
  font-family: 'BM Jua';
  margin-bottom: 4px;
  z-index: 100;
}

.error-message {
  position: absolute;
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
  font-family: 'BM Jua';
  z-index: 101;
}
</style> 