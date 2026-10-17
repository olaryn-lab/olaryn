/* Olaryn theme toggle. Loaded in <head> so the saved choice applies before first paint.
   No choice saved = the page follows the OS (CSS handles it); a click saves light or dark. */
(function () {
  var KEY = "olaryn-theme";
  var root = document.documentElement;
  root.classList.add("js"); // pages style script-dependent states under .js
  var query = window.matchMedia("(prefers-color-scheme: dark)");
  var COLORS = { light: "#FAFBFC", dark: "#12161A" };

  function saved() {
    try { var v = localStorage.getItem(KEY); return v === "light" || v === "dark" ? v : null; } catch (e) { return null; }
  }
  function effective() { return root.getAttribute("data-theme") || (query.matches ? "dark" : "light"); }
  function paintBrowserChrome(theme) {
    var metas = document.querySelectorAll('meta[name="theme-color"]');
    for (var i = 0; i < metas.length; i++) { metas[i].setAttribute("content", COLORS[theme]); metas[i].setAttribute("media", "all"); }
  }
  function sync() {
    var theme = effective();
    var buttons = document.querySelectorAll(".theme-toggle");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].hidden = false;
      buttons[i].setAttribute("data-mode", theme);
      buttons[i].setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    }
  }
  function apply(theme) {
    root.setAttribute("data-theme", theme);
    paintBrowserChrome(theme);
    sync();
  }

  var initial = saved();
  if (initial) root.setAttribute("data-theme", initial);

  document.addEventListener("DOMContentLoaded", function () {
    if (initial) paintBrowserChrome(initial);
    sync();
    document.addEventListener("click", function (event) {
      var button = event.target.closest && event.target.closest(".theme-toggle");
      if (!button) return;
      var next = effective() === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* private mode: the choice lasts for this page view */ }
    });
  });
  window.addEventListener("load", sync); // the OS preference can settle after first script run
  // Follow the OS while no choice is saved; follow other tabs when one is.
  var onSystemChange = function () { if (!saved()) sync(); };
  if (query.addEventListener) query.addEventListener("change", onSystemChange); else if (query.addListener) query.addListener(onSystemChange);
  window.addEventListener("storage", function (event) {
    if (event.key !== KEY) return;
    var value = saved();
    if (value) apply(value); else { root.removeAttribute("data-theme"); sync(); }
  });
})();
