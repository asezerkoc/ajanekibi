// 30 karakteri voksel olarak stüdyo ışığında render eder (Playwright + headless Chromium).
// Kullanım: node oyun/karakterler/render/render.js [kod ...]   (girdi: cikti/3b/*.png, çıktı: cikti/render/*.png)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), http = require("http");
const KOK = path.resolve(__dirname, "..");
const liste = JSON.parse(fs.readFileSync(path.join(__dirname, "kadro.json"), "utf8"));
const secili = process.argv.slice(2);
const sunucu = http.createServer((q, s) => {
  const p = path.join(KOK, decodeURIComponent(q.url.split("?")[0]));
  if (!p.startsWith(KOK) || !fs.existsSync(p)) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { "Content-Type": p.endsWith(".html") ? "text/html; charset=utf-8" : p.endsWith(".js") ? "text/javascript" : "image/png" });
  fs.createReadStream(p).pipe(s);
}).listen(0);
(async () => {
  const port = sunucu.address().port;
  const tarayici = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  fs.mkdirSync(path.join(KOK, "cikti", "render"), { recursive: true });
  for (const k of liste) {
    if (secili.length && !secili.includes(k.kod)) continue;
    const sayfa = await tarayici.newPage({ viewport: { width: 768, height: 1056 } });
    sayfa.on("pageerror", e => console.log("hata:", k.kod, e.message));
    await sayfa.goto(`http://localhost:${port}/render/sahne.html`);
    const veri = await sayfa.evaluate(a => window.ciz(...a), [`../cikti/3b/${k.kod}.png`, k.gok, k.zemin, k.aci]);
    fs.writeFileSync(path.join(KOK, "cikti", "render", k.kod + "_ham.png"), Buffer.from(veri.split(",")[1], "base64"));
    console.log("render:", k.kod);
    await sayfa.close();
  }
  await tarayici.close(); sunucu.close();
})();
