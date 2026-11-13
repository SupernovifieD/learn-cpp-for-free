// The book's additions to mdBook's stock scripts: the theme menu, tabs, and
// keyboard access to the sidebar button and to content that scrolls sideways.

(() => {
    'use strict';

    // --- Themes -------------------------------------------------------------
    // The book offers Auto, Light and Navy. Removing the other entries (rather
    // than only hiding them) keeps the arrow keys in the menu working.
    for (const name of ['rust', 'coal', 'ayu']) {
        const button = document.getElementById('mdbook-theme-' + name);
        if (button) {
            button.parentElement.remove();
        }
    }

    // --- Sidebar button ------------------------------------------------------
    // mdBook's button is a <label> for a hidden checkbox, which the Tab key
    // skips and which may not carry aria-expanded. As a button it can be
    // reached and used with the keyboard.
    const sidebarToggle = document.getElementById('mdbook-sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.setAttribute('role', 'button');
        sidebarToggle.tabIndex = 0;
        sidebarToggle.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                sidebarToggle.click();
            }
        });
    }

    // --- Tabs ---------------------------------------------------------------
    // scripts/mdbook_cppbook.py writes each group of tabs as
    //   <div class="tabs"><section class="tab" data-tab="Label">...</section>...</div>
    // This turns a group into a tablist. Choosing a tab also chooses it in
    // every group with the same labels, and the choice is remembered.
    const STORE = 'cppbook-tabs';
    let saved = {};
    try {
        saved = JSON.parse(localStorage.getItem(STORE)) || {};
    } catch (error) {
        // No storage (private mode, for example): the choice lasts for this page.
    }

    const groups = [];

    function show(group, label) {
        group.tabs.forEach((tab, index) => {
            const selected = group.labels[index] === label;
            tab.setAttribute('aria-selected', selected ? 'true' : 'false');
            tab.tabIndex = selected ? 0 : -1;
            group.panels[index].hidden = !selected;
        });
    }

    function choose(group, label, origin) {
        // Other groups on the page may change height, so keep the tab that
        // was used at the same place on the screen.
        const before = origin ? origin.getBoundingClientRect().top : 0;
        for (const other of groups) {
            if (other.key === group.key) {
                show(other, label);
            }
        }
        if (origin) {
            window.scrollBy(0, origin.getBoundingClientRect().top - before);
        }
        saved[group.key] = label;
        try {
            localStorage.setItem(STORE, JSON.stringify(saved));
        } catch (error) {
            // See above.
        }
    }

    document.querySelectorAll('.tabs').forEach((element, number) => {
        const panels = Array.from(element.querySelectorAll(':scope > .tab'));
        if (panels.length === 0) {
            return;
        }
        const labels = panels.map(panel => panel.dataset.tab);
        const group = { key: labels.join('|'), labels, panels, tabs: [] };

        const list = document.createElement('div');
        list.className = 'tab-list';
        list.setAttribute('role', 'tablist');
        list.setAttribute('aria-label', 'Instructions for ' + labels.join(', '));

        panels.forEach((panel, index) => {
            const tab = document.createElement('button');
            tab.type = 'button';
            tab.id = 'tab-' + number + '-' + index;
            tab.textContent = labels[index];
            tab.setAttribute('role', 'tab');
            panel.id = 'tabpanel-' + number + '-' + index;
            tab.setAttribute('aria-controls', panel.id);
            panel.setAttribute('role', 'tabpanel');
            panel.setAttribute('aria-labelledby', tab.id);
            panel.tabIndex = 0;

            tab.addEventListener('click', () => choose(group, labels[index], tab));
            tab.addEventListener('keydown', event => {
                const last = panels.length - 1;
                const target = {
                    ArrowRight: index === last ? 0 : index + 1,
                    ArrowLeft: index === 0 ? last : index - 1,
                    Home: 0,
                    End: last,
                }[event.key];
                if (target === undefined) {
                    return;
                }
                // mdBook turns the page on the arrow keys; inside the tabs they move between tabs.
                event.preventDefault();
                event.stopPropagation();
                choose(group, labels[target], group.tabs[target]);
                group.tabs[target].focus();
            });

            group.tabs.push(tab);
            list.appendChild(tab);
        });

        element.insertBefore(list, panels[0]);
        element.classList.add('tabs-ready');
        groups.push(group);
        show(group, labels.includes(saved[group.key]) ? saved[group.key] : labels[0]);
    });

    // --- Content that scrolls sideways ---------------------------------------
    // A wide table or a long line of code scrolls inside its own box. Make
    // that box reachable with the keyboard, so it can be scrolled without a
    // mouse.
    function markScrollable() {
        document.querySelectorAll('.table-wrapper, pre > code').forEach(box => {
            if (box.scrollWidth > box.clientWidth) {
                box.tabIndex = 0;
                box.setAttribute('role', 'region');
                box.setAttribute('aria-label', (box.tagName === 'CODE' ? 'Code' : 'Table') + ', scrolls sideways');
            } else {
                box.removeAttribute('tabindex');
                box.removeAttribute('role');
                box.removeAttribute('aria-label');
            }
        });
    }
    markScrollable();
    window.addEventListener('resize', markScrollable);
    window.addEventListener('load', markScrollable);
    if (document.fonts) {
        document.fonts.ready.then(markScrollable);
    }
})();
