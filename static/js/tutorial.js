/**
 * 提示词工程互动式教程 - 核心逻辑
 * 处理教程加载、步骤导航及 AI 模拟交互
 */

// 从 window.TUTORIAL_CONFIG 获取 Django 传来的初始配置
const config = window.TUTORIAL_CONFIG || { activeSlug: '' };

// 扩展 AppRoot 配置
Object.assign(AppRoot, {
    data() {
        return {
            loading: true,
            tutorials: [],
            activeSlug: config.activeSlug,
            tutorialData: null,
            currentStepIndex: 0,
            stepStates: [], // Tracks state for quizzes, fill_blanks per step
            drawerVisible: false,
            
            // Playground 状态
            promptInput: "",
            chatHistory: [],
            aiLoading: false,
        };
    },
    
    computed: {
        totalSteps() {
            return this.tutorialData && this.tutorialData.steps ? this.tutorialData.steps.length : 0;
        },
        currentStepData() {
            if (this.totalSteps === 0) return null;
            return this.tutorialData.steps[this.currentStepIndex];
        },
        renderedMarkdown() {
            if (!this.currentStepData || !this.currentStepData.content) return '';
            if (window.marked) {
                return window.marked.parse(this.currentStepData.content);
            }
            return this.currentStepData.content;
        },
        currentInteractions() {
            return this.currentStepData && this.currentStepData.interaction ? this.currentStepData.interaction : [];
        }
    },
    
    watch: {
        currentStepIndex: {
            handler() {
                this.applyHighlights();
            },
            flush: 'post'
        }
    },

    methods: {
        /**
         * 获取所有可用教程目录
         */
        async fetchDirectory() {
            try {
                const res = await fetch('/api/tutorials/');
                const data = await res.json();
                this.tutorials = data.tutorials || [];
                
                // 初始加载逻辑
                if (!this.activeSlug && this.tutorials.length > 0) {
                    this.loadTutorial(this.tutorials[0].slug, false);
                } else if (this.activeSlug) {
                    this.loadTutorial(this.activeSlug, false);
                } else {
                    this.loading = false;
                }
            } catch (e) {
                console.error("Failed to fetch tutorials directory", e);
                this.loading = false;
                if (window.ElementPlus) {
                    ElementPlus.ElMessage.error("获取教程目录失败");
                }
            }
        },

        /**
         * 加载选定的教程详情
         */
        async loadTutorial(slug, pushState = true) {
            if (!slug) return;
            this.loading = true;
            
            try {
                const res = await fetch(`/api/tutorials/${slug}/`);
                if (res.ok) {
                    this.tutorialData = await res.json();
                    this.activeSlug = slug;
                    this.currentStepIndex = 0;
                    this.chatHistory = [];
                    this.initStepStates();
                    this.applyHighlights();
                    
                    if (pushState) {
                        window.history.pushState({ slug: slug }, '', `/tutorial/${slug}/`);
                    }
                } else {
                    if (window.ElementPlus) ElementPlus.ElMessage.warning("无法加载选择的教程");
                }
            } catch (e) {
                console.error("Error loading tutorial detail", e);
            } finally {
                this.loading = false;
            }
        },

        initStepStates() {
            // 初始化每一步的特定状态（用于跨步骤保留做题记录和填空内容）
            this.stepStates = [];
            if (this.tutorialData && this.tutorialData.steps) {
                for (let i = 0; i < this.tutorialData.steps.length; i++) {
                    const step = this.tutorialData.steps[i];
                    let state = { quizAnswer: null, quizSubmitted: false, blanks: {} };
                    
                    if (step.interaction) {
                        step.interaction.forEach(inter => {
                            // 初始化填空
                            if (inter.type === 'fill_blank' && inter.blanks) {
                                inter.blanks.forEach((_, idx) => {
                                    state.blanks[idx] = '';
                                });
                            }
                        });
                    }
                    this.stepStates.push(state);
                }
            }
        },

        applyHighlights() {
            // 清除旧高亮
            document.querySelectorAll('.km-highlight').forEach(el => {
                el.classList.remove('km-highlight');
            });
            
            // 应用新高亮
            if (!this.currentInteractions) return;
            this.currentInteractions.forEach(inter => {
                if (inter.type === 'highlights' && inter.selectors) {
                    inter.selectors.forEach(selector => {
                        const target = document.querySelector(selector);
                        if (target) {
                            target.classList.add('km-highlight');
                        }
                    });
                }
            });
        },

        nextStep() {
            if (this.currentStepIndex < this.totalSteps - 1) {
                this.currentStepIndex++;
                this.scrollToTop();
            }
        },

        prevStep() {
            if (this.currentStepIndex > 0) {
                this.currentStepIndex--;
                this.scrollToTop();
            }
        },

        scrollToTop() {
            this.$nextTick(() => {
                if (this.$refs.contentScroll) {
                    this.$refs.contentScroll.scrollTo({ top: 0, behavior: 'smooth' });
                }
            });
        },

        applyAndSimulateChat(promptStr) {
            if (promptStr) {
                this.promptInput = promptStr;
                if (window.ElementPlus) {
                    ElementPlus.ElMessage({
                        message: '自动填充完毕，执行测试',
                        type: 'success',
                        duration: 1500
                    });
                }
                this.simulateAIChat();
            }
        },

        submitQuiz(idx, interaction) {
            const state = this.stepStates[this.currentStepIndex];
            state.quizSubmitted = true;
        },

        getFillBlankParts(templateStr) {
            // 将 "你是一个{0}，请帮我{1}。" 拆分为数组
            const parts = [];
            const regex = /\{(\d+)\}/g;
            let lastIndex = 0;
            let match;
            
            while ((match = regex.exec(templateStr)) !== null) {
                if (match.index > lastIndex) {
                    parts.push({ type: 'text', text: templateStr.substring(lastIndex, match.index) });
                }
                parts.push({ type: 'blank', index: parseInt(match[1], 10) });
                lastIndex = regex.lastIndex;
            }
            if (lastIndex < templateStr.length) {
                parts.push({ type: 'text', text: templateStr.substring(lastIndex) });
            }
            return parts;
        },

        submitFillBlank(interaction) {
            let result = interaction.template;
            const blanks = this.stepStates[this.currentStepIndex].blanks;
            
            // 替换逻辑
            for (let i = 0; i < interaction.blanks.length; i++) {
                const val = blanks[i] ? blanks[i] : `[${interaction.blanks[i]}]`; // Default placeholder if empty
                result = result.replace(new RegExp(`\\{${i}\\}`, 'g'), val);
            }
            
            this.promptInput = result;
            this.simulateAIChat();
        },

        renderMarkdownInline(text) {
            if (!text) return "";
            return window.marked ? window.marked.parse(text) : text;
        },

        /**
         * 模拟 AI 聊天交互
         */
        async simulateAIChat() {
            const text = this.promptInput.trim();
            if (!text) return;
            
            this.chatHistory.push({ role: 'user', content: text });
            this.promptInput = '';
            this.aiLoading = true;
            this.$nextTick(this.scrollPlayground);
            
            setTimeout(async () => {
                try {
                    // 后端 API 尚未接入，抛出模拟错误
                    throw new Error("AI 交互功能后端 API 尚未接入");
                } catch (error) {
                    this.chatHistory.push({
                        role: 'error',
                        content: error.message || "请求 AI 时发生错误"
                    });
                } finally {
                    this.aiLoading = false;
                    this.$nextTick(this.scrollPlayground);
                }
            }, 1200);
        },

        scrollPlayground() {
            if (this.$refs.playgroundScroll) {
                const el = this.$refs.playgroundScroll;
                el.scrollTop = el.scrollHeight;
            }
        }
    },

    mounted() {
        this.fetchDirectory();
        
        // 监听浏览器前进后退
        window.addEventListener('popstate', (e) => {
             const pathObj = window.location.pathname.match(/\/tutorial\/([^\/]+)\//);
             if (pathObj && pathObj[1]) {
                 this.loadTutorial(pathObj[1], false);
             }
        });
    }
});
