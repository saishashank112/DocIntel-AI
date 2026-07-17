/* ==========================================================================
   DocIntel AI Platform - Landing Page Interactive Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle Orchestration
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navbar = document.querySelector('.navbar');

    if (mobileToggle && navbar) {
        mobileToggle.addEventListener('click', () => {
            navbar.classList.toggle('active');
        });

        // Close mobile menu when clicking a link
        const navLinks = document.querySelectorAll('.nav-links a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navbar.classList.remove('active');
            });
        });
    }

    // 2. Interactive Feature Showcase Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const showcasePanels = document.querySelectorAll('.showcase-panel');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Deactivate all buttons
            tabButtons.forEach(b => b.classList.remove('active'));
            // Activate current button
            btn.classList.add('active');

            // Hide all panels
            showcasePanels.forEach(panel => {
                panel.classList.remove('active');
            });

            // Show current panel
            const activePanel = document.getElementById(`panel-${targetTab}`);
            if (activePanel) {
                activePanel.classList.add('active');
            }
        });
    });

    // 3. Code Clipboard Copy Functionality
    const copyButton = document.getElementById('copy-code-btn');
    const codeElement = document.querySelector('.code-box code');

    if (copyButton && codeElement) {
        copyButton.addEventListener('click', () => {
            const codeText = codeElement.textContent;
            
            navigator.clipboard.writeText(codeText).then(() => {
                const originalText = copyButton.textContent;
                copyButton.textContent = 'Copied!';
                copyButton.style.color = 'var(--accent-teal)';
                copyButton.style.borderColor = 'var(--accent-teal)';

                setTimeout(() => {
                    copyButton.textContent = originalText;
                    copyButton.style.color = '';
                    copyButton.style.borderColor = '';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy code: ', err);
            });
        });
    }
});
