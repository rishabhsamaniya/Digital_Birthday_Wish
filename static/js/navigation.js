/**
 * Birthday Memories - Complete Journey Navigation Controller
 */
window.BirthdayNavigation = {
    steps: [
        { id: 'landing', title: 'Welcome', path: '' },
        { id: 'birthday', title: 'Birthday Reveal', path: 'birthday/' },
        { id: 'memories', title: 'Memories', path: 'memories/' },
        { id: 'timeline', title: 'Our Journey', path: 'timeline/' },
        { id: 'love_notes', title: 'Love Notes', path: 'love-notes/' },
        { id: 'gallery', title: 'Photo Gallery', path: 'gallery/' },
        { id: 'videos', title: 'Video Messages', path: 'videos/' },
        { id: 'secret', title: 'Secret Message', path: 'secret/' },
        { id: 'final_wish', title: 'Grand Finale', path: 'final-wish/' }
    ],

    currentStepIndex: 0,
    profileSlug: '',

    init(profileSlug, currentStepId) {
        this.profileSlug = profileSlug || '';
        if (currentStepId) {
            const foundIndex = this.steps.findIndex(s => s.id === currentStepId);
            if (foundIndex !== -1) {
                this.currentStepIndex = foundIndex;
            }
        }
        console.log(`🧭 Navigation Controller Initialized: Step ${this.currentStepIndex + 1} of ${this.steps.length}`);
    },

    getNextUrl() {
        if (this.currentStepIndex < this.steps.length - 1) {
            const nextStep = this.steps[this.currentStepIndex + 1];
            return `/${this.profileSlug}/${nextStep.path}`;
        }
        return null;
    },

    getPrevUrl() {
        if (this.currentStepIndex > 0) {
            const prevStep = this.steps[this.currentStepIndex - 1];
            return `/${this.profileSlug}/${prevStep.path}`;
        }
        return null;
    },

    next() {
        const url = this.getNextUrl();
        if (url) window.location.href = url;
    },

    prev() {
        const url = this.getPrevUrl();
        if (url) window.location.href = url;
    }
};
