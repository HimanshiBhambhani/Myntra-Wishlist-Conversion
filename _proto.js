/* Prototype interactions.
   Two behaviours only: tapping a card navigates, tapping its × hides the suggestion
   in place and offers an undo. Hiding never touches the wishlist itself — that is a
   separate, explicit choice in the snackbar. */

(function () {
  "use strict";

  var SNACK_ID = "proto-snackbar";

  function stripOf(card) {
    return card.closest(".wl");
  }

  function countLabel(strip) {
    return strip ? strip.querySelector(".wl-title") : null;
  }

  function setCount(strip, delta) {
    var label = countLabel(strip);
    if (!label) return;
    label.innerHTML = label.innerHTML.replace(/(\d+) matches/, function (_, n) {
      return Math.max(0, parseInt(n, 10) + delta) + " matches";
    });
  }

  function clearSnackbar(strip) {
    var existing = document.getElementById(SNACK_ID);
    if (existing) existing.remove();
  }

  function showSnackbar(strip, card) {
    clearSnackbar(strip);

    var bar = document.createElement("div");
    bar.id = SNACK_ID;
    bar.className = "snackbar";
    bar.innerHTML =
      '<div class="msg">Hidden from recommendations.<b>Remove from wishlist too?</b></div>' +
      '<span class="remove">REMOVE</span>' +
      '<span class="undo">UNDO</span>';

    strip.insertAdjacentElement("afterend", bar);

    bar.querySelector(".undo").addEventListener("click", function () {
      restore(card);
      bar.remove();
    });

    bar.querySelector(".remove").addEventListener("click", function () {
      card.remove();
      setCount(strip, -1);
      bar.remove();
    });
  }

  function hide(card) {
    if (card.classList.contains("hidden")) return;

    card.classList.add("hidden");

    var x = card.querySelector(".xbtn");
    if (x) x.style.display = "none";

    var img = card.querySelector(".wl-img");
    if (img && !img.querySelector(".hidden-tag")) {
      var tag = document.createElement("span");
      tag.className = "hidden-tag";
      tag.innerHTML = "<span>HIDDEN</span>";
      img.appendChild(tag);
    }

    showSnackbar(stripOf(card), card);
  }

  function restore(card) {
    card.classList.remove("hidden");
    var x = card.querySelector(".xbtn");
    if (x) x.style.display = "";
    var tag = card.querySelector(".hidden-tag");
    if (tag) tag.remove();
  }

  function switchCategory(chip) {
    var pair = chip.closest(".pair");
    if (!pair) return;
    var cat = chip.getAttribute("data-cat");
    pair.querySelectorAll(".pchip").forEach(function (c) {
      c.classList.toggle("on", c === chip);
    });
    pair.querySelectorAll(".wl-rail[data-cat]").forEach(function (r) {
      r.hidden = r.getAttribute("data-cat") !== cat;
    });
  }

  document.addEventListener("click", function (e) {
    var chip = e.target.closest(".pchip");
    if (chip) {
      e.preventDefault();
      switchCategory(chip);
      return;
    }

    var x = e.target.closest(".xbtn");
    if (x) {
      e.preventDefault();
      e.stopPropagation();
      var card = x.closest(".wl-card");
      if (card && stripOf(card)) hide(card);
      return;
    }

    var nav = e.target.closest("[data-href]");
    if (nav) window.location.href = nav.getAttribute("data-href");
  });
})();
