<script setup>
import { ref, onMounted, computed } from 'vue';
import { WavRecorder, WavStreamPlayer } from '../lib/wavtools/index';
import { RealtimeClient } from '@openai/realtime-api-beta';
import { NIcon, NButton, NAvatar } from 'naive-ui';
import { LoadingOutlined } from "@vicons/antd";
import { PlayCircle, PauseCircle, ChevronCircleUp, ChevronCircleDown, MinusCircle } from "@vicons/fa";
import { CloseCircle } from "@vicons/ionicons5";
import { AVWaveform } from "vue-audio-visual";
import AudioWave from './AudioWave.vue';

const isStartButtonVisible = ref(true);
const currentPageRef = ref(3);
const sentenceIndexRef = ref(0);
const showCaption = ref(false);
const pages = ref([]);
const knowledge = ref([]);
const isConnected = ref(false);
const realtimeEvents = ref([]);
const items = ref([]);
const isRecording = ref(false);
const isConversationEnded = ref(false);
const isPlaying = ref(false);
const audioRef = ref(new Audio());
const replayAudioRef = ref(new Audio());
const storyTextRef = ref([]);
const audioSpeed = ref(1);
const isWaitingForResponseRef = ref(false);
const userRespondedRef = ref(false);
const chatHistoryRef = ref([]);
const isAskingRef = ref(false);
const isReplayingRef = ref(false);
const audioPage = ref(null);
const isKnowledge = ref(true);
const answerRecord = ref([]);
const currentPageChatHistory = ref([]);
const filteredChatHistory = ref([]);
const chatHistoryIsEmpty = ref(true);
const isClientSetup = ref(false);
const itemToDelete = ref(null);
const itemToRespond = ref(null);
const isChatting = ref(false);
const isExpandedChat = ref(false);
const chatBoxSize = ref({ width: '400px', height: '600px' });
const replayingIndex = ref(null);
const recorderControls = ref({});
const canPushToTalk = ref(true);
const isEnding = ref(false);

// Add refs for child information
const childName = ref('Emma');
const childAge = ref('6');
const childInterests = ref('Snow White');

// Change remainingRequests to be a ref
const remainingRequests = ref(localStorage.getItem('remainingRequests') !== null ? parseInt(localStorage.getItem('remainingRequests')) : 3);

// Add these refs for audio handling
const audioContext = ref(null);
const audioStream = ref(null);
const analyser = ref(null);

const wavRecorderRef = ref(
    new WavRecorder({ sampleRate: 24000 })
);
const wavStreamPlayerRef = ref(
    new WavStreamPlayer({ sampleRate: 24000 })
);
const clientRef = ref(
    new RealtimeClient( { url: 'wss://storymate.hailab.io:8768' } )
);

onMounted(async () => {
    try {
        const response = await fetch(`/Why Frogs are Wet/Why Frogs are Wet_sentence_split.json`);
        const storyText = await response.json();
        pages.value = Array.from({ length: 5 }, (_, index) => ({
            image: `/Why Frogs are Wet/pages/page${index}.png`,
            text: storyText[index]
        }));
        const knowledgeResponse = await fetch(`/Why Frogs are Wet/Why Frogs are Wet_knowledge_dict.json`);
        const knowledgeDict = await knowledgeResponse.json();
        knowledge.value = knowledgeDict;
    } catch (error) {
        console.error('Error fetching story data:', error);
    }
});

const connectConversation = async () => {
    const client = clientRef.value;
    const wavRecorder = wavRecorderRef.value;
    const wavStreamPlayer = wavStreamPlayerRef.value;

    // Set state variables
    realtimeEvents.value = [];
    items.value = client.conversation.getItems();

    // Connect to microphone
    await wavRecorder.begin();

    // Connect to audio output
    await wavStreamPlayer.connect();

    // Connect to realtime API
    await client.connect();
    console.log('connected');
    isConnected.value = true;

    if (client.getTurnDetectionType() === 'server_vad') {
        await wavRecorder.record((data) => client.appendInputAudio(data.mono));
    }
};

const disconnectConversation = async () => {
    console.log('disconnecting conversation');
    isConnected.value = false;
    realtimeEvents.value = [];
    items.value = [];
    // setMemoryKv({}); // Implement this if needed

    const client = clientRef.value;
    client.disconnect();

    const wavRecorder = wavRecorderRef.value;
    await wavRecorder.end();

    const wavStreamPlayer = wavStreamPlayerRef.value;
    await wavStreamPlayer.interrupt();
};

const startRecording = async () => {
    console.log('startRecording function called');
    isRecording.value = true;
    isConversationEnded.value = false;
    console.log('Recording started, states updated');
    userRespondedRef.value = true;
    isWaitingForResponseRef.value = false;
    replayAudioRef.value.pause();
    isReplayingRef.value = false;

    try {
        // Initialize audio context if not already done
        if (!audioContext.value) {
            audioContext.value = new (window.AudioContext || window.webkitAudioContext)();
            analyser.value = audioContext.value.createAnalyser();
            analyser.value.fftSize = 512;
        }

        const client = clientRef.value;
        const wavRecorder = wavRecorderRef.value;
        const wavStreamPlayer = wavStreamPlayerRef.value;
        
        const trackSampleOffset = await wavStreamPlayer.interrupt();
        if (trackSampleOffset?.trackId) {
            const { trackId, offset } = trackSampleOffset;
            await client.cancelResponse(trackId, offset);
        }

        await wavRecorder.record((data) => client.appendInputAudio(data.mono));
        console.log('Recording successfully initialized');
    } catch (error) {
        console.error('Error starting recording:', error);
        isRecording.value = false;
    }
};

