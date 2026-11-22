# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/dimasskuy/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/dimasskuy/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One day of world news. One PNG. Zero dependencies. A single deterministic Python program draws Sunday 22 November 2026 — dot-matrix world map, six headlines, a market chart and one brighter story — pixel by pixel.

<p align="center">
  <img src="preview.png" alt="The generated entry: world news of 22 November 2026 in one image" width="640"/>
  <br/>
  <sub><i>The actual output of <code>main.py</code> — every pixel below is drawn by code, not pasted in.</i></sub>
</p>

---

## 🌍 What's in the image

| # | Story | Where |
|---|-------|-------|
| 🚀 | Russia fires **186 drones** in one night; Ukraine downs **161**, strikes hit 18 sites; Ukrainian drones set Russian ship Sparta II ablaze | Ukraine / Baltic |
| 💥 | Iran strikes US bases and a civilian plant in Bahrain — IRGC missile-drone attack, **2 hurt** | Bahrain |
| 🌡️ | COP31 final draft drops the words **"fossil fuels"** entirely — first admission the world will overshoot **1.5°C** | Antalya |
| 🤝 | EU and Indonesia sign a trade deal after **10 years** of talks — tariffs gone on **98%** of goods | Brussels |
| 🚢 | Funeral boat capsizes in Nigeria: **24 dead, 24 rescued** in Bayelsa | Nigeria |
| 🎮 | GTA VI: **$3.79bn** in one day, the biggest entertainment launch ever — **32.5m** pre-orders, Metacritic **99** | New York |
| ✨ | **Brighter news:** Lewis Pugh swims **15 km** through the Strait of Hormuz in 3 days, past burning tankers, to warn of war's toll on sea life | Strait of Hormuz |

A dot-matrix world map up top pins every story to where it happened, so the whole day reads at a glance — and still reads at 300 px wide.

## ⚙️ How it works

- **Pure Python 3.13 standard library** — `os`, `struct`, `zlib`. That's the whole dependency list. The PNG encoder is written by hand.
- **No network, no assets, no fonts on disk** — the pixel typeface, the map and the charts are all data + code inside `main.py`.
- **Fully deterministic** — run it twice, get the same bytes twice:

```text
$ sha256sum /output/entry.png
b73f6a39b422f91126684f3741cd499b8e9baff6a9bf4228dfec02a2aba5d10a  /output/entry.png
```

- **Output:** one `1024 × 1024` PNG, `20,591` bytes — comfortably inside the 1 MiB cap, and small files win ties.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png`. That's it — no install step, because there's nothing to install.

## 🧾 Facts & sources

Every headline was cross-checked across multiple international wires reporting on **Sunday, 22 November 2026**: the overnight Russian drone wave (186 launched, 161 downed) and the Sparta II fire in the Gulf of Finland, the Iranian missile-drone attack on US positions and a civilian industrial facility in Bahrain, COP31's final draft in Antalya omitting fossil fuels while admitting a 1.5°C overshoot, the EU–Indonesia trade deal signed in Brussels after a decade of talks, the capsized funeral boat in Bayelsa, Nigeria (24 dead, 24 rescued), GTA VI's record $3.79bn day-one sales, and Lewis Pugh's 15 km Strait of Hormuz swim.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zyx88bys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
