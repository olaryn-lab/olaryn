/* Tallyward ledger: a browser-only simulation of the reservation rules (no network).
   Holds are checked against the available balance one at a time, so two competing
   holds can never both succeed. Unsettled holds lapse after their TTL. */
(function () {
  var root = document.getElementById("ledger");
  if (!root) return;

  var START = 35;          // credits at the start of a run
  var SETTLE_SHARE = 0.75; // a "settle" uses 75% of the hold; the rest returns
  var MAX_HOLDS = 6;
  var MAX_EVENTS = 6;

  var out = {
    balance: document.getElementById("f-balance"),
    held: document.getElementById("f-held"),
    avail: document.getElementById("f-avail"),
    holds: document.getElementById("holds"),
    events: document.getElementById("events"),
    expire: root.querySelector('[data-act="expire"]'),
    status: document.getElementById("sr-status")
  };
  var state;
  var focusId = null;
  var newestEvent = false;

  function fresh() { return { balance: START, holds: [], seq: 0, events: [] }; }
  function held() {
    return state.holds.reduce(function (n, h) { return h.status === "pending" ? n + h.amount : n; }, 0);
  }
  function available() { return state.balance - held(); }
  function find(id) { for (var i = 0; i < state.holds.length; i++) if (state.holds[i].id === id) return state.holds[i]; return null; }
  function used(h) { return Math.ceil(h.amount * SETTLE_SHARE); }
  function note(kind, label, text) {
    state.events.unshift({ kind: kind, label: label, text: text });
    if (state.events.length > MAX_EVENTS) state.events.length = MAX_EVENTS;
    newestEvent = true;
  }
  function trimHolds() {
    while (state.holds.length > MAX_HOLDS) {
      var drop = -1;
      for (var i = 0; i < state.holds.length; i++) if (state.holds[i].status !== "pending") { drop = i; break; }
      if (drop < 0) return;
      state.holds.splice(drop, 1);
    }
  }

  function reserve(amount) {
    var free = available();
    if (amount > free) {
      note("err", "rejected", "Reserve " + amount + " with " + free + " available.");
      return;
    }
    var hold = { id: "res_" + (++state.seq), amount: amount, status: "pending", isNew: true };
    state.holds.push(hold);
    trimHolds();
    note("hold", "held", hold.id + " reserved " + amount + " of " + state.balance + ". Available " + available() + ".");
  }
  function settle(id) {
    var h = find(id);
    if (!h || h.status !== "pending") return;
    var u = used(h);
    state.balance -= u;
    h.status = "settled"; h.used = u; h.isNew = true;
    note("ok", "settled", h.id + " used " + u + " of " + h.amount + ". Available " + available() + ".");
    focusId = h.id;
  }
  function release(id) {
    var h = find(id);
    if (!h || h.status !== "pending") return;
    h.status = "released"; h.isNew = true;
    note("", "released", h.id + " returned " + h.amount + ". Available " + available() + ".");
    focusId = h.id;
  }
  function expireAll() {
    var count = 0, back = 0;
    state.holds.forEach(function (h) { if (h.status === "pending") { h.status = "expired"; h.isNew = true; count++; back += h.amount; } });
    if (!count) { note("", "idle", "No hold is waiting to expire."); return; }
    if (count) note("err", "expired", "15 minutes pass. " + count + (count === 1 ? " hold lapses" : " holds lapse") + ", " + back + " returned. Available " + available() + ".");
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function chip(state_, text) {
    var c = el("span", "chip", text);
    if (state_) c.setAttribute("data-state", state_);
    return c;
  }
  function statusChip(h) {
    if (h.status === "pending") return chip("hold", "pending");
    if (h.status === "settled") return chip("ok", "settled " + h.used + ", " + (h.amount - h.used) + " returned");
    if (h.status === "released") return chip("", "released");
    return chip("err", "expired");
  }
  function button(label, aria, act, id) {
    var b = el("button", "btn btn-small", label);
    b.type = "button";
    b.setAttribute("aria-label", aria);
    b.setAttribute("data-act", act);
    b.setAttribute("data-id", id);
    return b;
  }

  function render() {
    out.balance.textContent = state.balance;
    out.held.textContent = held();
    out.avail.textContent = available();

    out.holds.textContent = "";
    if (!state.holds.length) {
      var empty = el("tr");
      var cell = el("td", "empty", "No holds yet.");
      cell.colSpan = 4;
      empty.appendChild(cell);
      out.holds.appendChild(empty);
    }
    state.holds.forEach(function (h) {
      var tr = el("tr", h.isNew ? "is-new" : "");
      var th = el("th", "mono", h.id);
      th.scope = "row";
      th.tabIndex = -1;
      th.id = "hold-" + h.id;
      var amount = el("td", "num", String(h.amount));
      var status = el("td"); status.appendChild(statusChip(h));
      var acts = el("td", "acts");
      if (h.status === "pending") {
        acts.appendChild(button("Settle " + used(h), "Settle " + used(h) + " for " + h.id, "settle", h.id));
        acts.appendChild(button("Release", "Release " + h.id, "release", h.id));
      }
      [th, amount, status, acts].forEach(function (c) { tr.appendChild(c); });
      out.holds.appendChild(tr);
      h.isNew = false;
    });

    out.events.textContent = "";
    if (!state.events.length) out.events.appendChild(el("li", "", "No events yet."));
    state.events.forEach(function (e, i) {
      var li = el("li", i === 0 && newestEvent ? "is-new" : "");
      li.appendChild(chip(e.kind, e.label));
      li.appendChild(document.createTextNode(" " + e.text));
      out.events.appendChild(li);
    });
    out.status.textContent = state.events.length && newestEvent ? state.events[0].label + ". " + state.events[0].text : "";
    newestEvent = false;

    if (focusId) {
      var target = document.getElementById("hold-" + focusId);
      if (target) target.focus({ preventScroll: true });
      focusId = null;
    }
  }

  root.addEventListener("click", function (event) {
    var b = event.target.closest && event.target.closest("button[data-act]");
    if (!b || !root.contains(b)) return;
    var act = b.getAttribute("data-act");
    if (act === "reserve") reserve(Number(b.getAttribute("data-amount")));
    else if (act === "settle") settle(b.getAttribute("data-id"));
    else if (act === "release") release(b.getAttribute("data-id"));
    else if (act === "expire") expireAll();
    else if (act === "reset") { state = fresh(); note("", "reset", "Back to " + START + " credits."); }
    render();
  });

  // "Try it" buttons elsewhere on the page replay a rule in the ledger.
  document.addEventListener("click", function (event) {
    var b = event.target.closest && event.target.closest("[data-scenario]");
    if (!b) return;
    state = fresh();
    if (b.getAttribute("data-scenario") === "compete") { reserve(25); reserve(25); }
    else if (b.getAttribute("data-scenario") === "expire") { reserve(25); expireAll(); }
    render();
    var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    root.scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "start" });
  });

  state = fresh();
  render();
})();
