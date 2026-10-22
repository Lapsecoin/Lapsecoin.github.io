// Downloads page: lists the releases that the core repo publishes as
// core/releases.json (same origin, written by its Pages workflow). All text
// goes in with textContent, so nothing in that file can add markup.
(function () {
  var latest = document.getElementById("dl-latest");
  var older = document.getElementById("dl-older");
  if (!latest || !older) return;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function link(href, text, cls) {
    var a = el("a", cls, text);
    a.href = href;
    return a;
  }
  function mb(n) { return (n / 1048576).toFixed(1) + " MB"; }
  function day(iso) {
    var d = new Date(iso + "T00:00:00Z");
    return isNaN(d) ? iso : d.toLocaleDateString("en", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
  }
  function vt(v) {
    if (!v) return el("span", "vt none", "No scan yet");
    var clean = v.flagged === 0;
    var wrap = el("span", "vt " + (clean ? "ok" : "warn"));
    wrap.appendChild(el("i"));
    wrap.appendChild(document.createTextNode(v.engines ? v.flagged + " of " + v.engines + " engines flagged" : v.text));
    return wrap;
  }
  function fail() {
    latest.appendChild(el("p", "note", "The release list could not be loaded. "));
    latest.lastChild.appendChild(link("https://github.com/Lapsecoin/core/releases", "Open the releases page on GitHub"));
  }

  function renderLatest(r, stable) {
    var p = el("section", "panel dl-latest");
    var main = el("div", "dl-main");
    main.appendChild(el("small", null, "Latest release, " + day(r.published)));
    main.appendChild(el("h2", null, r.version));
    var actions = el("div", "actions");
    actions.appendChild(link(r.msi.url, "Download for Windows (" + mb(r.msi.size) + ")", "btn primary lg"));
    if (r.linux) actions.appendChild(link(r.linux.url, "Linux (" + mb(r.linux.size) + ")", "btn lg"));
    main.appendChild(actions);
    main.appendChild(link(r.url, "Release notes", "dl-notes"));
    if (stable) {
      var perm = el("p", "dl-sub", "Stable link to the newest Windows installer, for scripts: ");
      perm.appendChild(link(stable, stable.replace("https://", "")));
      main.appendChild(perm);
    }
    p.appendChild(main);

    var facts = el("dl", "dl-facts");
    function fact(name, node) {
      var row = el("div");
      row.appendChild(el("dt", null, name));
      var dd = el("dd");
      dd.appendChild(node);
      row.appendChild(dd);
      facts.appendChild(row);
    }
    if (r.msi.sha256) fact("Windows SHA256", el("code", null, r.msi.sha256));
    if (r.linux && r.linux.sha256) fact("Linux SHA256", el("code", null, r.linux.sha256));
    var scan = el("span");
    scan.appendChild(vt(r.virustotal));
    if (r.virustotal) {
      scan.appendChild(document.createTextNode(" "));
      scan.appendChild(link(r.virustotal.url, "View scan"));
      if (r.virustotal.scanned) scan.appendChild(el("span", "dl-sub", "Scanned " + r.virustotal.scanned + ". Verdicts change over time, so the link shows the current result."));
    }
    fact("VirusTotal (Windows)", scan);
    p.appendChild(facts);
    latest.appendChild(p);
  }

  function renderOlder(list) {
    if (!list.length) return;
    older.appendChild(el("h2", "dl-h", "Previous releases"));
    var box = el("div", "tbl");
    var t = el("table", "dl-table");
    var head = el("tr");
    ["Version", "Date", "Windows", "Linux", "VirusTotal", "SHA256 (Windows)"].forEach(function (h) { head.appendChild(el("th", null, h)); });
    t.appendChild(head);
    list.forEach(function (r) {
      var row = el("tr");
      row.appendChild(el("td", null, r.version));
      row.appendChild(el("td", "dl-date", day(r.published)));
      var w = el("td"); w.appendChild(link(r.msi.url, "lapsecoin.msi")); row.appendChild(w);
      var l = el("td"); if (r.linux) l.appendChild(link(r.linux.url, "lapsecoin")); else l.textContent = "";
      row.appendChild(l);
      var v = el("td"); v.appendChild(vt(r.virustotal));
      if (r.virustotal) { v.appendChild(document.createTextNode(" ")); v.appendChild(link(r.virustotal.url, "scan")); }
      row.appendChild(v);
      var s = el("td"); if (r.msi.sha256) { var c = el("code", null, r.msi.sha256.slice(0, 12) + "..."); c.title = r.msi.sha256; s.appendChild(c); }
      row.appendChild(s);
      t.appendChild(row);
    });
    box.appendChild(t);
    older.appendChild(box);
  }

  fetch("core/releases.json", { cache: "no-cache" })
    .then(function (res) { if (!res.ok) throw new Error(res.status); return res.json(); })
    .then(function (data) {
      var list = (data && data.releases) || [];
      if (!list.length) return fail();
      renderLatest(list[0], data.latest_msi);
      renderOlder(list.slice(1));
      document.getElementById("dl-note").hidden = false;
    })
    .catch(fail);
})();
