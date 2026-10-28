/* becertain.app: Einblenden beim Scrollen, Balken „Chance zu bestehen", Probier-eine-Frage.
   Ohne Abhängigkeiten, ohne Netzwerk, ohne Speicher. Bewegung nur über CSS, das bei
   prefers-reduced-motion abschaltet. Ohne JavaScript ist alles sichtbar (Klasse .js fehlt). */
(function () {
  "use strict";

  // 1. Einblenden beim Scrollen, einmal je Element
  var ziele = document.querySelectorAll("[data-reveal], .balken");
  if (!("IntersectionObserver" in window)) {
    ziele.forEach(function (el) { el.classList.add("is-sichtbar", "is-gefuellt"); });
  } else {
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add(e.target.classList.contains("balken") ? "is-gefuellt" : "is-sichtbar");
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.15 });
    ziele.forEach(function (el) { io.observe(el); });
  }

  // 2. Probier eine Frage
  var demo = document.getElementById("demo");
  var daten = document.getElementById("demo-aufgabe");
  if (!demo || !daten) return;
  var aufgabe;
  try { aufgabe = JSON.parse(daten.textContent); } catch (err) { return; }

  var BUCHSTABEN = "ABCDEFGH";
  var HAKEN = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var KREUZ = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4.5 4.5l7 7M11.5 4.5l-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

  var liste = demo.querySelector(".optionen");
  var pruefen = demo.querySelector("[data-pruefen]");
  var grund = demo.querySelector(".demo__grund");
  var ergebnis = demo.querySelector(".demo__ergebnis");
  var gewaehlt = null;
  var geprueft = false;

  function text(el, t) { el.textContent = t; return el; }
  function neu(tag, klasse) { var el = document.createElement(tag); if (klasse) el.className = klasse; return el; }

  function optionenBauen() {
    liste.innerHTML = "";
    aufgabe.optionen.forEach(function (o, i) {
      var li = neu("li");
      var b = neu("button", "option");
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      b.dataset.id = o.id;
      var mark = neu("span", "option__mark");
      mark.setAttribute("aria-hidden", "true");
      mark.textContent = BUCHSTABEN[i];
      var t = neu("span", "option__text");
      var sr = neu("span", "sr-only");
      sr.textContent = "Antwort " + BUCHSTABEN[i] + ": ";
      t.appendChild(sr);
      t.appendChild(document.createTextNode(o.text));
      b.appendChild(mark);
      b.appendChild(t);
      b.addEventListener("click", function () { waehlen(o.id); });
      li.appendChild(b);
      liste.appendChild(li);
    });
  }

  function waehlen(id) {
    if (geprueft) return;
    gewaehlt = id;
    liste.querySelectorAll(".option").forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.id === id ? "true" : "false");
    });
    pruefen.disabled = false;
    grund.hidden = true;
  }

  function quelleText(f) {
    var t = "§\u00a0" + f.paragraf;
    if (f.absatz) t += " Abs.\u00a0" + f.absatz;
    if (f.satz) t += " Satz\u00a0" + f.satz;
    if (f.nummer) t += " Nr.\u00a0" + f.nummer;
    return t + " " + f.kurz;
  }

  function auswerten() {
    if (!gewaehlt || geprueft) return;
    geprueft = true;
    var richtigId = aufgabe.loesung.richtig;
    var istRichtig = gewaehlt === richtigId;
    var buchstabeRichtig = "";

    liste.querySelectorAll(".option").forEach(function (b, i) {
      var id = b.dataset.id;
      var mark = b.querySelector(".option__mark");
      b.disabled = true;
      b.removeAttribute("aria-pressed");
      var wort = null;
      if (id === richtigId) buchstabeRichtig = BUCHSTABEN[i];
      if (id === gewaehlt && istRichtig) {
        b.classList.add("is-richtig"); mark.innerHTML = HAKEN; wort = "Richtig, deine Wahl";
      } else if (id === gewaehlt) {
        b.classList.add("is-falsch"); mark.innerHTML = KREUZ; wort = "Falsch, deine Wahl";
      } else if (id === richtigId) {
        b.classList.add("is-loesung"); mark.innerHTML = HAKEN; wort = "Richtige Antwort";
      } else {
        b.classList.add("is-neutral");
      }
      if (wort) b.querySelector(".option__text").appendChild(text(neu("span", "option__wort"), wort));
    });

    pruefen.parentNode.hidden = true;

    // Rückmeldung: Symbol, Wort, Farbe
    var r = neu("div", "rueckmeldung" + (istRichtig ? "" : " rueckmeldung--falsch"));
    r.tabIndex = -1;
    var sym = neu("span", "rueckmeldung__symbol");
    sym.innerHTML = istRichtig ? HAKEN : KREUZ;
    var mitte = neu("div");
    mitte.appendChild(text(neu("p", "rueckmeldung__wort"), istRichtig ? "Richtig." : "Falsch."));
    if (!istRichtig) mitte.appendChild(text(neu("p", "rueckmeldung__satz"), "Richtig ist " + buchstabeRichtig + "."));
    var punkte = text(neu("span", "rueckmeldung__punkte"), (istRichtig ? "1" : "0") + " von 1 Punkt");
    r.appendChild(sym); r.appendChild(mitte); r.appendChild(punkte);

    // Erklärung und Quelle mit Zitat
    var erk = neu("div", "erklaerung is-eingeblendet");
    erk.appendChild(text(neu("p", "label"), "Erklärung"));
    erk.appendChild(text(neu("p"), aufgabe.erklaerung));
    erk.appendChild(text(neu("p", "label"), aufgabe.fundstellen.length > 1 ? "Quellen" : "Quelle"));
    aufgabe.fundstellen.forEach(function (f, i) {
      var box = neu("div", "quelle");
      var kopf = neu("button", "quelle__kopf");
      kopf.type = "button";
      kopf.setAttribute("aria-expanded", "true");
      kopf.setAttribute("aria-controls", "demo-zitat-" + i);
      kopf.textContent = quelleText(f);
      var zitat = neu("div", "quelle__zitat");
      zitat.id = "demo-zitat-" + i;
      zitat.appendChild(text(neu("p"), "„" + f.zitat + "“"));
      zitat.appendChild(text(neu("p", "quelle__stand"), f.titel + ", Rechtsstand " + aufgabe.rechtsstand + "."));
      kopf.addEventListener("click", function () {
        var offen = kopf.getAttribute("aria-expanded") === "true";
        kopf.setAttribute("aria-expanded", offen ? "false" : "true");
        zitat.hidden = offen;
      });
      box.appendChild(kopf); box.appendChild(zitat);
      erk.appendChild(box);
    });
    var nochmal = neu("p", "demo__nochmal");
    var nb = text(neu("button", "text-button"), "Noch einmal versuchen");
    nb.type = "button";
    nb.addEventListener("click", zuruecksetzen);
    nochmal.appendChild(nb);
    erk.appendChild(nochmal);

    ergebnis.innerHTML = "";
    r.classList.add("is-eingeblendet");
    ergebnis.appendChild(r);
    ergebnis.appendChild(erk);
    r.focus({ preventScroll: false });
  }

  function zuruecksetzen() {
    gewaehlt = null; geprueft = false;
    ergebnis.innerHTML = "";
    optionenBauen();
    pruefen.disabled = true;
    pruefen.parentNode.hidden = false;
    grund.hidden = false;
    var erste = liste.querySelector(".option");
    if (erste) erste.focus();
  }

  pruefen.addEventListener("click", auswerten);
  optionenBauen();
  demo.hidden = false;
  var ohne = document.getElementById("demo-ohne-js");
  if (ohne) ohne.hidden = true;
})();
