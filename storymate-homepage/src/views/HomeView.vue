<script setup lang="ts">
import Author from '../components/Author.vue'
import Demo from '../components/Demo.vue'

const scrollToDemo = () => {
  const demoSection = document.getElementById('demo-section');
  if (demoSection) {
    demoSection.scrollIntoView({ behavior: 'smooth' });
  }
}
</script>

<template>
  <main class="container">
    <div class="hero-body">
      <div class="row center">
        <div class="title-container">
          <img src="/imgs/logo-chi2025.svg" alt="CHI 2025 Logo" class="chi-logo" />
          <h1 style="font-size: 40px;">
              Characterizing LLM-Empowered Personalized Story-Reading and Interaction for Children: 
              <br>
              Insights from Multi-Stakeholder Perspectives
          </h1>
        </div>
      </div>
      <div class="row center" style="margin-bottom: 16px;">
        <h2 style="font-size:30px; font-weight: 400; color: #333; margin-top: 6px;">
            [CHI'25 Accepted]
        </h2>
      </div>
      <div class="row center author-row">
        <Author author="Jiaju Chen" href="https://malcolm-chen.github.io/"sup="1" />, <Author author="Minglong Tang" sup="1" />,
        <Author author="Yuxuan Lu" href="https://yuxuan.lu/" sup="2" />,
        <Author author="Bingsheng Yao" href="https://www.bingshengyao.com/" sup="2" />,
        <Author author="Elissa Fan" sup="3" />, 
        <Author author="Xiaojuan Ma" href="https://www.cse.ust.hk/~mxj/" sup="4" />,
      </div>
      <div class="row center">
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
        <pre>jiajuchen89@gmail.com</pre>
        <pre>ylsun@cs.ecnu.edu.cn</pre>
      </div>
      <div class="row center" style="margin-top: 48px; margin-bottom: 48px;">
      <a href="https://arxiv.org/abs/2503.00590" target="_blank">
        <n-button round>
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
        <n-button round>
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
      <n-button round @click="scrollToDemo">
        <template #icon>
          <n-icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path fill="currentColor" d="M8 5v14l11-7z"/>
            </svg>
          </n-icon>
        </template>
        Try Demo
      </n-button>
    </div>
    <div class="row center">
      <img src="../assets/teaser.png" alt="teaser" style="width: 80%; margin-bottom: 48px" />
    </div>
    <div class="row center">
      <p class="text-lg text-justify">
        Personalized interaction is highly valued by parents in their story-reading activities with children. While AI-empowered story-reading tools have been increasingly used, their abilities to support personalized interaction with children are still limited. Recent advances in large language models (LLMs) show promise in facilitating personalized interactions, but little is known about how to effectively and appropriately use LLMs to enhance children's personalized story-reading experiences. This work explores this question through a design-based study. Drawing on a formative study, we designed and developed StoryMate, an LLM-empowered personalized interactive story-reading tool for children, following an empirical study with children, parents, and education experts. Our participants valued the personalized features in StoryMate, and also highlighted the need to support personalized content, guiding mechanisms, reading context variations, and interactive interfaces. Based on these findings, we propose a series of design recommendations for better using LLMs to empower children's personalized story reading and interaction.
      </p>
    </div>
    <div class="row center">
        <h2>
            StoryMate's Demo
        </h2>
    </div>
    <div class="row center">
        <p style="font-size: 18px; font-weight: 300; color: #333;">
            We have updated StoryMate with a new UI with faster response 😎 Try it out!
        </p>
    </div>
    <div class="row center" id="demo-section">
        <Demo />
    </div>
    <div class="row center">
        <h2>
            Citation
        </h2>
    </div>
    <div class="row center">
        <div class="citation">
            <pre class="citation-text">
@inproceedings{chen2025storymate,
  author    = {Jiaju Chen and Minglong Tang and Yuxuan Lu and Bingsheng Yao and Elissa Fan and Xiaojuan Ma and Ying Xu and Dakuo Wang and Yuling Sun and Liang He},
  title     = {StoryMate: An LLM-Empowered Personalized Interactive Story-Reading Tool for Children},
  booktitle = {Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems},
  year      = {2025},
  month     = {April},
  location  = {Yokohama, Japan},
  publisher = {ACM},
  doi       = {10.1145/3706598.3713275},
  isbn      = {979-8-4007-1394-1},
}</pre>
        </div>
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
  }
}

.citation {
  margin: 32px 0;
  width: 80%;
  max-width: 800px;

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
</style>