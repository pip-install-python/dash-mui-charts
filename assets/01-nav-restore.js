/**
 * Restore nav tree expanded state and active selection after Dash renders.
 * Uses dash_clientside.set_props (Dash 3.x) for reliable prop updates.
 */
(function() {
    function restoreNavTree() {
        if (!window.dash_clientside || !window.dash_clientside.set_props) {
            return false;
        }

        // Restore expanded items from localStorage
        try {
            var stored = localStorage.getItem('nav-tree-expanded');
            if (stored) {
                var expanded = JSON.parse(stored);
                if (Array.isArray(expanded) && expanded.length > 0) {
                    window.dash_clientside.set_props('nav-tree', { expandedItems: expanded });
                }
            }
        } catch(e) {}

        // Sync selected item to current pathname
        var pathname = window.location.pathname || '/';
        window.dash_clientside.set_props('nav-tree', { selectedItems: pathname });

        return true;
    }

    function waitAndRestore() {
        if (restoreNavTree()) return;
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