const stopRecording = async () => {
    console.log('stopRecording function called');
    
    // Reset states first to prevent UI issues
    console.log('Resetting recording states');
    isRecording.value = false;
    
    try {
        console.log('Attempting to stop recording');
        
        const client = clientRef.value;
        const wavRecorder = wavRecorderRef.value;
        await wavRecorder.pause();
        console.log('Recorder paused successfully');
        
        if (isKnowledge.value) {
            console.log('Processing knowledge recording');
            await client.realtime.send('input_audio_buffer.commit');
            client.conversation.queueInputAudio(client.inputAudioBuffer);
            client.inputAudioBuffer = new Int16Array(0);
            await client.realtime.send('response.create', {
                response: {
                    "modalities": ["text", "audio"],
                    "instructions": getInstruction4Evaluation(items.value),
                }
            });
        } else {
            console.log('Creating standard response');
            await client.createResponse();
            remainingRequests.value -= 1;
            localStorage.setItem('remainingRequests', remainingRequests.value);
        }
        console.log('Recording stopped and processed successfully');
    } catch (error) {
        console.error('Error stopping recording:', error);
    }
};

const togglePlayPause = () => {
    if (isPlaying.value) {
        audioRef.value.pause();
    } else {
        if (audioPage.value !== currentPageRef.value) {
            audioRef.value.src = `/Why Frogs are Wet/audio/p${currentPageRef.value}sec0.mp3`; // Define title if needed
            audioPage.value = currentPageRef.value;
        }
        audioRef.value.play();
        audioRef.value.playbackRate = audioSpeed.value;
    }
    isPlaying.value = !isPlaying.value;
};

