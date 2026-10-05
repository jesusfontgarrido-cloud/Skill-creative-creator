#!/usr/bin/env python3
"""Base de datos de referencias para creador-skills-creativas (solo librería estándar).

Subcomandos:
  init        crea refs.json con el perfil del creativo
  validate    comprueba esquema, duplicados y mínimos (50 en explore, 200 en search)
  board       genera un tablero HTML autocontenido (modo pick o rate)
  apply       fusiona en refs.json el JSON que descarga el tablero
  stats       analiza las puntuaciones y propone el patrón de gusto
  export-skill  vuelca las listas de referencias para la skill final

Esquema de cada referencia (refs.json -> "refs"):
  id, url, title, author, platform, thumb, group, tipologia, tags[], note, license,
  phase ("explore" | "search"), contrast (bool), picked (bool), score (1-10 | null)
"""
import argparse
import datetime
import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

REQUIRED = ("id", "url", "platform", "group")
LIKE_MIN = 6  # score >= 6 -> le gusta; <= 5 -> evitar
TRACKING = re.compile(r"^(utm_|fbclid|gclid|igshid|ref$|source$)")


def norm_url(u):
    p = urlsplit(u.strip())
    q = [(k, v) for k, v in parse_qsl(p.query) if not TRACKING.match(k)]
    path = p.path.rstrip("/") or "/"
    return urlunsplit((p.scheme.lower(), p.netloc.lower().removeprefix("www."), path, urlencode(q), ""))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


# ----------------------------------------------------------------------------- init
def cmd_init(a):
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    target = d / "refs.json"
    if target.exists() and not a.force:
        sys.exit(f"{target} ya existe (usa --force para sobrescribir).")
    save(target, {
        "profile": {
            "oficio": a.oficio, "foco": a.foco, "keyword": a.keyword or "",
            "created": datetime.date.today().isoformat(),
        },
        "refs": [],
    })
    print(f"Creado {target}")


# ----------------------------------------------------------------------------- validate
def cmd_validate(a):
    data = load(a.file)
    refs = data["refs"]
    errors, warns = [], []
    seen_id, seen_url = {}, {}
    for i, r in enumerate(refs):
        for k in REQUIRED:
            if not r.get(k):
                errors.append(f"ref #{i} ({r.get('id', '?')}): falta '{k}'")
        if r.get("url") and not r["url"].startswith(("http://", "https://")):
            errors.append(f"{r.get('id')}: url no válida")
        if r.get("id") in seen_id:
            errors.append(f"id duplicado: {r['id']}")
        seen_id[r.get("id")] = True
        if r.get("url"):
            n = norm_url(r["url"])
            if n in seen_url:
                errors.append(f"url duplicada: {r['id']} == {seen_url[n]}")
            seen_url[n] = r.get("id")
        if not r.get("tags"):
            warns.append(f"{r.get('id')}: sin tags (el análisis de patrón los necesita)")
        if r.get("phase") == "explore" and not r.get("tipologia"):
            errors.append(f"{r.get('id')}: en explore hace falta 'tipologia' (la opción que el creativo elige)")
        if r.get("phase") not in ("explore", "search"):
            errors.append(f"{r.get('id')}: phase debe ser 'explore' o 'search'")

    explore = [r for r in refs if r.get("phase") == "explore"]
    search = [r for r in refs if r.get("phase") == "search"]
    print(f"Total {len(refs)} | explore {len(explore)} | search {len(search)}")

    if a.stage == "explore":
        if len(explore) != 50:
            errors.append(f"explore debe tener 50 referencias, hay {len(explore)}")
        per = Counter(r["group"] for r in explore)
        for g, n in per.items():
            if n != 5:
                errors.append(f"grupo '{g}' tiene {n} referencias (deben ser 5)")
        if len(per) != 10:
            warns.append(f"hay {len(per)} grupos (lo previsto son 10 grupos x 5)")
    elif a.stage == "search":
        if len(search) < a.min:
            errors.append(f"search tiene {len(search)} referencias, el mínimo es {a.min}")
        plats = Counter(r["platform"] for r in search)
        if len(plats) < 3:
            warns.append(f"solo {len(plats)} plataformas en search; usa al menos 3")
        if search:
            top, n = plats.most_common(1)[0]
            if n / len(search) > 0.5:
                warns.append(f"'{top}' aporta {n * 100 // len(search)}% de la búsqueda; diversifica")
            share = sum(1 for r in search if r.get("contrast")) / len(search)
            if share < 0.12:
                warns.append(f"solo {share:.0%} de contraste; sin ejemplos fuera de gusto no habrá puntuaciones bajas")
        print("Plataformas:", dict(plats))
        print("Grupos:", dict(Counter(r["group"] for r in search)))
    for w in warns[:25]:
        print("AVISO:", w)
    for e in errors[:50]:
        print("ERROR:", e)
    if errors:
        sys.exit(1)
    print("OK")


