"""The stylesheet, in one place, so the pages carry it inline and load nothing."""

CSS = """
:root{
 --ink:#17120e; --paper:#f6efe3; --panel:#fffaf0; --line:#d8c9ae;
 --accent:#b7222a; --accent2:#e08a1e; --muted:#6a5c48;
 --display:"Bebas Neue","Oswald","Haettenschweiler","Arial Narrow",system-ui,sans-serif;
 --body:Georgia,"Iowan Old Style","Times New Roman",serif;
 --mono:"SFMono-Regular",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
 :root{--ink:#f0e6d6; --paper:#12100e; --panel:#1b1714; --line:#3a3128;
       --accent:#ef4b4b; --accent2:#f0b04a; --muted:#a6947c;}
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
 font-size:19px;line-height:1.62}
.wrap{max-width:46rem;margin:0 auto;padding:0 1.1rem}
a{color:var(--accent);text-underline-offset:.16em}
a:hover{color:var(--accent2)}

header.top{border-bottom:4px solid var(--accent);background:var(--panel)}
header.top .wrap{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;
 padding-top:.7rem;padding-bottom:.7rem}
header.top .mark{font-family:var(--display);font-size:1.5rem;letter-spacing:.06em;
 text-transform:uppercase;color:var(--ink);text-decoration:none;white-space:nowrap}
header.top .mark b{color:var(--accent)}
nav.site{display:flex;flex-wrap:wrap;gap:.1rem .9rem;font-family:var(--display);
 font-size:1rem;letter-spacing:.08em;text-transform:uppercase}
nav.site a{text-decoration:none}
nav.site a[aria-current]{color:var(--ink);border-bottom:3px solid var(--accent2)}

h1{font-family:var(--display);font-size:clamp(2.6rem,10vw,4.6rem);line-height:.92;
 letter-spacing:.01em;text-transform:uppercase;margin:1.6rem 0 .3rem}
h1 .sub{display:block;font-family:var(--body);font-size:clamp(1rem,3vw,1.25rem);
 text-transform:none;letter-spacing:0;color:var(--muted);line-height:1.4;
 margin-top:.6rem;font-style:italic}
h2{font-family:var(--display);font-size:clamp(1.7rem,5.5vw,2.4rem);line-height:1;
 text-transform:uppercase;letter-spacing:.02em;margin:2.4rem 0 .6rem;
 border-bottom:2px solid var(--line);padding-bottom:.3rem}
h3{font-family:var(--display);font-size:1.35rem;text-transform:uppercase;
 letter-spacing:.04em;margin:1.8rem 0 .3rem}
p{margin:.85rem 0}
.lede{font-size:1.16rem}
.lede:first-letter{font-family:var(--display);float:left;font-size:3.1em;line-height:.78;
 padding:.06em .09em 0 0;color:var(--accent)}

.pull{font-family:var(--display);font-size:clamp(1.5rem,5vw,2.1rem);line-height:1.04;
 text-transform:uppercase;color:var(--accent);border-left:6px solid var(--accent2);
 padding:.2rem 0 .2rem 1rem;margin:1.8rem 0}

.pull.eq{text-transform:none;letter-spacing:0;font-family:var(--mono);
 font-size:clamp(1.02rem,3.4vw,1.4rem);line-height:1.5;color:var(--ink);
 border-left-color:var(--accent)}
.box{background:var(--panel);border:2px solid var(--line);border-left:8px solid var(--accent2);
 padding:.9rem 1.1rem;margin:1.5rem 0}
.box h3{margin-top:.2rem}
.box.sum{border-left-color:var(--accent)}
.fig{margin:1.7rem 0}
.fig .canvas{overflow-x:auto;border:2px solid var(--line);background:var(--panel)}
.fig svg{width:100%;min-width:640px;height:auto;display:block}
.fig figcaption{font-size:.86rem;color:var(--muted);margin-top:.45rem}
figure{margin:1.7rem 0}

table{border-collapse:collapse;width:100%;font-size:.94rem;margin:1.2rem 0}
th,td{border:1px solid var(--line);padding:.36rem .5rem;text-align:left;vertical-align:top}
th{font-family:var(--display);text-transform:uppercase;letter-spacing:.05em;
 font-weight:400;font-size:1rem;background:var(--panel)}
td.n{text-align:right;font-family:var(--mono);font-size:.86rem;white-space:nowrap}
.scroll{overflow-x:auto}

ol.rungs{list-style:none;padding:0;margin:1.4rem 0;counter-reset:rung}
ol.rungs li{border-top:1px solid var(--line);padding:.9rem 0;display:grid;
 grid-template-columns:5.6rem 1fr;gap:.2rem .9rem}
ol.rungs li:last-child{border-bottom:1px solid var(--line)}
ol.rungs .v{font-family:var(--mono);font-size:.84rem;color:var(--accent);
 text-align:right;padding-top:.35rem;line-height:1.35}
ol.rungs .v b{display:block;font-family:var(--display);font-size:1.45rem;color:var(--ink);
 letter-spacing:.02em}
ol.rungs h3{margin:0}
ol.rungs p{margin:.25rem 0 0}
ol.rungs .show{font-size:.84rem;color:var(--muted);font-family:var(--mono)}

.calc{background:var(--panel);border:2px solid var(--line);padding:1rem 1.1rem;margin:1.6rem 0}
.calc label{display:block;font-family:var(--display);text-transform:uppercase;
 letter-spacing:.06em;font-size:.95rem;margin:.7rem 0 .15rem}
.calc input,.calc select{font:inherit;font-family:var(--mono);font-size:.95rem;
 padding:.35rem .5rem;border:2px solid var(--line);background:var(--paper);
 color:var(--ink);width:100%;max-width:18rem}
.calc input[type=range]{padding:0;border:0;max-width:100%}
.calc .out{font-family:var(--display);font-size:clamp(1.6rem,6vw,2.6rem);line-height:1.06;
 color:var(--accent);margin:.8rem 0 .1rem;word-break:break-word}
.calc .out small{display:block;font-family:var(--body);font-size:.95rem;font-style:italic;
 color:var(--muted);line-height:1.4;margin-top:.35rem}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:.2rem 1.4rem}

.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem;
 margin:1.6rem 0;padding:0;list-style:none}
.cards li{border:2px solid var(--line);background:var(--panel);padding:.8rem .9rem}
.cards h3{margin:.1rem 0 .3rem}
.cards h3 a{text-decoration:none}
.cards p{margin:.2rem 0 0;font-size:.95rem}

.src{font-size:.82rem;color:var(--muted)}
sup.ref a{text-decoration:none;font-family:var(--mono);font-size:.74em;
 padding:0 .12em;color:var(--accent)}
ol.sources{font-size:.92rem}
ol.sources li{margin:.55rem 0}

footer.foot{margin-top:3.5rem;border-top:4px solid var(--accent);background:var(--panel);
 padding:1.3rem 0 2.2rem;font-size:.88rem;color:var(--muted)}
footer.foot a{color:var(--accent)}
footer.foot .fleet{margin-top:.6rem;line-height:1.9}
footer.foot .support,footer.foot .maker{margin-top:.5rem}
.prev-next{display:flex;justify-content:space-between;gap:1rem;margin:2.6rem 0 0;
 font-family:var(--display);text-transform:uppercase;letter-spacing:.05em}
.prev-next a{text-decoration:none}

@media (max-width:30rem){
 body{font-size:18px}
 ol.rungs li{grid-template-columns:1fr}
 ol.rungs .v{text-align:left;padding-top:0}
 ol.rungs .v b{display:inline;font-size:1.25rem;margin-right:.5rem}
}
@media print{nav.site,.calc{display:none}body{background:#fff;color:#000}}
"""
