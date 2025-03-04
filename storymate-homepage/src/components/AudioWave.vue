<template>
  <div class="wave-container">
    <div class="wave-bar" v-for="n in 10" :key="n"></div>
  </div>
</template>

<style scoped>
.wave-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 100%;
}

.wave-bar {
  width: 4px;
  height: 20px;
  background-color: #7AA2E3;
  border-radius: 2px;
  animation: wave 1s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% {
    height: 20px;
  }
  50% {
    height: 40px;
  }
}

/* Add different animation delays for each bar */
.wave-bar:nth-child(1) { animation-delay: -0.9s; }
.wave-bar:nth-child(2) { animation-delay: -0.8s; }
.wave-bar:nth-child(3) { animation-delay: -0.7s; }
.wave-bar:nth-child(4) { animation-delay: -0.6s; }
.wave-bar:nth-child(5) { animation-delay: -0.5s; }
.wave-bar:nth-child(6) { animation-delay: -0.4s; }
.wave-bar:nth-child(7) { animation-delay: -0.3s; }
.wave-bar:nth-child(8) { animation-delay: -0.2s; }
.wave-bar:nth-child(9) { animation-delay: -0.1s; }
.wave-bar:nth-child(10) { animation-delay: 0s; }
</style> 