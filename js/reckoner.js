/* reckoner.js — the four calculators. Same formulas as tools/figures.py, printed
   under each box so a reader can check them on paper. No storage, no network. */
(function () {
  "use strict";
  var C = 299792458, MPH = 0.44704, G = 6.6743e-11, M = 5.9722e24;
  var RE = 6378137, SIDEREAL = 86164.0905;          // equatorial radius, sidereal day

  function $(id) { return document.getElementById(id); }
  function n(v, d) { return v.toLocaleString(undefined, { maximumFractionDigits: d === undefined ? 0 : d }); }
  function on(el, f) { if (!el) return; el.addEventListener("input", f); f(); }

  /* 1 — settin' still */
  var lat = $("lat");
  on(lat, function () {
    var phi = Math.max(-90, Math.min(90, parseFloat(lat.value) || 0)) * Math.PI / 180;
    var spin = 2 * Math.PI * RE * Math.cos(phi) / SIDEREAL;
    var orbit = 29780, galaxy = 230000;
    $("still-out").innerHTML =
      n(spin) + " m/s on the spin" +
      "<small>" + n(spin / MPH) + " mph, eastward, and you cannot feel a bit of it. " +
      "On top of that: " + n(orbit) + " m/s around the Sun and about " + n(galaxy) +
      " m/s around the middle of the galaxy — three speeds, three different things " +
      "to be fast compared to. Add them and you get " + n(spin + orbit + galaxy) +
      " m/s, which is " + (100 * (spin + orbit + galaxy) / C).toFixed(3) +
      "% of light speed, for doin' nothing whatsoever.</small>";
  });

  /* 2 — the air tax */
  function air() {
    var v = (parseFloat($("v").value) || 0) * MPH;
    var cd = parseFloat($("cd").value), A = parseFloat($("area").value) || 0.1;
    var alt = Math.max(0, parseFloat($("alt").value) || 0);
    var rho = 1.225 * Math.pow(1 - 2.25577e-5 * alt, 4.2559);   // standard atmosphere
    var F = 0.5 * rho * v * v * cd * A, P = F * v;
    var half = 0.5 * rho * Math.pow(v / 2, 2) * cd * A * (v / 2);
    $("air-out").innerHTML =
      n(P / 745.7, 1) + " hp, on air alone" +
      "<small>" + n(F) + " newtons of shove — about " + n(F / 9.81) + " kg hangin' off " +
      "the bumper — and " + n(P / 1000, 1) + " kW to keep it there. " +
      "At half this speed the same shape costs " + n(half / 745.7, 1) + " hp, which is " +
      n(P / half, 1) + " times less. Air is " + rho.toFixed(3) + " kg/m³ at this height. " +
      "Tyres, driveline and hills are extra.</small>";
  }
  ["v", "cd", "area", "alt"].forEach(function (id) { on($(id), air); });

  /* 3 — addin' speeds */
  function add() {
    var u = parseFloat($("u").value), w = parseFloat($("w").value);
    var s = (u + w) / (1 + u * w);
    $("add-out").innerHTML =
      s.toFixed(6) + "c" +
      "<small>" + u.toFixed(3) + "c and " + w.toFixed(3) + "c. Plain arithmetic says " +
      (u + w).toFixed(3) + "c" + (u + w > 1 ? ", which is over the ceilin' and does not happen" : "") +
      ". The correct sum is (u+v)/(1+uv/c²) = " + s.toFixed(6) + "c — that is " +
      n(s * C) + " m/s. Push both sliders all the way and it still lands on 1.</small>";
  }
  on($("u"), add); on($("w"), add);

  /* 4 — the watch */
  function clock() {
    var b = parseFloat($("b").value), g = 1 / Math.sqrt(1 - b * b);
    var yearSec = 31557600, lost = yearSec - yearSec / g;
    $("clock-out").innerHTML =
      "×" + g.toFixed(6) + " slower" +
      "<small>At " + b.toFixed(6) + "c — " + n(b * C) + " m/s — a year on the porch is " +
      (1 / g).toFixed(6) + " years in the cab. You come home " +
      (lost > 86400 ? n(lost / 86400, 1) + " days" : n(lost, 1) + " seconds") +
      " younger than the folks who stayed. Gettin' a 2,000 kg truck to this speed takes " +
      ((g - 1) * 2000 * C * C).toExponential(2) + " joules.</small>";
  }
  on($("b"), clock);
})();
