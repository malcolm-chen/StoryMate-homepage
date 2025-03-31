<script setup lang="ts">
import Author from '../components/Author.vue'
import Demo from '../components/Demo.vue'
import { ref } from 'vue'

const citationText = ref<HTMLPreElement | null>(null)
const isCopied = ref(false)

const openLink = (url: string) => {
  window.open(url, '_blank')
}

const copyCitation = () => {
  if (citationText.value?.textContent) {
    const text = citationText.value.textContent
    navigator.clipboard
      .writeText(text)
      .then(() => {
        isCopied.value = true
        setTimeout(() => {
          isCopied.value = false
        }, 2000)
      })
      .catch((err) => {
        console.error('Failed to copy text: ', err)
      })
  }
}

const scrollToDemo = () => {
  const demoSection = document.getElementById('demo-section');
  if (demoSection) {
    demoSection.scrollIntoView({ behavior: 'smooth' });
  }
}

const scrollToRW = () => {
  const rwSection = document.getElementById('rw-section');
  if (rwSection) {
    rwSection.scrollIntoView({ behavior: 'smooth' });
  }
}
</script>

<template>
  <main class="container">
    <div class="hero-body">
      <div class="row center">
        <img src="/imgs/logo-chi2025.svg" alt="CHI 2025 Logo" class="chi-logo" />
      </div>
      <div class="row center">
          <h1 style="font-size: 35px;">
              Characterizing LLM-Empowered Personalized Story-Reading and Interaction for Children: 
              <br>
              Insights from Multi-Stakeholder Perspectives
          </h1>
      </div>
      <div class="row center" style="margin-bottom: 16px;">
        <h2 style="font-size:30px; font-weight: 400; margin-top: 6px; color: #EA6D93; display: flex; align-items: center; justify-content: center; gap: 8px;">
            <img src="/imgs/sakura.png" alt="sakura" style="width: 24px; height: 24px;" />
            [CHI'25 Accepted]
            <img src="/imgs/sakura.png" alt="sakura" style="width: 24px; height: 24px;" />
        </h2>
      </div>
      <div class="row center author-row">
        <Author author="Jiaju Chen" href="https://malcolm-chen.github.io/"sup="1" />, <Author author="Minglong Tang" sup="1" />,
        <Author author="Yuxuan Lu" href="https://yuxuan.lu/" sup="2" />,
        <Author author="Bingsheng Yao" href="https://www.bingshengyao.com/" sup="2" />,
        <Author author="Elissa Fan" sup="3" />, 
        <Author author="Xiaojuan Ma" href="https://www.cse.ust.hk/~mxj/" sup="4" />,
        <Author author="Ying Xu" href="https://ying-xu.com/" sup="5" />, 
        <Author author="Dakuo Wang" href="https://www.dakuowang.com/" sup="2" />,
        <Author author="Yuling Sun" href="https://www.yulingsun.net/" sup="1" />, 
        <Author author="Liang He" sup="1" />.
      </div>
      <div class="row center text-lg">
        <div class="affiliation"><sup>1</sup>East China Normal University</div>
        <div class="affiliation"><sup>2</sup>Northeastern University</div>
        <div class="affiliation"><sup>3</sup>Lexington High School</div>
        <div class="affiliation"><sup>4</sup>Hong Kong University of Science and Technology</div>
        <div class="affiliation"><sup>5</sup>Harvard University</div>
      </div>
      <div class="row center">
        <pre>10205102450@stu.ecnu.edu.cn</pre>
        <pre>ylsun@cs.ecnu.edu.cn</pre>
      </div>
    </div>
      <div class="row center" style="margin-top: 48px; margin-bottom: 48px;">
      <a href="https://arxiv.org/abs/2503.00590" target="_blank">
        <n-button round type="info">
          <template #icon>
            <n-icon>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 16 16"
              >
                <g fill="none">
                  <path
                    d="M4.5 9.003a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 1 0v-.166h.333a1.167 1.167 0 0 0 0-2.334H4.5zm.833 1.334H5v-.334h.333a.167.167 0 0 1 0 .334zm4.668-.835a.5.5 0 0 1 .5-.499h.998a.5.5 0 0 1 0 1h-.5v.335h.5a.5.5 0 1 1 0 1H11v.164a.5.5 0 0 1-1 .002L10 10.837L10 9.502zm-2.503-.499a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5H8a1.5 1.5 0 0 0 0-3h-.502zm.5 2v-1H8a.5.5 0 0 1 0 1h-.002zM9 2.002H4.5a1.5 1.5 0 0 0-1.5 1.5v3.582A1.5 1.5 0 0 0 2 8.5v4.003a1.5 1.5 0 0 0 1.5 1.5h9a1.5 1.5 0 0 0 1.5-1.5V8.499a1.5 1.5 0 0 0-1-1.415V6h-2.5A1.5 1.5 0 0 1 9 4.5V2.002zM3.5 7.999h9a.5.5 0 0 1 .5.5v4.003a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V8.499a.5.5 0 0 1 .5-.5zm9.206-3H10.5a.5.5 0 0 1-.5-.5V2.298L12.706 5z"
                    fill="currentColor"
                  ></path>
                </g>
              </svg>
            </n-icon>
          </template>
          Paper
        </n-button>
      </a>
      <a href="https://github.com/neuhai/storymate" target="_blank">
        <n-button round type="info">
          <template #icon>
            <n-icon>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 496 512"
              >
                <path
                  d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6c-3.3.3-5.6-1.3-5.6-3.6c0-2 2.3-3.6 5.2-3.6c3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9c2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9c.3 2 2.9 3.3 5.9 2.6c2.9-.7 4.9-2.6 4.6-4.6c-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2c12.8 2.3 17.3-5.6 17.3-12.1c0-6.2-.3-40.4-.3-61.4c0 0-70 15-84.7-29.8c0 0-11.4-29.1-27.8-36.6c0 0-22.9-15.7 1.6-15.4c0 0 24.9 2 38.6 25.8c21.9 38.6 58.6 27.5 72.9 20.9c2.3-16 8.8-27.1 16-33.7c-55.9-6.2-112.3-14.3-112.3-110.5c0-27.5 7.6-41.3 23.6-58.9c-2.6-6.5-11.1-33.3 2.6-67.9c20.9-6.5 69 27 69 27c20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27c13.7 34.7 5.2 61.4 2.6 67.9c16 17.7 25.8 31.5 25.8 58.9c0 96.5-58.9 104.2-114.8 110.5c9.2 7.9 17 22.9 17 46.4c0 33.7-.3 75.4-.3 83.6c0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252C496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2c1.6 1.6 3.9 2.3 5.2 1c1.3-1 1-3.3-.7-5.2c-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9c1.6 1 3.6.7 4.3-.7c.7-1.3-.3-2.9-2.3-3.9c-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2c2.3 2.3 5.2 2.6 6.5 1c1.3-1.3.7-4.3-1.3-6.2c-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9c1.6 2.3 4.3 3.3 5.6 2.3c1.6-1.3 1.6-3.9 0-6.2c-1.4-2.3-4-3.3-5.6-2z"
                  fill="currentColor"
                ></path>
              </svg>
            </n-icon>
          </template>
          Code
        </n-button>
      </a>
      <n-button round type="info" @click="scrollToDemo">
        <template #icon>
          <n-icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path fill="currentColor" d="M8 5v14l11-7z"/>
            </svg>
          </n-icon>
        </template>
        Try Demo
      </n-button>
      <n-button round type="info" @click="scrollToRW">
        <template #icon>
          <n-icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path fill="currentColor" d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/>
            </svg>
          </n-icon>
        </template>
        Related Work
      </n-button>
    </div>
    <div class="row center flex-wrap">
      <div class="flex-0" style="flex-basis: 300px">
        <img src="@/assets/arxiv.png" alt="teaser" style="width: 100%" />
      </div>
      <div class="flex-1 bg-gray-100 p-4 rounded-lg" style="flex-basis: 600px; max-width: 100%">
        <p class="text-lg text-align-left">
          Personalized interaction is highly valued by parents in their story-reading activities with children. While AI-empowered story-reading tools have been increasingly used, their abilities to support personalized interaction with children are still limited. Recent advances in large language models (LLMs) show promise in facilitating personalized interactions, but little is known about how to effectively and appropriately use LLMs to enhance children's personalized story-reading experiences. This work explores this question through a design-based study. Drawing on a formative study, we designed and developed <span style="font-weight: 1000;">StoryMate</span>, an LLM-empowered personalized interactive story-reading tool for children, following an empirical study with children, parents, and education experts. Our participants valued the personalized features in StoryMate, and also highlighted the need to support personalized content, guiding mechanisms, reading context variations, and interactive interfaces. Based on these findings, we propose a series of design recommendations for better using LLMs to empower children's personalized story reading and interaction.
        </p>
      </div>
    </div>
    <div class="row center">
        <h2>
            StoryMate's Demo
        </h2>
    </div>
    <div class="row center">
        <p style="font-size: 18px; font-weight: 300; color: #333;">
            We have updated StoryMate's UI with faster response 😎 Imagine yourself as a kid and try our demo!
        </p>
    </div>
    <div class="row center" id="demo-section">
        <Demo />
    </div>
    <div class="row center text-lg text-align-left bg-gray-100 p-4 rounded-lg">
      <div style="padding: 10px 0; ">
        <p>
          <span style="font-weight: 1000;">StoryMate</span> is a interactive story-reading tool that uses Large Language Model
          (LLMs) to provide personalized story reading and interaction for children. Specifically, it has four main features:
        </p>
        <ul style="list-style-type: disc; margin-left: 30px;">
          <li>Customizable reading content and modes.</li>
          <li>Child-appropriate, adaptive, and personalized interaction.</li>
          <li>Embedded attention-getting mechanisms.</li>
          <li>RAG-based guided conversation for active thinking.</li>
        </ul>
      </div>
    </div>
    <div class="row center" id="rw-section">
      <h2>Check out our related work</h2>
    </div>
    <div class="row center">
      <n-card>
        <h3 style="font-size: 20px; font-weight: 600;">
          <span style="color: oklch(.623 .214 259.815); font-weight: 600;">[Accepted at EMNLP 2024]</span>
          <br>
          StorySparkQA: Expert-Annotated QA Pairs with Real-World Knowledge for Children's Story-Based Learning
        </h3>
        <div>
          <a href="https://malcolm-chen.github.io/" style="color: oklch(.623 .214 259.815);">Jiaju Chen</a>, 
          <a href="https://yuxuan.lu/" style="color: oklch(.623 .214 259.815);">Yuxuan Lu</a>,
          <a href="https://shaozhang.info/" style="color: oklch(.623 .214 259.815);">Shao Zhang</a>, 
          <a href="https://www.bingshengyao.com/" style="color: oklch(.623 .214 259.815);">Bingsheng Yao</a>,
          Yuanzhe Dong,
          <a href="https://ying-xu.com/" style="color: oklch(.623 .214 259.815);">Ying Xu</a>, 
          Yunyao Li,
          <a href="https://qianwen.info/" style="color: oklch(.623 .214 259.815);">Qianwen Wang</a>,
          <a href="https://www.dakuowang.com/" style="color: oklch(.623 .214 259.815);">Dakuo Wang</a>,
          <a href="https://www.yulingsun.net/" style="color: oklch(.623 .214 259.815);">Yuling Sun</a>.
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0;">
          <a href="https://arxiv.org/abs/2311.09756" target="_blank">
            <n-button round type="info">
              <template #icon>
                <n-icon>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    viewBox="0 0 16 16"
                  >
                    <g fill="none">
                      <path
                        d="M4.5 9.003a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 1 0v-.166h.333a1.167 1.167 0 0 0 0-2.334H4.5zm.833 1.334H5v-.334h.333a.167.167 0 0 1 0 .334zm4.668-.835a.5.5 0 0 1 .5-.499h.998a.5.5 0 0 1 0 1h-.5v.335h.5a.5.5 0 1 1 0 1H11v.164a.5.5 0 0 1-1 .002L10 10.837L10 9.502zm-2.503-.499a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5H8a1.5 1.5 0 0 0 0-3h-.502zm.5 2v-1H8a.5.5 0 0 1 0 1h-.002zM9 2.002H4.5a1.5 1.5 0 0 0-1.5 1.5v3.582A1.5 1.5 0 0 0 2 8.5v4.003a1.5 1.5 0 0 0 1.5 1.5h9a1.5 1.5 0 0 0 1.5-1.5V8.499a1.5 1.5 0 0 0-1-1.415V6h-2.5A1.5 1.5 0 0 1 9 4.5V2.002zM3.5 7.999h9a.5.5 0 0 1 .5.5v4.003a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V8.499a.5.5 0 0 1 .5-.5zm9.206-3H10.5a.5.5 0 0 1-.5-.5V2.298L12.706 5z"
                        fill="currentColor"
                      ></path>
                    </g>
                  </svg>
                </n-icon>
              </template>
              Paper
            </n-button>
          </a>
          <a href="https://github.com/neuhai/StorySparkQA" target="_blank">
            <n-button round type="info">
              <template #icon>
                <n-icon>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    viewBox="0 0 496 512"
                  >
                    <path
                      d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6c-3.3.3-5.6-1.3-5.6-3.6c0-2 2.3-3.6 5.2-3.6c3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9c2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9c.3 2 2.9 3.3 5.9 2.6c2.9-.7 4.9-2.6 4.6-4.6c-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2c12.8 2.3 17.3-5.6 17.3-12.1c0-6.2-.3-40.4-.3-61.4c0 0-70 15-84.7-29.8c0 0-11.4-29.1-27.8-36.6c0 0-22.9-15.7 1.6-15.4c0 0 24.9 2 38.6 25.8c21.9 38.6 58.6 27.5 72.9 20.9c2.3-16 8.8-27.1 16-33.7c-55.9-6.2-112.3-14.3-112.3-110.5c0-27.5 7.6-41.3 23.6-58.9c-2.6-6.5-11.1-33.3 2.6-67.9c20.9-6.5 69 27 69 27c20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27c13.7 34.7 5.2 61.4 2.6 67.9c16 17.7 25.8 31.5 25.8 58.9c0 96.5-58.9 104.2-114.8 110.5c9.2 7.9 17 22.9 17 46.4c0 33.7-.3 75.4-.3 83.6c0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252C496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2c1.6 1.6 3.9 2.3 5.2 1c1.3-1 1-3.3-.7-5.2c-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9c1.6 1 3.6.7 4.3-.7c.7-1.3-.3-2.9-2.3-3.9c-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2c2.3 2.3 5.2 2.6 6.5 1c1.3-1.3.7-4.3-1.3-6.2c-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9c1.6 2.3 4.3 3.3 5.6 2.3c1.6-1.3 1.6-3.9 0-6.2c-1.4-2.3-4-3.3-5.6-2z"
                      fill="currentColor"
                    ></path>
                  </svg>
                </n-icon>
              </template>
              Code
            </n-button>
          </a>
          <a href="https://huggingface.co/datasets/NEU-HAI/StorySparkQA" target="_blank">
            <n-button round type="info">
              <template #icon>
                <n-icon>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4m0 2c3.71 0 6 1.56 6 2s-2.29 2-6 2-6-1.56-6-2 2.29-2 6-2M6 8.27C7.38 9.34 9.55 10 12 10s4.62-.66 6-1.73V11c0 .44-2.29 2-6 2s-6-1.56-6-2V8.27M6 12.27C7.38 13.34 9.55 14 12 14s4.62-.66 6-1.73V15c0 .44-2.29 2-6 2s-6-1.56-6-2v-2.73m0 4C7.38 17.34 9.55 18 12 18s4.62-.66 6-1.73V17c0 .44-2.29 2-6 2s-6-1.56-6-2v-2.73Z"/>
                  </svg>
                </n-icon>
              </template>
              Dataset
            </n-button>
          </a>
        </div>
        <p class="flex-1 bg-gray-100 p-4 rounded-lg" >
          Interactive story reading is a common parent-child activity, where parents expect to teach both language skills and real-world knowledge beyond the story. While increasing storytelling and reading systems have been developed for this activity, they often fail to infuse real-world knowledge into the conversation. This limitation can be attributed to the existing question-answering (QA) datasets used for children's education, upon which the systems are built, failing to capture the nuances of how education experts think when conducting interactive story reading activities. To bridge this gap, we design an annotation framework, empowered by existing knowledge graph to capture experts' annotations and thinking process, and leverage this framework to construct StorySparkQA dataset, which comprises 5,868 expert-annotated QA pairs with real-world knowledge. We conduct automated and human expert evaluations across various QA pair generation settings to demonstrate that our StorySparkQA can effectively support models in generating QA pairs that target real-world knowledge beyond story content.
        </p>
        <n-carousel 
          effect="card"
          style="height: 300px; cursor: pointer; touch-action: pan-y pinch-zoom;"
          :draggable="true"
          :mousewheel="true"
          :loop="true"
          :show-arrow="true"
          :slides-per-view="1"
          :space-between="20"
          :touch-drag-ratio="1"
          :transition-props="{ name: 'fade', duration: 100 }"
        >
          <n-carousel-item style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content" @click="openLink('https://arxiv.org/abs/2311.09756')">
              <img src="../assets/storyspark/dataset.png" class="carousel-img" alt="storysparkqa" />
              <p class="carousel-caption">A datapoint from StorySparkQA.</p>
            </div>
          </n-carousel-item>
          <n-carousel-item style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content" @click="openLink('https://arxiv.org/abs/2311.09756')">
              <img src="../assets/storyspark/split stats.png" class="carousel-img" alt="storysparkqa" />
              <p class="carousel-caption">Statistics of StorySparkQA.</p>
            </div>
          </n-carousel-item>
          <n-carousel-item style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content" @click="openLink('https://arxiv.org/abs/2311.09756')">
              <img src="../assets/storyspark/workflow.png" class="carousel-img" alt="storysparkqa" />
              <p class="carousel-caption">Workflow of StorySparkQA's annotation process.</p>
            </div>
          </n-carousel-item>
          <n-carousel-item style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content" @click="openLink('https://arxiv.org/abs/2311.09756')">
              <img src="../assets/storyspark/annotation.png" class="carousel-img" alt="storysparkqa" />
              <p class="carousel-caption">The user interface of StorySparkQA's annotation framework.</p>
            </div>
          </n-carousel-item>
        </n-carousel>
      </n-card>
      <n-card>
        <h3 style="font-size: 20px; font-weight: 600;">
          <span style="color: oklch(.623 .214 259.815); font-weight: 600;">[Accepted at CSCW 2024]</span>
          <br>
          Exploring Parent's Needs for Children-Centered AI to Support Preschoolers' Interactive Storytelling and Reading Activities
        </h3>
        <div>
          <a href="https://www.yulingsun.net/" style="color: oklch(.623 .214 259.815);">Yuling Sun</a>, 
          <a href="https://malcolm-chen.github.io/" style="color: oklch(.623 .214 259.815);">Jiaju Chen</a>, 
          <a href="https://www.bingshengyao.com/" style="color: oklch(.623 .214 259.815);">Bingsheng Yao</a>, 
          Jiali Liu, 
          <a href="https://www.dakuowang.com/" style="color: oklch(.623 .214 259.815);">Dakuo Wang</a>, 
          <a href="https://www.cse.ust.hk/~mxj/" style="color: oklch(.623 .214 259.815);">Xiaojuan Ma</a>,
          <a href="https://yuxuan.lu/" style="color: oklch(.623 .214 259.815);">Yuxuan Lu</a>,
          <a href="https://ying-xu.com/" style="color: oklch(.623 .214 259.815);">Ying Xu</a>, 
          Liang He.
        </div>
        <div style="display: flex; gap: 16px; margin: 16px 0;">
          <a href="https://arxiv.org/abs/2401.13804" target="_blank">
            <n-button round type="info">
              <template #icon>
                <n-icon>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    viewBox="0 0 16 16"
                  >
                    <g fill="none">
                      <path
                        d="M4.5 9.003a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 1 0v-.166h.333a1.167 1.167 0 0 0 0-2.334H4.5zm.833 1.334H5v-.334h.333a.167.167 0 0 1 0 .334zm4.668-.835a.5.5 0 0 1 .5-.499h.998a.5.5 0 0 1 0 1h-.5v.335h.5a.5.5 0 1 1 0 1H11v.164a.5.5 0 0 1-1 .002L10 10.837L10 9.502zm-2.503-.499a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5H8a1.5 1.5 0 0 0 0-3h-.502zm.5 2v-1H8a.5.5 0 0 1 0 1h-.002zM9 2.002H4.5a1.5 1.5 0 0 0-1.5 1.5v3.582A1.5 1.5 0 0 0 2 8.5v4.003a1.5 1.5 0 0 0 1.5 1.5h9a1.5 1.5 0 0 0 1.5-1.5V8.499a1.5 1.5 0 0 0-1-1.415V6h-2.5A1.5 1.5 0 0 1 9 4.5V2.002zM3.5 7.999h9a.5.5 0 0 1 .5.5v4.003a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V8.499a.5.5 0 0 1 .5-.5zm9.206-3H10.5a.5.5 0 0 1-.5-.5V2.298L12.706 5z"
                        fill="currentColor"
                      ></path>
                    </g>
                  </svg>
                </n-icon>
              </template>
              Paper
            </n-button>
          </a>
        </div>
        <p class="flex-1 bg-gray-100 p-4 rounded-lg">
          Interactive storytelling is vital for preschooler development. While children's interactive partners have traditionally been their parents and teachers, recent advances in artificial intelligence (AI) have sparked a surge of AI-based storytelling and reading technologies. As these technologies become increasingly ubiquitous in preschoolers' lives, questions arise regarding how they function in practical storytelling and reading scenarios and, how parents, the most critical stakeholders, experience and perceive these technologies. This paper investigates these questions through a qualitative study with 17 parents of children aged 3-6. Our findings suggest that even though AI-based storytelling and reading technologies provide more immersive and engaging interaction, they still cannot meet parents' expectations due to a series of interactive and algorithmic challenges. We elaborate on these challenges and discuss the possible implications of future AI-based interactive storytelling technologies for preschoolers.
        </p>
        <n-carousel>
          <n-carousel-item style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content" @click="openLink('https://arxiv.org/abs/2401.13804')">
              <img src="../assets/cscw/tools.png" style="max-height: 500px; margin-top: 12px;" alt="tools" />
              <p class="carousel-caption">Some AI-based storytelling technologies reported by participants.</p>
            </div>
          </n-carousel-item>
        </n-carousel>
      </n-card>
      <n-card>
        <h3 style="font-size: 20px; font-weight: 600;">
          <span style="color: oklch(.623 .214 259.815); font-weight: 600;">[Accepted at CHI 2025]</span>
          <br>
          Live-Streaming-Based Dual-Teacher Classes for Equitable Education: Insights and Challenges From Local Teachers' Perspective in Disadvantaged Areas
        </h3>
        <div>
          <a href="https://www.yulingsun.net/" style="color: oklch(.623 .214 259.815);">Yuling Sun</a>, 
          <a href="https://malcolm-chen.github.io/" style="color: oklch(.623 .214 259.815);">Jiaju Chen</a>, 
          Xiaomu Zhou,
          <a href="https://www.cse.ust.hk/~mxj/" style="color: oklch(.623 .214 259.815);">Xiaojuan Ma</a>,
          <a href="https://www.bingshengyao.com/" style="color: oklch(.623 .214 259.815);">Bingsheng Yao</a>, 
          Kai Zhang, Liang He,
          <a href="https://www.dakuowang.com/" style="color: oklch(.623 .214 259.815);">Dakuo Wang</a>.
        </div>
        <div style="display: flex; gap: 16px; margin: 16px 0;">
          <a href="https://arxiv.org/abs/2401.13799" target="_blank">
            <n-button round type="info">
              <template #icon>
                <n-icon>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    viewBox="0 0 16 16"
                  >
                    <g fill="none">
                      <path
                        d="M4.5 9.003a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 1 0v-.166h.333a1.167 1.167 0 0 0 0-2.334H4.5zm.833 1.334H5v-.334h.333a.167.167 0 0 1 0 .334zm4.668-.835a.5.5 0 0 1 .5-.499h.998a.5.5 0 0 1 0 1h-.5v.335h.5a.5.5 0 1 1 0 1H11v.164a.5.5 0 0 1-1 .002L10 10.837L10 9.502zm-2.503-.499a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5H8a1.5 1.5 0 0 0 0-3h-.502zm.5 2v-1H8a.5.5 0 0 1 0 1h-.002zM9 2.002H4.5a1.5 1.5 0 0 0-1.5 1.5v3.582A1.5 1.5 0 0 0 2 8.5v4.003a1.5 1.5 0 0 0 1.5 1.5h9a1.5 1.5 0 0 0 1.5-1.5V8.499a1.5 1.5 0 0 0-1-1.415V6h-2.5A1.5 1.5 0 0 1 9 4.5V2.002zM3.5 7.999h9a.5.5 0 0 1 .5.5v4.003a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V8.499a.5.5 0 0 1 .5-.5zm9.206-3H10.5a.5.5 0 0 1-.5-.5V2.298L12.706 5z"
                        fill="currentColor"
                      ></path>
                    </g>
                  </svg>
                </n-icon>
              </template>
              Paper
            </n-button>
          </a>
        </div>
        <p class="flex-1 bg-gray-100 p-4 rounded-lg" >
          Educational inequalities in disadvantaged areas have long been a global concern. While Information and Communication Tech- nologies (ICTs) have shown great potential in addressing this is- sue, the unique challenges in disadvantaged areas often hinder the practical effectiveness of such technologies. This paper exam- ines live-streaming-based dual-teacher classes (LSDC) through a qualitative study in disadvantaged regions of China. Our findings indicate that, although LSDC offers students in these regions access to high-quality educational resources, its practical implementation is fraught with challenges. Specifically, we foreground the pivotal role of local teachers in mitigating these challenges. Through a series of situated efforts, local teachers contextualize high-quality lectures to the local classroom environment, ensuring the expected educational outcomes. Based on our findings, we argue that greater recognition and support for the situational practices of local teach- ers is essential for fostering a more equitable, sustainable, and scalable technology-driven educational model in disadvantaged areas.
        </p>
        <n-carousel
          effect="card"
          style="height: 300px; cursor: pointer; touch-action: pan-y pinch-zoom;"
          :draggable="true"
          :touchable="true"
          :mousewheel="true"
          :loop="true"
          :show-arrow="true"
          :slides-per-view="1"
          :space-between="20"
          :touch-drag-ratio="1"
          :transition-props="{ name: 'fade', duration: 100 }"
        >
          <n-carousel-item  @click="openLink('https://arxiv.org/abs/2401.13799')" style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content">
              <img src="../assets/lsdc/onescreen.png" class="carousel-img" alt="tools" />
              <p class="carousel-caption">One Screen Initiative in China.</p>
            </div>
          </n-carousel-item>
          <n-carousel-item  @click="openLink('https://arxiv.org/abs/2401.13799')" style="width: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 0 20px;">
            <div class="carousel-item-content">
              <img src="../assets/lsdc/sketches.png" class="carousel-img" alt="tools" />
              <p class="carousel-caption">The sketches of live-streaming-based dual-teacher classes (LSDC).</p>
            </div>
          </n-carousel-item>
        </n-carousel>
      </n-card>
    </div>
    <div class="row center">
      <div class="citation">
        <h3>Citation</h3>
        <h4 style="margin-bottom: 8px; font-size: 16px; font-weight: 600;">🐧 StoryMate</h4>
        <pre class="citation-text" ref="citationText">
@inproceedings{chen2025storymate,
  author    = {Jiaju Chen and Minglong Tang and Yuxuan Lu and Bingsheng Yao and Elissa Fan and Xiaojuan Ma and Ying Xu and Dakuo Wang and Yuling Sun and Liang He},
  title     = {Characterizing LLM-Empowered Personalized Story-Reading and Interaction for Children: Insights from Multi-Stakeholder Perspectives},
  booktitle = {Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems},
  year      = {2025},
  month     = {April},
  location  = {Yokohama, Japan},
  publisher = {ACM},
  doi       = {10.1145/3706598.3713275},
  isbn      = {979-8-4007-1394-1},
}</pre>
        <n-button quaternary circle size="tiny" class="copy-button"  @click="copyCitation">
          <template #icon>
            <n-icon>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 24 24"
              >
                <path
                  d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
                  fill="currentColor"
                ></path>
              </svg>
            </n-icon>
          </template>
        </n-button>
      </div> 
    </div>
    <div class="row center">
      <div class="citation">
        <h4 style="margin-bottom: 8px; font-size: 16px; font-weight: 600;">✨ StorySparkQA</h4>
        <pre class="citation-text" ref="citationText">
@inproceedings{chen-etal-2024-storysparkqa,
  title = "{S}tory{S}park{QA}: Expert-Annotated {QA} Pairs with Real-World Knowledge for Children`s Story-Based Learning",
  author = "Chen, Jiaju and Lu, Yuxuan and Zhang, Shao and Yao, Bingsheng and Dong, Yuanzhe and Xu, Ying and Li, Yunyao and Wang, Qianwen and Wang, Dakuo and Sun, Yuling",
  booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
  month = nov,
  year = "2024",
  address = "Miami, Florida, USA",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2024.emnlp-main.961/",
  doi = "10.18653/v1/2024.emnlp-main.961",
  pages = "17351--17370",
}</pre>
        <n-button quaternary circle size="tiny" class="copy-button-2" @click="copyCitation">
          <template #icon>
            <n-icon>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 24 24"
              >
                <path
                  d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
                  fill="currentColor"
                ></path>
              </svg>
            </n-icon>
          </template>
        </n-button>
      </div> 
    </div>
  </main>
</template>

<style scoped lang="scss">
h2 {
  margin-top: 48px;
  font-size: 32px;
  font-weight: 700;
  color: #333;
  text-align: center;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
}
.hero-body {
  margin: 48px 24px;

  .author-row {
    flex-wrap: wrap;
    column-gap: 0px;
  }
  h1 {
    font-size: 48px;
    font-weight: 700;
    color: #333;
    text-align: center;
  }
  .affiliation {
    font-size: 16px;
    font-weight: 400;
    color: #333;
    text-align: center;
    margin-right: 16px;
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
}

.title-container {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  max-width: 100%;
  justify-content: center;
  flex-wrap: nowrap;
}

.chi-logo {
  height: 60px;
  width: auto;
  flex-shrink: 0;
  margin-top: 0.2em;
}

h1 {
  font-size: 40px;
  font-weight: 700;
  color: #333;
  text-align: left;
  margin: 0;
  flex: 1;
  line-height: 1.2;
}

.citation {
  margin: 32px 0;
  width: 80%;
  max-width: 800px;
  position: relative;

  h3 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin-bottom: 16px;
    text-align: center;
  }

  .citation-text {
    background-color: #f5f5f5;
    padding: 16px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 14px;
    overflow-x: auto;
    white-space: pre-wrap;
    text-align: left;
  }

  .copy-button {
    font-size: 24px;
    position: absolute;
    top: calc(1.6 * 24px + 16px + 10px + 30px);
    right: 10px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: #e0e0e0;
    }

    &.copied {
      background-color: #4caf50;
      color: white;
    }
  }

  .copy-button-2 {
    font-size: 24px;
    position: absolute;
    top: calc(10px + 30px);
    right: 10px;
    &:hover {
      background-color: #e0e0e0;
    }

    &.copied {
      background-color: #4caf50;
      color: white;
    }
  }
}

.row.center {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 8px;
    padding: 0 16px;
}

.carousel-img {
  margin: 0 auto;
  height: 240px;
  width: auto;
  object-fit: contain;
  cursor: pointer;
}

.carousel-caption {
  font-size: 14px;
  font-weight: 500;
  color: #424242;
  text-align: center;
  margin-top: 6px;
}

.carousel-item-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  touch-action: pan-y pinch-zoom;
  user-select: none;
  -webkit-user-drag: none;
}

:deep(.n-carousel.n-carousel--card) {
  .n-carousel__dots {
    bottom: -20px;
  }
  
  .n-carousel__arrow {
    font-size: 24px;
    background-color: rgba(0, 0, 0, 0.2);
    z-index: 2;
    
    &:hover {
      background-color: rgba(0, 0, 0, 0.4);
    }
  }

  .n-carousel__slides {
    touch-action: pan-y pinch-zoom;
    
    .n-carousel__slide {
      touch-action: pan-y pinch-zoom;
      user-select: none;
      -webkit-user-drag: none;
      
      &:not(.n-carousel__slide--current) {
        opacity: 0.13;
        filter: blur(1px);
      }
    }
  }
}
</style>