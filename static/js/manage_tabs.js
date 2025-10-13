  // same tab-switching JS
  (function(){
    const tabsEl = document.getElementById('tabs');
    if (!tabsEl) return;
    const tabs = Array.from(tabsEl.querySelectorAll('[role="tab"]'));
    const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));

    function activateTab(newTab){
      tabs.forEach(t => { t.setAttribute('aria-selected','false'); t.setAttribute('tabindex','-1'); });
      panels.forEach(p => { p.hidden = true; p.classList.remove('active'); });

      newTab.setAttribute('aria-selected','true');
      newTab.setAttribute('tabindex','0');
      const panel = document.getElementById(newTab.getAttribute('aria-controls'));
      panel.hidden = false;
      panel.classList.add('active');
      newTab.focus();
    }

    tabs.forEach(t => t.addEventListener('click', () => activateTab(t)));
    tabs.forEach((t, idx) => {
      t.addEventListener('keydown', (e) => {
        const key = e.key;
        let newIndex = null;
        if (key === 'ArrowRight' || key === 'ArrowDown') newIndex = (idx + 1) % tabs.length;
        else if (key === 'ArrowLeft' || key === 'ArrowUp') newIndex = (idx - 1 + tabs.length) % tabs.length;
        else if (key === 'Home') newIndex = 0;
        else if (key === 'End') newIndex = tabs.length - 1;
        if (newIndex !== null){ e.preventDefault(); activateTab(tabs[newIndex]); }
      });
    });
  })();
