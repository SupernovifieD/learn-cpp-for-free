// Starts Mermaid (theme/mermaid.min.js) with colors that match the book's theme.

(() => {
    'use strict';

    const html = document.documentElement;
    const darkThemes = ['navy', 'coal', 'ayu'];
    const isDark = () => darkThemes.some(theme => html.classList.contains(theme));
    const currentTheme = () => ['navy', 'coal', 'ayu', 'rust'].find(theme => html.classList.contains(theme)) || 'light';
    const dark = isDark();

    const chartTheme = {
        light: { backgroundColor: '#ffffff', plotColorPalette: '#20609f' },
        rust: { backgroundColor: 'hsl(60, 9%, 87%)', plotColorPalette: '#20609f' },
        navy: { backgroundColor: '#161923', plotColorPalette: '#5aa9e6' },
        coal: { backgroundColor: '#131516', plotColorPalette: '#98a3ad' },
        ayu: { backgroundColor: '#0f141a', plotColorPalette: '#ffb454' },
    }[currentTheme()];
    const chartText = dark ? '#e6edf3' : '#131300';
    Object.assign(chartTheme, {
        titleColor: chartText,
        dataLabelColor: chartText,
        legendTextColor: chartText,
        xAxisLabelColor: chartText,
        xAxisTitleColor: chartText,
        xAxisTickColor: chartText,
        xAxisLineColor: chartText,
        yAxisLabelColor: chartText,
        yAxisTitleColor: chartText,
        yAxisTickColor: chartText,
        yAxisLineColor: chartText,
    });

    mermaid.initialize({
        startOnLoad: true,
        theme: dark ? 'dark' : 'default',
        flowchart: { diagramPadding: 6, nodeSpacing: 20 },
        sequence: {
            actorMargin: 30,
            width: 110,
            actorFontSize: 20,
            noteFontSize: 20,
            messageFontSize: 20,
        },
        xyChart: {
            width: 300,
            height: 260,
            xAxis: { labelFontSize: 13 },
            yAxis: { labelFontSize: 13 },
        },
        themeVariables: {
            edgeLabelBackground: dark ? chartTheme.backgroundColor : '#e8e8e8',
            xyChart: chartTheme,
        },
    });

    // Mermaid cannot recolor a diagram it has drawn, so a page with diagrams
    // is loaded again when the reader switches between light and dark.
    new MutationObserver(() => {
        if (isDark() !== dark && document.querySelector('.mermaid')) {
            window.location.reload();
        }
    }).observe(html, { attributes: true, attributeFilter: ['class'] });
})();
