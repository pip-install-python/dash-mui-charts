/**
 * Restore nav tree expanded state and active selection after Dash renders.
 * Uses dash_clientside.set_props when available, with graceful fallback.
 */
(function() {
    function restoreNavTree() {
        // Need set_props to be available
        if (!window.dash_clientside || typeof window.dash_clientside.set_props !== 'function') {
            return false;
        }

        try {
            // Restore expanded items from localStorage
            var stored = localStorage.getItem('nav-tree-expanded');
            if (stored) {
                var expanded = JSON.parse(stored);
                if (Array.isArray(expanded) && expanded.length > 0) {
                    window.dash_clientside.set_props('nav-tree', { expandedItems: expanded });
                }
            }

            // Sync selected item to current pathname
            var pathname = window.location.pathname || '/';
            window.dash_clientside.set_props('nav-tree', { selectedItems: pathname });
        } catch(e) {
            // set_props API may differ across Dash versions — fail silently
            // The tree will still work, just without restored state on this load
        }

        return true;
    }

    function waitAndRestore() {
        if (restoreNavTree()) return;
        // Retry until set_props is available (max ~5 seconds)
        if (waitAndRestore._retries > 25) return;
        waitAndRestore._retries = (waitAndRestore._retries || 0) + 1;
        setTimeout(waitAndRestore, 200);
    }

    if (document.readyState === 'complete') {
        setTimeout(waitAndRestore, 300);
    } else {
        window.addEventListener('load', function() {
            setTimeout(waitAndRestore, 300);
        });
    }
})();
