// Starts Mermaid (theme/mermaid.min.js) with colors that match the book's theme.

(() => {
    'use strict';

    const html = document.documentElement;
    const isDark = () => ['navy', 'coal', 'ayu'].some(theme => html.classList.contains(theme));
    const dark = isDark();

    mermaid.initialize({ startOnLoad: true, theme: dark ? 'dark' : 'default' });

    // Mermaid cannot recolor a diagram it has drawn, so a page with diagrams
    // is loaded again when the reader switches between light and dark.
    new MutationObserver(() => {
        if (isDark() !== dark && document.querySelector('.mermaid')) {
            window.location.reload();
        }
    }).observe(html, { attributes: true, attributeFilter: ['class'] });
})();