const playPageSentences = () => {
    isStartButtonVisible.value = false;
    if (pages.value[currentPageRef.value]?.text) {
        sentenceIndexRef.value = 0;
        const audio = audioRef.value;
        const playNextSentence = async () => {
            if (sentenceIndexRef.value < pages.value[currentPageRef.value].text.length) {
                audio.src = `/Why Frogs are Wet/audio/p${currentPageRef.value}sec${sentenceIndexRef.value}.mp3`;

                audio.onended = () => {
                    sentenceIndexRef.value += 1;
                    playNextSentence();
                };
                try {
                    await audio.play();
                    audio.playbackRate = audioSpeed.value;
                    isPlaying.value = true;
                } catch (error) {
                    console.error('Error playing audio:', error);
                }
            } else {
                audio.pause();
                isPlaying.value = false;
                isConversationEnded.value = false;
                isChatting.value = true;
                answerRecord.value = [];
                currentPageChatHistory.value = [];
                filteredChatHistory.value = [];
                chatHistoryIsEmpty.value = true;
                if (!clientRef.value.realtime.isConnected()) {
                    console.log('setting up client for guiding');
                    setupClient(await getInstruction4Guiding());
                    isClientSetup.value = true;
                } else {
                    console.log('resetting client for guiding');
                    updateClientInstruction(await getInstruction4Guiding());
                }
            }
        };
        playNextSentence();
    }
};


    function getInstruction4Evaluation(items) {
        const instruction4Evaluation = `
        **Instructions for Evaluation**:
        You need to evaluate the child's response based on the following inputs:
        - Conversation History: ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')}
        - Child's Latest Response: The most recent input from the child.
        - Story Context: ${pages[currentPageRef.value]?.text.join(' ')}
        Focus only on evaluating the child's response to the latest question.

        **Steps for Evaluation**:
        Step 1: Check Response Validity
        If the response is empty, cannot be recognized due to noise, being too short, or sent by mistake, mark it as "invalid".
        Step 2: Evaluate Valid Responses
        For responses that contain meaningful content, use the following criteria:
        - Correct: The response is accurate (or partially accurate) and directly relevant to the question.
        - Partially Correct: The response shows partial accuracy and relevance. For example, in a multiple-choice question, selecting one correct option qualifies as partially correct.
        - Incorrect: The response is wrong or shows no understanding of the question (e.g., "I don't know," "I don't remember," or incorrect guesses).
        - Child Asks Question: As long as the child asks a question, mark it as "child asks question".
        - Off-topic: The response is unrelated to the question or the story context.
                    
        **Response Format**:
        Precede each evaluation with the tag <eval>. Do not include any other text apart from the tag and evaluation. 
        Below are the examples of your output, reply with one of these only:
        - <eval>invalid
        - <eval>correct
        - <eval>partially correct
        - <eval>incorrect
        - <eval>child asks question
        - <eval>off-topic
        `;
        console.log(instruction4Evaluation);
        return instruction4Evaluation;
    }


    // update the instruction4Guiding when the currentPageRef.value changes   
    async function getInstruction4Guiding() {
        const instruction4Guiding = `
        You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. From now on, your role is to guide an interactive conversation based on the story information and instructions to enrich their knowledge.
        
        **Story Information**:
        - Story Title: Why Frogs are Wet?
        - Story Text: ${pages.value[currentPageRef.value]?.text.join(' ')}
        - Concept Word: ${knowledge.value[currentPageRef.value]?.keyword}
        - Learning Objective: ${knowledge.value[currentPageRef.value]?.learning_objective}
        - Core Idea: ${knowledge.value[currentPageRef.value]?.core_idea.map(idea => `${idea.knowledge}`).join('\n')}
        - First Question: ${knowledge.value[currentPageRef.value]?.example_nonrecall_questions[0]}

        **Child Information**:
        - Child Name: ${childName.value}
        - Child Age: ${childAge.value}
        - Child Interests: ${childInterests.value}

        **Instructions for Initiating the Conversation**:
            Begin the interaction by posing the first question, which will guide to the concept word.
            You should use different ways to open the conversation. For example: "Hmm, this part of the story is so interesting! + first question"; "Hey xxx, share with me what you think + first question"; "xxx, let's chat about what you just read! + first question"; etc. 
            You should not pose a yes/no question (bad examples: "Can you tell me xxx", "Do you know xxx?", "Can you think of xxx").
            You should tailor the first question to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the posed question.
            Always end your first turn of conversation with a question, instead of a declarative sentence.

        **Response Guidelines**:
        - Maintain a friendly, conversational tone suitable for a 6-8-year-old child.
        - Keep sentences simple, engaging, and under 25 words.
        - Avoid assuming or making up the child's response. Just wait for the child's response for each turn.
        - Ensure that all responses align with the structured three-turn process, focusing on scaffolding, evaluation, and explanation.   
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `;
        console.log(instruction4Guiding);
        return instruction4Guiding;
    }

    const getInstruction4Correct = (items, evaluation) => {
        const instruction4Correct1 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}

    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. one follow-up question.
    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'correct', you should acknowledge their answer and tailor your acknowledgement to the context (e.g., "Great job!", "Wow, that is a great observation!", "You are on the right track!", "Exactly!", "Excellent! You are really paying attention to the story details!", "Ah! Interesting idea!", "Good thinking!", and more)

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Keep your explanation simple, engaging and under 20 words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Since the evaluation of the child's response is 'correct', provide a concise explanation to deepen their understanding.

    **Instructions for Pose a Follow-up Question**:
        - Pose one follow-up, open-ended question related to the learning objective: ${knowledge.value[currentPageRef.value]?.learning_objective}, and the core idea: ${knowledge.value[currentPageRef.value]?.core_idea.map(idea => `${idea.knowledge}`).join('\n')}.
        Here are some examples of follow-up questions for your reference. Note that you should try to come up with better follow-up questions, instead of directly using these examples.
        ${knowledge.value[currentPageRef.value]?.example_nonrecall_questions.join('\n')}
        - You should pose an open-ended question. Do not pose a yes/no question (bad examples: "Can you tell me xxx", "Do you know xxx?", "Can you think of xxx").
        - You should tailor the follow-up question to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the posed question.

    **Instructions for Whole Response**:
        - When organizing all the elements above to form a whole response, make sure the whole response only includes one question sentence.
        - Do not end the conversation. You need to address the question first.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        `
        const instruction4Correct2 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}

    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. conclusion.
    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'correct', you should acknowledge their answer and tailor your acknowledgement to the context (e.g., "Great job!", "Wow, that is a great observation!", "You are on the right track!", "Exactly!", "Excellent! You are really paying attention to the story details!", "Ah! Interesting idea!", "Good thinking!", and more)

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Keep your explanation simple, engaging and under 20 words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Since the evaluation of the child's response is 'correct', provide a concise explanation to deepen their understanding.

    **Instructions for Conclusion**:
        - Do not use question marks in the conclusion.
        - If you are not asking a question, after the explanation, transition to a conclusion. 
        - Keep the conclusion part concise, under 15 words. Here is an example: "It was fun chatting with you! Let's continue reading the story." (Make sure to use different conclusions based on the examples, but end the conclusion using declarative sentence, instead of questions.))
       
    **Instructions for Whole Response**:
        - Do not include any question or question marks in the response.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `

        // case 1: only one 'correct' or 'correct' after one 'incorrect'/'partially correct'
        let correctCount = 0;
        for (const answer of answerRecord.value) {
            if (answer === 'correct') {
                correctCount++;
            }
        }
        console.log('correctCount', correctCount);
        if (correctCount === 1) {
            console.log(instruction4Correct1);
            return instruction4Correct1;
        } else {
            console.log(instruction4Correct2);
            return instruction4Correct2;
        }
    }

    const getInstruction4PartialCorrect = (items, evaluation) => {
        const instruction4PartialCorrect1 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}

    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. one follow-up question.

    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'partially correct', you should first provide encouraging acknowledgement and tailor your acknowledgement to the context (e.g., "That's a good try!", "Aha! You're on the right track!", and more).

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Keep your explanation simple, engaging and under 20 words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Do not explicitly tell the child the correct answer.
        
    **Instructions for Pose a Follow-up Question**:
        - Ask the ORIGINAL, most recent, last-posed question (which the child answers partially correctly) again, but add some multiple-choice options. Avoid using labels like "A, B, C." 
        - Here is an example: What did Amara's mom and brother do, did they ignore the bat, play with the bat, or wait for a wildlife rescue team?
        - You only need to add some multiple-choice options to the original question. Do not pose a new question.
        - Do not end the conversation.
    
     **Instructions for Whole Response**:
        - When organizing all the elements above to form a whole response, make sure the whole response only includes one question sentence.
        - Do not end the conversation.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        - Do not reveal the answer. You should hint the child to think in the explanation part.
        - The rephrased question should have the same question type as the original question. For example, if the original question is 'What xxx', the rephrased multiple-choice question should also be 'What xxx', and you should add the multiple-choice options after the question.
        `
        const instruction4PartialCorrect2 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}


    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. conclusion.

    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'partially correct', you should first provide acknowledgement and tailor your acknowledgement to the context (e.g., "That's a good try!", "Aha! You're on the right track!", and more).

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Explain the answer here with easy-to-understand words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Keep your explanation simple, engaging and under 20 words. 

    **Instructions for Conclusion**:
        - Do not use question marks in the conclusion.
        - If you are not asking a question, after the explanation, transition to a conclusion. 
        - Keep the conclusion part concise, under 15 words. Here is an example: "It was fun chatting with you! Let's continue reading the story." (Make sure to use different conclusions based on the examples, but end the conclusion using declarative sentence, instead of questions.))

    **Instructions for Whole Response**:
        - Do not include any question or question marks in the response.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `

        let PartialCorrectCount = 0;
        let correctCount = 0;
        for (const answer of answerRecord.value) {
            if (answer === 'partially correct' || answer === 'incorrect') {
                PartialCorrectCount++;
            } else if (answer === 'correct') {
                correctCount++;
            }
        }

        if (PartialCorrectCount === 1 || (PartialCorrectCount === 2 && correctCount === 1)) {
            return instruction4PartialCorrect1;
        } else {
            return instruction4PartialCorrect2;
        }
    }

    const getInstruction4Incorrect = (items, evaluation) => {
        const instruction4Incorrect1 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')}
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}

    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. one follow-up question.

    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'incorrect', you should acknowledge their effort and tailor your acknowledgement to the context (e.g., "That's a good try!", "Let's try it again!", "Let's think about it together!", and more).

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Do not explicitly tell the child the correct answer.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Keep your explanation simple, engaging and under 20 words.
                
    **Instructions for Pose a Follow-up Question**:
        - Ask the ORIGINAL, most recent, last-posed question (which the child answers incorrectly) again, but add some multiple-choice options. Avoid using labels like "A, B, C." 
        - Here is an example: What did Amara's mom and brother do, did they ignore the bat, play with the bat, or wait for a wildlife rescue team?
        - You only need to add some multiple-choice options to the original question. Do not pose a new question.
        - Do not end the conversation.
    
    
     **Instructions for Whole Response**:
        - When organizing all the elements above to form a whole response, make sure the whole response only includes one question sentence.
        - Do not end the conversation.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        - Do not reveal the answer. You should hint the child to think in the explanation part.
        - The rephrased question should have the same question type as the original question. For example, if the original question is 'What xxx', the rephrased multiple-choice question should also be 'What xxx', and you should add the multiple-choice options after the question.
        `
        const instruction4Incorrect2 = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')}
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}


    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. conclusion.

    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the evaluation of the child's response is 'incorrect', you should first provide encouraging feedback (e.g., "Let's try it again!", "Let's think about it together!", "That's a good try!", etc.).

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Explain the answer here with easy-to-understand words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Keep your explanation simple, engaging and under 20 words. 

    **Instructions for Conclusion**:
        - Do not use question marks in the conclusion.
        - If you are not asking a question, after the explanation, transition to a conclusion. 
        - Keep the conclusion part concise, under 15 words. Here is an example: "It was fun chatting with you! Let's continue reading the story." (Make sure to use different conclusions based on the examples, but end the conclusion using declarative sentence, instead of questions.))

    **Instructions for Whole Response**:
        - Do not include any question or question marks in the response.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `
        let incorrectCount = 0;
        let correctCount = 0;
        for (const answer of answerRecord.value) {
            if (answer === 'incorrect' || answer === 'partially correct') {
                incorrectCount++;
            } else if (answer === 'correct') {
                correctCount++;
            }
        }

        if (incorrectCount === 1 || (incorrectCount === 2 && correctCount === 1)) {
            return instruction4Incorrect1;
        } else {
            return instruction4Incorrect2;
        }
    }

    const getInstruction4ChildQuestion = (items, evaluation) => {
        const instruction4ChildQuestion = `
    You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};

    Your response should contain three parts: 1. acknowledgement, 2. explanation, and 3. follow-up question or conclusion.

    **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements. Do not repeat the same acknowledgement as in the conversation history. 
        - Since the child posed a question, you should first acknowledge their effort and tailor your acknowledgement to the context (e.g., Good thinking!", "Oh it's an interesting question!", and more).

    **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Keep your explanation simple, engaging and under 20 words.
        - Since the child poses a question, answer the question with easy-to-understand words.

    **Situations for Not Posing a Follow-up Question**:
        - You do not need to pose a follow-up question if:
        1. The child has asked more than three questions, or
        2. There are more than four rounds of questions.
        In these cases, refer to **Instructions for Conclusion**. You do not need to end the conversation early, like only having two rounds of conversation.

    **Instructions for Pose a Follow-up Question**:
        - After you answer the child's question, and there are less than three rounds of questions, ask the ORIGINAL question, which has not been answered, to the child.
        ${knowledge.value[currentPageRef.value]?.example_nonrecall_questions.join('\n')}
        - You should pose an open-ended, multi-choice question. Do not pose a yes/no question (bad examples: "Can you tell me xxx", "Do you know xxx?", "Can you think of xxx").

    **Instructions for Conclusion**:
        - Do not use question marks in the conclusion.
        - You cannot conclude the conversation if you're posing a follow-up question.
        - If you are not asking a question, after the explanation, transition to a conclusion. 
        - Keep the conclusion part concise, under 15 words.
        - Here is an example: "There are many interesting things in the story! Let's continue reading the story." (Make sure to use different conclusions based on the examples, but end the conclusion using declarative sentence, instead of questions.))

    **Instructions for Whole Response**:
        - When organizing all the elements above to form a whole response, make sure the whole response only includes one question sentence.
        - If your response includes a question, do not end the conversation. You need to address the question first.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `;
        console.log(instruction4ChildQuestion);
        return instruction4ChildQuestion;
    }

    const getInstruction4Invalid = (items, evaluation) => {
        const instruction4Invalid = `
        You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')}

        Since the evaluation of the child's response is 'invalid', you should respond with a friendly line (e.g., "I didn't hear your answer, can you say it again?", "Oh I didn't catch that, can you say it again?")
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        `;
        console.log(instruction4Invalid);
        return instruction4Invalid;
    }

    const getInstruction4OffTopic = (items, evaluation) => {
        const instruction4OffTopic = `
        You are a friendly chatbot engaging with a 6-8-year-old child named ${childName.value}, who is reading a storybook. Now your task is to generate a response to the child's latest answer, based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's latest response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')}

        Start by acknowledging the child's response (e.g., "Interesting idea!"). Then guide the conversation back to the original question you asked or conclude the interaction if the conversation has gone beyond three rounds.
        - Speak ${audioSpeed <= 1 ? 'slower' : 'faster'} than usual (like ${audioSpeed} of your normal speed) for improved understanding by children.
        `;
        console.log(instruction4OffTopic);
        return instruction4OffTopic;
    }

    const getInstruction4FollowUp = (items, evaluation) => {
        const instruction4FollowUp = `
        You need to pose a follow-up question based on the following information: 
        1. conversation history: 
        ${items.map(item => `${item.role}: ${item.content[0]?.transcript}`).join('\n')};
        2. the evaluation of the child's response: ${evaluation};
        3. story text: ${pages[currentPageRef.value]?.text.join(' ')};
        4. children's information: name: ${childName.value}, age: ${childAge.value}, interests: ${childInterests.value}
        Follow the following instructions:
        Your response should contain three parts: acknowledgement, explanation, and follow-up question or conclusion.

        **Instructions for Acknowledgement**:
        - Your acknowledgement should be friendly, non-repetitive, and under 25 words.
        - You need to avoid using judgmental words like 'wrong', 'incorrect', 'correct', 'right', etc.
        - Use various acknowledgements tailored to the context. Do not repeat the same acknowledgement as in the conversation history. 
        - Here are different situations for acknowledgement based on the child's response:
            1. If the evaluation is 'invalid', reply with a friendly line (e.g., "I didn't hear your answer, can you say it again?", "Oh I didn't catch that, can you say it again?")
            2. If the evaluation is 'incorrect', you should first provide encouraging feedback (e.g., "Let's try again!", "Let's think about it together!", "It's okay if you don't remember!", "Let's think again!", "Aha! You jumped ahead of me a little bit, but that's okay.")
            3. If the evaluation is 'partially correct', you should first provide encouraging feedback (e.g., "That's a good try!", "Aha! You're on the right track!"), then hint the child to think about the correct answer.
            4. If the evaluation is 'correct', you should first acknowledge their answer (e.g., "Great job!", "Wow, that is a great observation!", "You are on the right track!", "Exactly!", "Excellent! You are really paying attention to the story details!", "Ah! Interesting idea!", "Good thinking!")
            5. If the evaluation is 'child asks question', you should acknowledge their question (e.g., "Good question!", "Oh it's an interesting question!")
            6. If the evaluation of the child's response is 'off-topic', you should steer the conversation back to the original topic.
        - You should tailor the follow-up question to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the posed question.
        
        **Instructions for Explanation**:
        - Your explanation should be suitable for children aged 6 to 8.
        - Keep your explanation simple, engaging and under 20 words.
        - Tailor the explanation to the child's age and interests. For instance, you can set a scene and embed the child's favorite character in the explanation.
        - Here are different situations for explanation based on the child's response:
            1. If the evaluation is 'correct', provide a concise explanation to deepen their understanding.
            2. If the evaluation is 'incorrect', briefly explain why what the child has chosen is not right (without explicitly telling them they did wrong) 
            3. If the evaluation is 'partially correct', hint the child to think to get the correct answer (without explicitly telling the correct answer)
            4. If the evaluation is 'child asks question', answer the child's question using simple words.

        **Situations for Not Posing a Follow-up Question**:
        - You do not need to pose a follow-up question if:
            1. You think the learning objective has been addressed effectively (usually after 4 rounds of conversation in total, and this is the ${items.length/2} round of conversation), or
            2. You are addressing the first question: the child failed to answer the first question correctly and you rephrased the first question into a multiple-choice question, or
            3. The child answers incorrectly two times in a row, or
            4. You already asked three different questions in total, or 
            5. There are more than four rounds of questions.
        In these cases, you can end the conversation (refer to **Instructions for Conclusion**). 
        
        **Instructions for Pose a Follow-up Question**:
         - If you are posing a follow-up question, you do not need to conclude the conversation.
         - You should pose open-ended questions. Do not pose a yes/no question (bad examples: "Can you tell me xxx", "Do you know xxx?", "Can you think of xxx").
         - Here are the only situations you need to pose a follow-up question based on the child's response:
            1. If the evaluation of the child's response is 'correct', you should pose a follow-up question related to the learning objective: ${knowledge.value[currentPageRef.value]?.learning_objective}.
            Here are some examples of follow-up questions for your reference. Note that you should try to come up with better follow-up questions, instead of directly using these examples.
            ${knowledge.value[currentPageRef.value]?.example_nonrecall_questions.join('\n')}
            2. If the evaluation of the child's response is 'partially correct' or 'incorrect' to the previous question:
                i. If this is the first time the child answers incorrectly (you haven't rephrased the previous question into a multiple-choice question), rephrase the previous question into a multiple-choice question. The rephrased question should ask about the same thing as the previous question, but in a multiple-choice format. For the options of the multiple-choice question, avoid using "A, B, C" to make it sound more natural. (e.g., What did Amara's mom and brother do? Did they ignore the bat, play with the bat, or wait for a wildlife rescue team?)
                ii.  If the child answers incorrectly more than one time (it means you already rephrased into a multiple-choice question), do not rephrase the question or ask the question in the same way again. Do not pose a new question. You should provide the correct answer and end the conversation (refer to **Instructions for Conclusion**).
                The rephrased question should have the same question type as the original question. For example, if the original question is 'What xxx', the rephrased question should also be 'What xxx', then add the multiple-choice options.
            3. If the evaluation is 'question-posed', and you have not asked three different questions in total, pose a follow-up question related to the learning objective: ${knowledge.value[currentPageRef.value]?.learning_objective} after the explanation.

        **Instructions for Conclusion**:
        - Do not use question marks in the conclusion.
        - You cannot conclude the conversation if you're posing a follow-up question.
        - If you are not asking a question, after the explanation, transition to a conclusion. 
        - If the child repeatedly answers incorrectly, you should provide the correct answer, then transition to a conclusion.
        - Keep the conclusion part concise, under 15 words.
        - Here is an example: "It was fun chatting with you! Let's continue reading the story." (Make sure to use different conclusions based on the examples, but end the conclusion using declarative sentence, instead of questions.))

        **Instructions for Whole Response**:
        - When organizing all the elements above to form a whole response, make sure the whole response only includes one question sentence.
        - If your response includes a question, you can't conclude the conversation. You need to address the question first.
        - Keep the conversation safe, civil, and appropriate for children. Do not include any inappropriate content, such as violence, sex, drugs, etc.
        `;
        console.log(instruction4FollowUp);
        return instruction4FollowUp;
    }


    const updateClientInstruction = async (instruction) => {
        const client = clientRef.value;
        client.updateSession({ instructions: instruction });
        client.realtime.send('response.create');
        remainingRequests.value -= 1;
        localStorage.setItem('remainingRequests', remainingRequests.value);
        console.log(instruction);
    }

    const setupClient = async (instruction) => {
        (async () => {
            console.log('setting up client');
            console.log('currentPageRef.value', currentPageRef.value);
            const wavStreamPlayer = wavStreamPlayerRef.value;
            const client = clientRef.value;
            client.updateSession({ instructions: instruction });
            client.updateSession({ voice: 'alloy' });
            client.updateSession({ input_audio_transcription: { model: 'whisper-1' } });
            client.on('error', (event) => console.error(event));
            client.on('conversation.interrupted', async () => {
                const trackSampleOffset = await wavStreamPlayer.interrupt();
                if (trackSampleOffset?.trackId) {
                const { trackId, offset } = trackSampleOffset;
                await client.cancelResponse(trackId, offset);
                }
                userRespondedRef.value = true;
                isWaitingForResponseRef.value = false;
            });
            client.on('conversation.item.appended', (item) => {
                console.log('conversation.item.appended');
                // console.log(item);
            });
            client.on('conversation.updated', async ({ item, delta }) => {
                const items = client.conversation.getItems();
                // if the item starts with <test>, delete it
                if (item?.content[0]?.transcript?.startsWith('<')) {
                    // keep the item id, and when the item status is completed, delete it
                    itemToDelete.value = item.id;
                    console.log('evaluation result', item.content[0]?.transcript);
                    if (item.status === 'completed') {
                        console.log('!!! deleting item', item);
                        // setEvaluation(item.content[0]?.transcript.replace('<eval>', '').trim());
                        try {
                            await client.realtime.send('conversation.item.delete', {
                                item_id: item.id
                            });
                            const answerOrder = Math.floor(items.length / 2) - 1;
                            // make sure only update answerRecord if all answers in answerRecord are not null before the answerOrder
                            let allAnswersNotNull = true;
                            for (let i = 0; i < answerOrder; i++) {
                                if (answerRecord.value[i] === null || answerRecord.value[i] === undefined) {
                                    allAnswersNotNull = false;
                                    break;
                                }
                            }
                            console.log('answerOrder', answerOrder);
                            console.log('allAnswersNotNull', allAnswersNotNull);
                            if (allAnswersNotNull && (!(answerRecord.value[answerOrder] !== null && answerRecord.value[answerOrder] !== undefined))) {
                                answerRecord.value[answerOrder] = item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim();
                            }
                            console.log('answerRecord', answerRecord.value);
                        } catch (error) {
                            console.log('error', error);
                        }
                        console.log('items', items);
                        console.log('items to delete', itemToDelete.value);
                        // only update answerRecord after the item is deleted
                        
                        // if this is the first completed item for the item id, send a response
                        if (item.id !== itemToRespond.value && item.role === 'assistant' && items[items.length - 1]?.status === 'completed') {
                            console.log('now generating response for', item.content[0]?.transcript.replace('<eval>', '').trim());
                            itemToRespond.value = item.id;
                            // send this instruction after the item is completed
                            setTimeout(async () => {
                                // if the string has </eval>, remove it
                                const evaluation = item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim();
                                console.log('evaluation', evaluation);
                                switch (evaluation) {
                                    case 'correct':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4Correct(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    case 'partially correct':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4PartialCorrect(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    case 'incorrect':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4Incorrect(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    case 'off-topic':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4OffTopic(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    case 'child asks question':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4ChildQuestion(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    case 'invalid':
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4Invalid(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                    default:
                                        await client.realtime.send('response.create', {
                                            response: {
                                                "modalities": ["text", "audio"],
                                                "instructions": getInstruction4FollowUp(items, item.content[0]?.transcript.replace('<eval>', '').replace('</eval>', '').trim())
                                            }
                                        });
                                        userRespondedRef.value = false;
                                        remainingRequests.value = remainingRequests.value - 1;
                                        localStorage.setItem('remainingRequests', remainingRequests.value);
                                        break;
                                }
                            }, 100);
                        }
                    }
                }
                else if (item.id !== itemToDelete.value || (!item.content[0]?.transcript?.startsWith('<'))) {
                    // console.log('logging this item: ', item.content[0]?.transcript);
                    if (delta?.transcript) {
                        // setChatHistory(items);
                        currentPageChatHistory.value = items;
                        filteredChatHistory.value = currentPageChatHistory.value.filter(msg => msg.type === 'message');
                        chatHistoryIsEmpty.value = filteredChatHistory.value.length === 0;
                        // chatHistoryRef.value[currentPageRef.value] = items;
                        // check if the chat-window element exists
                        const chatWindow = document.getElementById('chat-window');
                        if (chatWindow) {
                            chatWindow.scrollTop = chatWindow.scrollHeight;
                        }
                    }
                    if (delta?.audio) {
                        wavStreamPlayer.add16BitPCM(delta.audio, item.id);
                    }
                    if (item.status === 'completed' && item.formatted.audio?.length) {
                        console.log('current item', item);
                        const wavFile = await WavRecorder.decode(
                            item.formatted.audio,
                            24000,
                            24000
                        );
                        item.formatted.file = wavFile;
                        // setChatHistory(items);
                        currentPageChatHistory.value = items;
                        filteredChatHistory.value = currentPageChatHistory.value.filter(msg => msg.type === 'message');
                        chatHistoryIsEmpty.value = filteredChatHistory.value.length === 0;
                        //chatHistoryRef.value[currentPageRef.value] = items;
                        // get the chat-window element by class name
                        const chatWindow = document.getElementsByClassName('chat-window')[0];
                        if (chatWindow) {
                            chatWindow.scrollTop = chatWindow.scrollHeight;
                        }
                        if (item.role === 'assistant') {
                            // if the last item does not end with a question mark, it means the conversation is ended
                            if (!item?.content[0]?.transcript?.endsWith('?') && !item?.content[0]?.transcript?.endsWith('? ') && !item?.content[0]?.transcript?.endsWith('talk.')) {
                                while (wavStreamPlayer.isPlaying() || isReplayingRef.value) {
                                    await new Promise(resolve => setTimeout(resolve, 100));
                                }
                                console.log('conversation ended');
                                if (!isReplayingRef.value && !isAskingRef.value) {
                                    isConversationEnded.value = true;
                                }
                            } 
                        }
                    }
                    items.value = items;
                }
                isClientSetup.value = true;
            });

            
            if (!client.isConnected()) {
                await connectConversation();
            }   
        
            client.realtime.send('response.create');
            remainingRequests.value = remainingRequests.value - 1;
            localStorage.setItem('remainingRequests', remainingRequests.value);
            items.value = client.conversation.getItems();

            return () => {
                // cleanup; resets to defaults
                client.reset();
            };
        })();
    };

    const handleReplay = async (index) => {
        const wavStreamPlayer = wavStreamPlayerRef.value;
        await wavStreamPlayer.interrupt();
        const replayAudio = replayAudioRef.value;
        console.log('---replayAudio', filteredChatHistory, index);
        replayAudio.src = filteredChatHistory.value[index].formatted.file.url;
        // pause the replayAudio
        replayAudio.pause();
        replayAudio.currentTime = 0;
        if (isReplayingRef.value === false) {
            replayAudio.play();
            replayingIndex.value = index; // Set the replaying index
            isReplayingRef.value = true;
            replayAudio.onended = () => {
                console.log('replay ended');
                isReplayingRef.value = false;
                replayingIndex.value = null; // Reset the replaying index when done
            };
        }
        else {
            isReplayingRef.value = false;
            replayingIndex.value = null;
        }
    }

    const expandBtnStyle = {
        position: 'absolute',
        top: '8px',
        left: '8px',
        zIndex: 1
    };

    const minimizeBtnStyle = {
        position: 'absolute',
        top: '8px',
        left: '45px',
        zIndex: 1
    };

    const closeBtnStyle = {
        
    };

    // Add chatInputStyle definition
    const chatInputStyle = computed(() => ({
        width: '100%',
        height: '80px',
        padding: '8px',
        borderRadius: '50px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#F4A011',
        position: 'relative',
        zIndex: 103
    }));

    // Add computed property for container disabled state
    const isContainerDisabled = computed(() => remainingRequests.value <= 0);

</script>

<template>
    <div class="container" :class="{ 'disabled': isContainerDisabled }">
        <n-tag type="info" :style="{ marginTop: '10px', marginBottom: '10px', zIndex: 103 }">
            Remaining Requests: {{ remainingRequests }}
        </n-tag>
        <div class="main-container" :class="{ 'disabled': isContainerDisabled }">
            <div v-if="isContainerDisabled" class="disabled-overlay">
                <div class="disabled-message">
                    <p>You have used all your available requests 🖐️</p>
                </div>
            </div>
            <div class="header">
                <h3 class="header-title">Why Frogs are Wet?</h3>
            </div>
            <div id='main-container'>
                <div id='book-container'>
                    <div id='book-content'>
                        <div id='book-img'>
                            <img :src="pages[currentPageRef]?.image"/>
                        </div>
                        <div id='bottom-box'>
                            <div id='caption-box'>
                                <h4 id="caption">
                                    {{ pages[currentPageRef]?.text[sentenceIndexRef] }}
                                </h4>
                            </div>
                            <div id='penguin-box'>
                                <img
                                src='/imgs/penguin.svg'
                                alt='penguin'
                                style='width: 88px;'>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="isChatting" id='chat-container' :style="{ position: 'absolute', height: chatBoxSize.height }">
                <div v-if="isRecording" id='recording-layer' :style="{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', borderRadius: '16px', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 101}"></div>
                <div v-if="isRecording" id='audio-visualizer' :style="{position: 'absolute', top: '40%', left: '50%', transform: 'translate(-50%, -50%)', width: '100px', height: '100px', zIndex: 101}">
                    <AudioWave />
                </div>
                <div class='chat-window'>
                    <div v-if="chatHistoryIsEmpty" id='loading-box'>
                        <n-icon>
                            <LoadingOutlined id='loading-icon' size="40" color="#7AA2E3" />
                        </n-icon>
                    </div>
                    <div v-for="(msg, index) in filteredChatHistory" :key="index" :id="msg.role === 'user' ? 'user-msg' : 'chatbot-msg'">
                        <div v-if="msg.role === 'user'" id="user-chat">
                            <n-avatar round id='user-avatar' :style="{ backgroundColor: '#ACD793', marginRight: '8px' }">{{ childName.substring(0, 2) }}</n-avatar>
                            <div id="msg-bubble" :style="{ backgroundColor: '#ECECEC' }">
                                <h5 v-if="msg.content[0].transcript !== null" level="body-lg" :style="{ margin: '0px' }">{{ msg.content[0].transcript }}</h5>
                                <n-icon v-else>
                                    <LoadingOutlined id="loading-icon" size="20" color="#7AA2E3" />
                                </n-icon>
                            </div>
                        </div>
                        <div v-else id="chatbot-chat">
                            <img id='chatbot-avatar' src='/imgs/penguin.svg' />
                            <div id="msg-bubble" :style="{ position: 'relative' }" @click="handleReplay(index)">
                                <h5 v-if="!msg.content?.[0]?.transcript?.startsWith('<')" level="body-lg" :style="{ margin: '0px', marginRight: '30px' }">
                                    {{ msg.content?.[0]?.transcript }}
                                </h5>
                                <n-button v-if="msg.status === 'completed' && !msg.content?.[0]?.transcript?.startsWith('<')" id="replay-btn" :key="index" quaternary :style="{ position: 'absolute', right: '8px', bottom: '8px' }">
                                    <template v-if="replayingIndex === index">
                                        <n-icon><PauseCircle size="25" color="#2A2278" /></n-icon>
                                    </template>
                                    <template v-else>
                                        <n-icon><PlayCircle size="25" color="#2A2278" /></n-icon>
                                    </template>
                                </n-button>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="canPushToTalk && !isEnding" id='recording-box'>
                    <div v-if="isRecording">
                        <div id='recording-box-1'></div>
                        <div id='recording-box-2'></div>
                    </div>
                    <button id='chat-input' 
                            class='no-selection'
                            :disabled="!isConnected || !canPushToTalk"
                            @mousedown.left.prevent="(e) => { console.log('mousedown event triggered'); startRecording(); }"
                            @mousedown.right.prevent
                            @touchstart.passive.prevent="startRecording"
                            @pointerdown.prevent="startRecording"
                            @mouseup.left.prevent="(e) => { console.log('mouseup event triggered'); stopRecording(); }"
                            @touchend.passive.prevent="(e) => { console.log('touchend event triggered'); stopRecording(); }"
                            @pointerup.prevent="(e) => { console.log('pointerup event triggered'); stopRecording(); }"
                            @contextmenu.stop.prevent
                            @click.right.prevent
                            :style="chatInputStyle">
                        <h4 v-if="isRecording" :style="{ color: 'white', fontSize: '30px', fontFamily: 'Cherry Bomb' }">Talking...</h4>
                        <div v-else>
                            <div :style="{ width: '90%', height: '25%', backgroundColor: '#FFFFFF4D', position: 'absolute', top: '7px', left: '3%', borderRadius: '20px' }"></div>
                            <img src='/imgs/ring.svg' alt='ring' :style="{ width: '35px', height: '35px', position: 'absolute', top: '2px', right: '6px', borderRadius: '50%' }" />
                            <h4 :style="{ color: 'white', fontSize: '30px', fontFamily: 'Cherry Bomb' }">Hold to talk!</h4>
                        </div>
                    </button>
                </div>
                <div id='moon-chat-box'>
                    <img src='/imgs/moon.svg' alt='moon' :style="{ position: 'absolute', bottom: '0', right: '0', zIndex: -1 }" />
                </div>
            </div>
            <div id="start-box" v-if="isStartButtonVisible" :style="{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', width: '100%' }">
                <div id="persona-box" :style="{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', width: '40%' }">
                    <n-card title="Child's Background" size="medium" >
                        <n-space vertical>
                            Name
                            <n-input v-model:value="childName" placeholder="Emma">
                            </n-input>
                            Age
                            <n-input v-model:value="childAge" round placeholder="6">
                            <template #suffix>
                                years old
                            </template>
                            </n-input>
                            Interests
                            <n-input v-model:value="childInterests" round placeholder="Snow White">
                            </n-input>
                        </n-space>
                        <div style="display: flex; justify-content: center; margin-top: 20px;">
                            <n-button id="start-button" strong secondary round type="tertiary" @click="playPageSentences">Start Reading!</n-button>
                        </div>
                    </n-card>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
@font-face {
  font-family: 'Cherry Bomb';
  src: url('/fonts/cherrybombone-regular.ttf');
  font-weight: normal;
  font-style: normal;
}

#start-box {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background-color: #ffffff80;
}

#start-button {
    font-size: 20px;
    font-family: 'Cherry Bomb';
    font-weight: bold;
    border-radius: 50px;
    padding: 10px 20px;
    width: 200px;
    color: #333333;
}

.container {
    position: relative;
    margin-left: 0;
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-items: center;
    align-items: center;
}

.main-container {
    position: relative;
    margin-left: 0;
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-items: center;
    align-items: center;
}

.header {
    flex-shrink: 0;
    flex-grow: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    background-color: #000000;
    font-family: 'Cherry Bomb';
    color: #FFFFFF;
    font-size: 20px;
    flex-basis: 40px;
    padding: 0 28px;
    width: 100%;
}

.header-title {
  font-size: 25px;
  font-weight: bold;
  flex-grow: 1;
  margin: auto;
  text-align: center;
}

#main-container {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    min-height: 0;
}

#book-container {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    width: 100%;
    position: relative;
    max-height: calc(100% - 130px);
}

#book-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    max-height: 100%;
    justify-content: center;
    align-items: center;
}

#bottom-box {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  flex-shrink: 0;
  flex-basis: 130px;
  position: relative;
  background-color: #000000;
  width: 100%;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

#caption {
  font-weight: 200;
  width: 70%;
  font-family: 'BM Jua';
  font-size: 28px;
  color: #3F150B;
  text-align: center;
  align-items: center;
  display: flex;
  justify-content: center;
  margin: 0;
}

