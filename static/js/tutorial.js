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
        currentInteraction() {
            return this.currentStepData ? this.currentStepData.interaction : null;
        },
        hasInteraction() {
            return this.currentInteraction && this.currentInteraction.length > 0 && this.currentInteraction[0].type === 'chat';
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

        applyInteractionPrompt() {
            if (this.hasInteraction) {
                const interaction = this.currentInteraction[0];
                if (interaction.prompt) {
                    this.promptInput = interaction.prompt;
                    if (window.ElementPlus) {
                        ElementPlus.ElMessage({
                            message: '提示词已填入右侧游乐场',
                            type: 'success',
                            duration: 2000
                        });
                    }
                }
            }
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
