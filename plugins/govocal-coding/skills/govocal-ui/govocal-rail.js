/* govocal-rail.js — scroll-aware edge fades for horizontal scrollers: .gv-rail
   carousels AND .gv-bo-tabs strips (a narrow stage can hold fewer tabs than a
   method page carries — the strip self-scrolls, and the fade says "more this way").
   At rest the first item sits flush (no left fade); a left fade appears once
   scrolled, and the right fade drops at the end. Pairs with the .rail--fade-left /
   .rail--fade-right rules in govocal-ui.css (.gv-rail) + govocal-bo.css (.gv-bo-tabs).
   Both runtime marks (data-railbound + rail--fade-*) are stripped by the provenance
   hash, so binding a LOCKED bo-tabs instance keeps it LINKED. */
(function () {
  var SCROLLERS = '.gv-rail, .gv-bo-tabs';
  function update(rail) {
    var max = rail.scrollWidth - rail.clientWidth;
    var x = rail.scrollLeft;
    var overflowing = max > 1;
    rail.classList.toggle('rail--fade-left', overflowing && x > 1);
    rail.classList.toggle('rail--fade-right', overflowing && x < max - 1);
  }
  function init(root) {
    (root || document).querySelectorAll(SCROLLERS).forEach(function (rail) {
      if (rail.dataset.railbound !== undefined) return;
      rail.dataset.railbound = '';
      update(rail);
      rail.addEventListener('scroll', function () { update(rail); }, { passive: true });
    });
  }
  function updateAll() { document.querySelectorAll(SCROLLERS).forEach(update); }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', function () { init(); });
  // re-measure after async content (web fonts, avatar faces) shifts widths
  window.addEventListener('load', function () { init(); updateAll(); });
  window.addEventListener('resize', updateAll);
  window.GVRail = { init: init, update: update, updateAll: updateAll };
})();