#caption-box {
  max-height: 120px;
  min-height: 80px;
  width: 100%;
  background-color: #F5F0E6;
  text-align: center;
  align-items: center;
  display: flex;
  justify-content: center;
}

#penguin-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  right: 32px;
  bottom: 10px;
}

#recording-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 16px;
  background-color: rgba(0,0,0,0.5);
  z-index: 101;
}

#audio-visualizer {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  z-index: 101;
}

#expand-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 1;
}

#minimize-btn {
  position: absolute;
  top: 8px;
  left: 45px;
  z-index: 1;
}

#close-btn {
  position: absolute;
  top: 8px;
  left: 80px;
  z-index: 1;
}

.chat-window {
  overflow-y: auto;
  height: calc(100% - 130px);
}

#chat-input {
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #F4A011;
  position: relative;
  z-index: 100;
}

#moon-chat-box {
  position: absolute;
  bottom: 0;
  right: 0;
  z-index: -1;
}

#chat-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  margin: 0 16px;
  padding: 16px;
  width: calc(100% - 350px);
  max-width: calc(100% - 64px);
  height: 60%;
  position: absolute;
  box-shadow: 0 4px 10px 0 #0C1560;
  border-radius: 16px;
  position: absolute;
  z-index: 100;
  bottom: 16px;
  background-color: #ffffff;
  min-width: 0;
  right: 180px;
  background-image: linear-gradient(to bottom, #261E70, #5C4ED3);
}

