/*
 * Open off-site navigation links in a new tab.
 *
 * The "Forum" entry in menu.main points at the Discourse instance, and the theme's
 * header.html has no way to set target="_blank" on a menu item. Forking that partial
 * is ruled out: it carries the hamburger button, the dropdown markup and the whole
 * mobile menu, all wired to the theme's scripts.js. This runs from the theme's
 * designated params.custom_js extension point instead.
 *
 * Scope is deliberately narrow — the header nav and the footer's menu column only.
 * Links in page content, the social icons and the licence link keep their current
 * behaviour. Without JS the links still work, they just open in the same tab.
 */
(function () {
  "use strict";

  var SELECTOR = ".main-menu a[href], .footer__menu a[href]";

  function markExternal(root) {
    root.querySelectorAll(SELECTOR).forEach(function (link) {
      // link.hostname is the resolved host, so relative URLs match our own and
      // are skipped. Empty hostname means a fragment or mailto: — leave those be.
      if (!link.hostname || link.hostname === window.location.hostname) return;
      link.target = "_blank";
      // Without noopener the opened page can reach back through window.opener.
      link.rel = "noopener noreferrer";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      markExternal(document);
    });
  } else {
    markExternal(document);
  }
})();