# ----------------------------------------------------------------------------- board
BOARD = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fafaf9;--fg:#1c1917;--mut:#78716c;--card:#fff;--bd:#e7e5e4;--ok:#15803d;--no:#b91c1c;--ac:#1d4ed8}
@media(prefers-color-scheme:dark){:root{--bg:#141413;--fg:#f5f5f4;--mut:#a8a29e;--card:#1f1e1d;--bd:#34312f;--ok:#4ade80;--no:#f87171;--ac:#60a5fa}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--bd);padding:12px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}
header h1{font-size:16px;margin:0 auto 0 0}
button,select{font:inherit;color:inherit;background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:6px 12px;cursor:pointer}
button.primary{background:var(--ac);border-color:var(--ac);color:#fff}
main{padding:16px;max-width:1400px;margin:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.card.sel{outline:3px solid var(--ok)}
.thumb{aspect-ratio:4/3;background:var(--bd);display:flex;align-items:center;justify-content:center;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover}
.thumb span{color:var(--mut);padding:8px;text-align:center;font-size:13px}
.meta{padding:10px 12px;display:flex;flex-direction:column;gap:6px;flex:1}
.meta a{color:var(--fg);font-weight:600;text-decoration:none}
.meta small{color:var(--mut)}
.tip{font-size:16px}
.tags{display:flex;flex-wrap:wrap;gap:4px}.tags i{font-style:normal;font-size:12px;border:1px solid var(--bd);border-radius:99px;padding:0 7px;color:var(--mut)}
.scale{display:grid;grid-template-columns:repeat(10,1fr);gap:3px}
.scale button{padding:5px 0;font-size:13px;border-radius:6px}
.scale button.on{color:#fff;border-color:transparent}
.scale button.on.lo{background:var(--no)}.scale button.on.hi{background:var(--ok)}
.note{width:100%;border:1px solid var(--bd);border-radius:6px;padding:5px 8px;background:var(--bg);color:inherit;font:inherit;font-size:13px}
section.grp{margin-bottom:28px}section.grp h2{font-size:17px;margin:0 0 4px}
.hint{color:var(--mut);margin:0 0 10px;font-size:13px}
.legend{color:var(--mut);font-size:13px;max-width:1400px;margin:0 auto;padding:8px 16px 0}
</style></head><body>
<header><h1>__TITLE__</h1><span id="prog"></span><span id="filters"></span><button class="primary" id="export">Descargar resultado</button></header>
<div class="legend" id="legend"></div>
<main id="main"></main>
<script>
const DATA=__DATA__;
const MODE=DATA.mode, KEY="board-"+MODE+"-"+DATA.slug;
let st={}; try{st=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
st.picks=st.picks||{}; st.reasons=st.reasons||{}; st.ratings=st.ratings||{};
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}};
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function thumb(r){
  const fb=`<span>${esc(r.platform)}<br>sin vista previa · abre el enlace</span>`;
  if(!r.thumb) return `<div class="thumb"><a href="${esc(r.url)}" target="_blank" rel="noopener">${fb}</a></div>`;
  return `<div class="thumb"><a href="${esc(r.url)}" target="_blank" rel="noopener" style="width:100%;height:100%"><img src="${esc(r.thumb)}" loading="lazy" referrerpolicy="no-referrer" alt="${esc(r.title)}" onerror="this.parentNode.innerHTML='${fb.replace(/'/g,"")}'"></a></div>`;
}
function info(r){
  const head=r.tipologia?`<b class="tip">${esc(r.tipologia)}</b><small>${esc(r.note||"")}</small><small>Ejemplo: <a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title||r.url)}</a> · ${esc(r.platform)}</small>`
    :`<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title||r.url)}</a><small>${esc(r.author||"")} · ${esc(r.platform)}</small>`;
  return head+`<div class="tags">${(r.tags||[]).map(t=>`<i>${esc(t)}</i>`).join("")}</div>`;
}
/* ---------- modo pick ---------- */
function renderPick(){
  document.getElementById("legend").textContent="De cada grupo de 5, elige la 1 que mejor represente lo que buscas. Si ninguna te convence, pulsa «Ninguna». Opcional: una frase con el porqué.";
  const groups=[...new Set(DATA.refs.map(r=>r.group))];
  document.getElementById("main").innerHTML=groups.map(g=>{
    const items=DATA.refs.filter(r=>r.group===g);
    return `<section class="grp"><h2>${esc(g)}</h2><p class="hint">Elige 1 de ${items.length}</p><div class="grid">${items.map(r=>
      `<div class="card ${st.picks[g]===r.id?"sel":""}" data-g="${esc(g)}" data-id="${esc(r.id)}">${thumb(r)}<div class="meta">${info(r)}<button data-pick="${esc(r.id)}" data-g="${esc(g)}">${st.picks[g]===r.id?"✓ Elegida":"Elegir esta"}</button></div></div>`).join("")}</div>
      <p><button data-none="${esc(g)}">Ninguna</button> <input class="note" style="max-width:520px" data-reason="${esc(g)}" placeholder="¿Por qué? (opcional)" value="${esc(st.reasons[g]||"")}"></p></section>`}).join("");
  prog();
}
function prog(){
  if(MODE==="pick"){const groups=new Set(DATA.refs.map(r=>r.group));const n=[...groups].filter(g=>g in st.picks).length;document.getElementById("prog").textContent=`${n}/${groups.size} grupos resueltos`;}
  else{const n=DATA.refs.filter(r=>st.ratings[r.id]&&st.ratings[r.id].score).length;document.getElementById("prog").textContent=`${n}/${DATA.refs.length} puntuadas`;}
}
/* ---------- modo rate ---------- */
let filt="all", grp="all", cur=null;
function renderRate(){
  document.getElementById("legend").textContent="Puntúa de 1 a 10. 6–10 = me gusta (cuanto más alto, más lo quiero). 1–5 = no me gusta / hay que evitarlo. Atajo: pasa el ratón por una tarjeta y pulsa 1-9 (0 = 10).";
  const groups=[...new Set(DATA.refs.map(r=>r.group))];
  document.getElementById("filters").innerHTML=`<select id="f"><option value="all">Todas</option><option value="todo">Pendientes</option><option value="hi">Gustan (6+)</option><option value="lo">Evitar (≤5)</option></select> <select id="g"><option value="all">Todos los grupos</option>${groups.map(g=>`<option>${esc(g)}</option>`).join("")}</select>`;
  document.getElementById("f").value=filt;document.getElementById("g").value=grp;
  document.getElementById("f").onchange=e=>{filt=e.target.value;draw()};document.getElementById("g").onchange=e=>{grp=e.target.value;draw()};
  draw();
}
function draw(){
  const list=DATA.refs.filter(r=>{const s=(st.ratings[r.id]||{}).score;
    if(grp!=="all"&&r.group!==grp)return false;
    return filt==="all"||(filt==="todo"&&!s)||(filt==="hi"&&s>=6)||(filt==="lo"&&s&&s<=5)});
  document.getElementById("main").innerHTML=`<div class="grid">${list.map(r=>{const v=st.ratings[r.id]||{};
    return `<div class="card" data-id="${esc(r.id)}">${thumb(r)}<div class="meta">${info(r)}<small>${esc(r.group)}</small>
    <div class="scale">${[1,2,3,4,5,6,7,8,9,10].map(n=>`<button data-s="${n}" class="${v.score===n?"on "+(n>=6?"hi":"lo"):""}">${n}</button>`).join("")}</div>
    <input class="note" data-note="${esc(r.id)}" placeholder="Nota (opcional)" value="${esc(v.note||"")}"></div></div>`}).join("")}</div>`;
  prog();
}
/* ---------- eventos ---------- */
document.addEventListener("click",e=>{
  const b=e.target.closest("button");if(!b)return;
  if(b.dataset.pick){st.picks[b.dataset.g]=b.dataset.pick;save();renderPick();}
  else if(b.dataset.none!==undefined){st.picks[b.dataset.none]=null;save();renderPick();}
  else if(b.dataset.s){const id=b.closest(".card").dataset.id;const v=st.ratings[id]=st.ratings[id]||{};v.score=+b.dataset.s;save();draw();}
});
document.addEventListener("input",e=>{
  if(e.target.dataset.reason!==undefined){st.reasons[e.target.dataset.reason]=e.target.value;save();}
  if(e.target.dataset.note){const id=e.target.dataset.note;const v=st.ratings[id]=st.ratings[id]||{};v.note=e.target.value;save();}
});
document.addEventListener("mouseover",e=>{const c=e.target.closest(".card");cur=c?c.dataset.id:null});
document.addEventListener("keydown",e=>{
  if(MODE!=="rate"||!cur||/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  if(/^[0-9]$/.test(e.key)){const id=cur;const v=st.ratings[id]=st.ratings[id]||{};v.score=e.key==="0"?10:+e.key;save();
    const sy=window.scrollY;draw();window.scrollTo(0,sy);}
});
document.getElementById("export").onclick=()=>{
  const out=MODE==="pick"?{mode:"pick",picks:st.picks,reasons:st.reasons}:{mode:"rate",ratings:Object.fromEntries(Object.entries(st.ratings).filter(([k,v])=>v.score))};
  const url=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download=MODE==="pick"?"picks.json":"ratings.json";a.click();
};
MODE==="pick"?renderPick():renderRate();
</script></body></html>
"""


def cmd_board(a):
    data = load(a.file)
    refs = data["refs"]
    if a.mode == "pick":
        refs = [r for r in refs if r.get("phase") == "explore"]
        title = "Elige 1 de cada 5"
    else:
        refs = [r for r in refs if r.get("phase") == "search" or r.get("picked")]
        title = "Puntúa cada referencia del 1 al 10"
    if not refs:
        sys.exit("No hay referencias para este modo (¿phase correcta?).")
    keep = ("id", "url", "title", "author", "platform", "thumb", "group", "tags", "tipologia", "note")
    slim = [{k: r.get(k) for k in keep} for r in refs]
    slug = re.sub(r"\W+", "-", (data["profile"].get("foco") or "board").lower()).strip("-")[:40]
    payload = json.dumps({"mode": a.mode, "slug": slug, "refs": slim}, ensure_ascii=False).replace("</", "<\\/")
    out = BOARD.replace("__TITLE__", html.escape(title)).replace("__DATA__", payload)
    Path(a.out).write_text(out, encoding="utf-8")
    print(f"Tablero escrito en {a.out} ({len(slim)} referencias, modo {a.mode})")


# ----------------------------------------------------------------------------- apply
def cmd_apply(a):
    data = load(a.file)
    res = load(a.result)
    by_id = {r["id"]: r for r in data["refs"]}
    if res.get("mode") == "pick":
        chosen = {v for v in res["picks"].values() if v}
        for r in data["refs"]:
            if r.get("phase") == "explore":
                r["picked"] = r["id"] in chosen
        data["profile"]["pick_reasons"] = {g: t for g, t in res.get("reasons", {}).items() if t}
        print(f"{len(chosen)} semillas marcadas (picked=true).")
    else:
        n = 0
        for rid, v in res["ratings"].items():
            if rid in by_id:
                by_id[rid]["score"] = v["score"]
                if v.get("note"):
                    by_id[rid]["user_note"] = v["note"]
                n += 1
            else:
                print("AVISO: id desconocido", rid)
        print(f"{n} puntuaciones aplicadas.")
    save(a.file, data)


# ----------------------------------------------------------------------------- stats
def mean(xs):
    return sum(xs) / len(xs)


def cmd_stats(a):
    data = load(a.file)
    refs = data["refs"]
    rated = [r for r in refs if r.get("score") is not None]
    if not rated:
        sys.exit("No hay referencias puntuadas todavía.")
    scores = [r["score"] for r in rated]
    gm = mean(scores)
    hi = [r for r in rated if r["score"] >= LIKE_MIN]
    out = [f"# Análisis de gusto — {data['profile'].get('oficio')} / {data['profile'].get('foco')}", ""]
    out.append(f"Puntuadas: {len(rated)} | media global {gm:.2f} | gustan (≥{LIKE_MIN}): {len(hi)} ({len(hi) / len(rated):.0%}) | evitar (≤{LIKE_MIN - 1}): {len(rated) - len(hi)}")
    dist = Counter(scores)
    out.append("Distribución: " + " ".join(f"{n}:{dist.get(n, 0)}" for n in range(1, 11)))
    share = len(hi) / len(rated)
    if share > 0.85:
        out.append("\n> AVISO: casi todo está por encima de 5. Hay poco contraste; el patrón de «evitar» será débil. Añade contraejemplos y repite una ronda.")
    if share < 0.15:
        out.append("\n> AVISO: casi todo está por debajo de 6. La búsqueda no ha dado con su gusto; revisa semillas y palabras clave.")

    tag_scores = defaultdict(list)
    for r in rated:
        for t in set(r.get("tags") or []):
            tag_scores[t].append(r["score"])

    def table(title, rows):
        out.append(f"\n## {title}\n")
        if not rows:
            out.append("_(nada con evidencia suficiente)_")
            return
        out.append("| tag | n | media | diferencia vs global |")
        out.append("|---|---|---|---|")
        for t, xs in rows:
            out.append(f"| {t} | {len(xs)} | {mean(xs):.1f} | {mean(xs) - gm:+.1f} |")

    ev = [(t, xs) for t, xs in tag_scores.items() if len(xs) >= a.min_n]
    table(f"Lo que le gusta (tags con n≥{a.min_n}, media ≥7)", sorted([x for x in ev if mean(x[1]) >= 7], key=lambda x: -mean(x[1])))
    table(f"Lo que hay que evitar (tags con n≥{a.min_n}, media ≤5)", sorted([x for x in ev if mean(x[1]) <= 5], key=lambda x: mean(x[1])))
    # tensiones: tags con mucha dispersión
    tens = [(t, xs) for t, xs in ev if max(xs) - min(xs) >= 6 and 5 < mean(xs) < 7]
    table("Tensiones (mismo tag puntuado muy alto y muy bajo: hay otra variable que lo decide)", sorted(tens, key=lambda x: -len(x[1])))
    few = sorted((t, xs) for t, xs in tag_scores.items() if len(xs) < a.min_n)
    out.append(f"\n## Huecos de evidencia\n\n{len(few)} tags con menos de {a.min_n} referencias (no usar como regla): " + ", ".join(t for t, _ in few[:40]))

    for label, key in (("Por grupo", "group"), ("Por plataforma", "platform")):
        agg = defaultdict(list)
        for r in rated:
            agg[r.get(key)].append(r["score"])
        out.append(f"\n## {label}\n")
        out.append("| " + key + " | n | media | % gustan |")
        out.append("|---|---|---|---|")
        for k, xs in sorted(agg.items(), key=lambda x: -mean(x[1])):
            out.append(f"| {k} | {len(xs)} | {mean(xs):.1f} | {sum(1 for x in xs if x >= LIKE_MIN) / len(xs):.0%} |")

    explore = [r for r in refs if r.get("phase") == "explore" and "picked" in r]
    if explore:
        t_all, t_pick = Counter(), Counter()
        for r in explore:
            for t in set(r.get("tags") or []):
                t_all[t] += 1
                t_pick[t] += bool(r.get("picked"))
        rows = sorted(((t, t_pick[t], n) for t, n in t_all.items() if n >= 3), key=lambda x: -x[1] / x[2])
        out.append("\n## Señal de la ronda 1 (tags elegidos vs vistos, n≥3)\n")
        out.append("| tag | elegidas | vistas |")
        out.append("|---|---|---|")
        out += [f"| {t} | {p} | {n} |" for t, p, n in rows[:15]]
    reasons = data["profile"].get("pick_reasons")
    if reasons:
        out.append("\n## Motivos que dio al elegir\n")
        out += [f"- **{g}**: {t}" for g, t in reasons.items()]
    notes = [r for r in rated if r.get("user_note")]
    if notes:
        out.append("\n## Notas de puntuación (lo que dijo con sus palabras)\n")
        out += [f"- ({r['score']}) {r.get('title') or r['id']}: {r['user_note']}" for r in sorted(notes, key=lambda r: -r["score"])]
    print("\n".join(out))


# ----------------------------------------------------------------------------- export-skill
def cmd_export(a):
    data = load(a.file)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rated = [r for r in data["refs"] if r.get("score") is not None]

    def line(r):
        tags = ", ".join(r.get("tags") or [])
        extra = f" — «{r['user_note']}»" if r.get("user_note") else ""
        return f"- **{r['score']}** [{r.get('title') or r['id']}]({r['url']}) · {r['platform']} · _{r['group']}_ · {tags}{extra}"

    def write(name, title, intro, items):
        by_g = defaultdict(list)
        for r in items:
            by_g[r["group"]].append(r)
        lines = [f"# {title}", "", intro, ""]
        for g, rs in by_g.items():
            lines += [f"## {g}", ""] + [line(r) for r in rs] + [""]
        (out / name).write_text("\n".join(lines), encoding="utf-8")

    write("referencias-gustan.md", "Referencias que le gustan (6-10)",
          "Ordenadas por puntuación dentro de cada grupo. Son la vara de medir de lo que SÍ.",
          sorted([r for r in rated if r["score"] >= LIKE_MIN], key=lambda r: -r["score"]))
    write("referencias-evitar.md", "Referencias a evitar (1-5)",
          "Ordenadas de peor a menos mala. Son la vara de medir de lo que NO.",
          sorted([r for r in rated if r["score"] < LIKE_MIN], key=lambda r: r["score"]))
    keep = ("id", "url", "title", "author", "platform", "group", "tipologia", "tags", "score", "user_note", "license")
    save(out / "referencias.json", {"profile": data["profile"], "refs": [{k: r.get(k) for k in keep} for r in rated]})
    print(f"Exportado a {out}/ (referencias-gustan.md, referencias-evitar.md, referencias.json)")


# ----------------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("init"); x.add_argument("--dir", required=True); x.add_argument("--oficio", required=True)
    x.add_argument("--foco", required=True); x.add_argument("--keyword"); x.add_argument("--force", action="store_true"); x.set_defaults(f=cmd_init)
    x = s.add_parser("validate"); x.add_argument("file"); x.add_argument("--stage", choices=["any", "explore", "search"], default="any")
    x.add_argument("--min", type=int, default=200); x.set_defaults(f=cmd_validate)
    x = s.add_parser("board"); x.add_argument("file"); x.add_argument("--mode", choices=["pick", "rate"], required=True)
    x.add_argument("--out", required=True); x.set_defaults(f=cmd_board)
    x = s.add_parser("apply"); x.add_argument("file"); x.add_argument("result"); x.set_defaults(f=cmd_apply)
    x = s.add_parser("stats"); x.add_argument("file"); x.add_argument("--min-n", type=int, default=3); x.set_defaults(f=cmd_stats)
    x = s.add_parser("export-skill"); x.add_argument("file"); x.add_argument("--out", required=True); x.set_defaults(f=cmd_export)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