#loading-box {
  display: flex;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
  margin: auto;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@keyframes loading {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

#loading-icon {
  animation: loading 2s linear infinite;
}

#recording-box {
  width: 100%;
  height: 100px;
  margin-top: 16px;
  padding: 12px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

#recording-box-1 {
  border: 2px solid rgba(246, 191, 69, 0.5);
  border-radius: 50px;
  position: absolute;
  top: 6px;
  left: 6px;
  width: calc(100% - 12px);
  height: calc(100% - 12px);
  z-index: 1;
}
#recording-box-2 {
  border: 2px solid rgba(246, 191, 69, 0.2);
  border-radius: 50px;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

#chatbot-chat {
  width: 100%;
  height: fit-content;
  display: flex;
  align-items: center;
}

#user-chat {
  width: 100%;
  height: fit-content;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  float: right;
}

#msg-bubble {
  background-color: #F5F0E6;
  font-family: 'BM Jua';
  font-style: bold;
  color: #272343;
  padding: 16px;
  margin: 8px;
  border-radius: 16px;
  text-align: left;
  display: flex;
  flex-direction: row;
  max-width: 90%;
}

#chatbot-avatar {
  float: left;
  width: 60px;
}

#chat-input, #chat-input-greet {
  width: 100%;
  height: 80px;
  padding: 8px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  justify-items: center;
}

#voice-input-btn {
  width: 100%;
  display: flex;
  justify-content: center;
}

.disabled {
    pointer-events: none;
    opacity: 0.7;
}

.disabled-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.disabled-message {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    max-width: 400px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.disabled-message h2 {
    color: #2A2278;
    margin-bottom: 1rem;
    font-family: 'Cherry Bomb';
}

.disabled-message p {
    color: #666;
    font-family: 'BM Jua';
    font-size: 1.1rem;
}

#user-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'BM Jua';
  font-size: 16px;
  color: #272343;
}

#replay-btn {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
}

#replay-btn:hover {
  background: transparent !important;
}
</style>