/**
 * Apply saved color scheme to <html> BEFORE Dash renders.
 * This runs immediately (assets are loaded before _dash-loading is shown)
 * so the loading screen CSS can use [data-mantine-color-scheme="dark"].
 *
 * Also swaps any page-level loading overlay logos to match the theme.
 * Prefixed with 00- to ensure it loads before other assets.
 */
(function() {
    try {
        var saved = localStorage.getItem('mantine-color-scheme-value');
        if (saved === 'dark' || saved === 'light') {
            document.documentElement.setAttribute('data-mantine-color-scheme', saved);
        }
        // Swap page loading logos after DOM is ready
        if (saved === 'dark') {
            var swapLogos = function() {
                var logos = document.querySelectorAll('.page-loading-overlay img');
                logos.forEach(function(img) {
                    if (img.src.indexOf('light_mode') !== -1) {
                        img.src = '/assets/2plot_dark_mode.png';
                    }
                });
            };
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', swapLogos);
            } else {
                swapLogos();
            }
        }
    } catch(e) {
        // localStorage unavailable — fall back to light
    }
})();
