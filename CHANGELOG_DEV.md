# Geliştirme kaydı

Her görev sonunda kısa kayıt: tarih ve görev · değişen dosyalar · önemli kararlar · çalıştırılan testler · açık sorunlar.
Eski kayıtlar kısa tutulur; ayrıntı gerekirse git geçmişine bakılır.

## Önceki işler (özet, git geçmişinden)
- `1889fb6` Savaşçı sınıfı (5 gövde GLB, yeniden rig + animasyon), Sv 70 ve son oyun dengesi.
- `d9f1acd` · `f65921b` · `032b90e` · `12e578b` · `0c38673`: Savaşçı kılıçları, hareket yakalama animasyonları, yeni yetenek
  seti (Hamle, Üç Yönlü Kesme, Kılıç Çevirme, Mühür Yemini), vuruş hissi, yetenek sırasında hareket kilidi.
- `3990959` Kılıca özel +0…+9 yükseltme görünümü.
- Her büyük işten önce `main` yedek dala alındı (`yedek/*-oncesi`).

## 2026-10-13 — Zırh +1…+9 efekti referans görsellere göre yeniden yazıldı · dal `ozellik/zirh-efekt-referans`
- Dosya: `index.html` (+ bu kayıt, `PROJECT_STATE.md`). Tapınak paleti, zorluk, EXP, ödül, Taş Mühür, deneme karakteri ve +0…+9 oranlarına dokunulmadı; `ARMOR_LV` değerleri aynı.
- Neden: kullanıcının verdiği iki referans görselde ilerleme baştan sona SICAK altın→turuncu; önceki gümüş→turkuaz→altın düzeni ona uymuyordu.
- Gölgelendirici (`GILD_ARM` bloğu): renk soluk altın → kehribar → alev turuncusu. +1…+3 ince metalik kenar ışığı + seyrek göz kırpan parıltılar; +4…+6 plaka yönünü izleyen ince, kırık RÜNİK çizgiler (yeni `uLatA`, kaba elmas ızgara, kalınlık `fwidth` ile; uzakta yıkama yok); +7 enerji akışı + yukarı süzülen şerit; +8/+9 alev gibi titreyen siluet, parlama darbesi, +9'da belirgin güçlü kenar ışığı (pelerin / püskül de `mk` maskesiyle parlar).
- Eski +7…+9 altın bloğu zırhta (`GILD_ARM`) yumuşatıldı: uzak düz yıkama, şerit yoğunluğu ve plaka renklendirmesi azaltıldı (silahlar etkilenmez).
- `gildSparks`: +7+ için iki kollu SARMAL enerji şeridi parçacıkları (tek `FX.spawn` havuzu, üst sınır 14/sn), +8/+9 turuncu köz, aura rengi +9'da altından alev turuncusuna; toplam köz üst sınırı 10/sn.
- Denemeler: ilk rünik ızgara (frekans 12, kalın) zırhı kamuflaj gibi doldurdu → frekans 5, ince çizgi, kırık hücreler. Parlama darbesinin plaka payı krem yıkama yaptığından 0.1 → 0.025.
- Testler: `node --check` tamam; `t_armorfx` 7/7, `t_logic` 21/21, `t_temple` 34/34, `t_reg` temiz; başsız Chromium + SwiftShader ekran görüntüleri (+0…+9). Gerçek mobil cihazda denenmedi (parlaklık, parçacık yoğunluğu, kare hızı).
- Açık: referanstaki tam gövde alev konturu ve parlayan pelerin ayrıntısı model tabanlı değil, gölgelendirici/parçacık yaklaşımıdır; arka plana göre okunabilirlik cihazda kontrol edilmeli.

## 2026-10-12 — Görsel: zırh +1…+9 efekti ve Bronz Taş Tapınağı renk paleti · dal `ozellik/gorsel-zirh-tapinak`
- Dosyalar: `index.html`, `CHANGELOG_DEV.md`, `PROJECT_STATE.md`. Zorluk, EXP, ödül, Taş Mühür ve deneme karakteri kodlarına dokunulmadı (yalnız `__tm` test kancasına semboller eklendi).
- **A. Zırh efekti** (`GILD_FRAG` içinde `#ifdef GILD_ARM`, `ARMOR_LV`/`armorLevel`, `gildSparks`): mevcut +7…+9 yaldız gölgelendiricisi korundu, `gildLevel` (silahlar) değişmedi.
  Zırh için aynı `uLv` alanına +1…+9 kademesi yazılır (0.05 … 0.15 · 0.22 … 0.36 · 0.4 / 0.7 / 1); yeni katmanlar yalnız zırh malzemesinde (`armor: true`) çalışır.
  - +1…+3: gümüş siluet (rim) ışığı. +4…+6: turkuaz kenar + eğri yüzeyde akan kontur + yukarı süzülen ince şerit.
  - +7…+9: eski altın şerit / parıltı / (+9) iplik dokuma + altın kenar ışığı + ~3.5 sn'de bir kısa parlama darbesi; aura sprite'ı darbeyle nabızlanır; kıvılcım seyreltildi (+9 parça başına 1.3/sn, üst sınır 7/sn; +7 de artık kıvılcım verir).
  - Emissive küçük ve yalnız siluet / kontur / şeritte (zırh yüzeyi yıkanmıyor). Gövde kostümü bölgeleri: göğüs → gövde/kol/bacak, ayakkabı → ayak (kask / kalkan eskisi gibi görselsiz).
  - Temizlik: efekt malzeme uniform'udur (eşya değişince `setBodyGild` yazar, birikmez); gövde yeniden kurulunca `disposeGild`; tek aura sprite'ı.
  - Modüler parça yolu (`gearMat`, negatif değer = zırh) eklendi ama mevcut oyunda zırh yuvasına bağlı modüler kıyafet yok → denenemedi.
  - Kenar için normal türevi (`fwidth(normal)`) denendi, ekran ölçeğine bağlı olduğundan her yeri beyaza boyadı → bırakıldı; siluet + kontur kullanılıyor.
- **B. Tapınak paleti** (`THEMES.bronze`, `templeAccent`, `templeSealTex`, `buildTempleFloor`): zemin/duvar nötr bazalt grisi (`floor 0x5a5652`, `wall 0x3a3733`, `wallTop 0x4e4843`), sis nötr-koyu (`0x15121a`), ortam ışığı nötr-sıcak beyaz, güneş soluk krem, oyuncu ışığı yumuşak sıcak (`0xffb878`);
  ateşler / mangallar sıcak turuncu (`torch 0xffa040`) kaldı. Mühür taşı koyu bazalt, altın-bronz kakma çizgileri korundu, parıltı haritası soluk mavi-mor ve yoğunluğu yarıya indi.
  Büyülü vurgu (sütun rün şeritleri, kuşak rün taşları, mühür parıltısı, portal): kat 1–5 turkuaz `0x44ccd8`, 6 mavi, 7–9 mavi-mor, 10 mor. Bronz parçalar biraz koyulaştı (`0x9a7438`/`0x5e4a30`, emissive azaltıldı).
  Mimari, sütunlar, dört ateş, zemin geometrisi, mühür deseni, yer uyarıları ve boss mühür noktaları değişmedi.
- Testler: `node --check` temiz; `t_armorfx.mjs` 7/7 (kademe tablosu, çıkarma/takma, 6 kez gövde yeniden kurma → tek aura, GPU kaynağı birikmiyor, sayfa hatası yok); `t_logic.mjs` 21/21; `t_temple.mjs` 34/34; `t_reg.mjs` temiz.
  Görsel doğrulama başsız Chromium (SwiftShader) ekran görüntüleriyle; gerçek mobil cihazda denenmedi (parlaklık, başarım, küçük ekranda okunurluk).
- Yedek: `yedek/gorsel-iyilestirme-oncesi` (main = `2e19020`). `main`'e ve Pages'e geçilmedi.

## 2026-10-12 — GEÇİCİ deneme karakteri (kaldırılacak)
- `index.html`: karakter seçim ekranında "Deneme: Sv 50 Savaşçı" düğmesi → yeni yuvada Sv 50 Savaşçı, +9 Nihai Zırh Seti (kask, zırh, çizme, kalkan, Efsane nadirlik), +9 Obsidyen Keski, Güç 108 / Can 58, yetenekler 5/5, 200.000 altın.
- Kaldırma: `// ===== GEÇİCİ DENEME KARAKTERİ` bloğunu sil, `testCharButton(box); // DENEME-DUGMESI` satırını sil, `__tm` kancasındaki `newTestWarrior`'ı çıkar (ya da bu işin commit'ini `git revert` et). Oyuncunun kayıtlarına dokunmaz.
- Test: `node --check` temiz; başsız Chromium'da düğme görünüyor, karakter doğru ekipmanla açılıyor (ATK 755, DEF 555, Can 2333), sayfa hatası yok.

## 2026-10-12 — Oyun sonu ilerleme ve zindan dengesi · dal `ozellik/oyun-sonu-denge`
- Dosyalar: `index.html`, `CHANGELOG_DEV.md`, `PROJECT_STATE.md`. Bağımlılık eklenmedi; V12 klasörüne dokunulmadı.
- **A. Tapınak zorluğu** (`TEMPLE_POW`, `TEMPLE_FLOORS`, `Mob`): kat seviyesi 42+2·kat → 46+2·kat (Sv 48–64). Canavar canı ×1.7…4.2,
  saldırı ×2.0…5.8, savunma ×1.15…1.55; 4. kattan itibaren saldırı (`cd`) ve yetenek (`sk`) sıklığı artar. Katlar 1–5 ve 7–9 iki
  dalga, 6 ve 10 tek dalga; 6. kat ilk büyük güç duvarı (can ×3.4, saldırı ×5.8). Patron mühür tutma süresi 2.0 → 2.4 sn
  (`SEAL_HOLD`). Alan saldırıları aynı kaldı (uyarı halkaları değişmedi). Grup avantajı: hasar sabit, can +%60/oyuncu (`COOP_HP`).
  - Simülasyon (oyun formülleriyle, `balance.mjs`): Sv 50 +9 Bronz tek başına kayıp ≈ %11/36/56/77/133 (1–5. kat), 6. katta %252, 7. katta %475+.
    Sv 55 +9 Efsane tek başına 6. katta ≈ %115; 4 kişilik Sv 55 +9 Efsane: 7–9. kat %36/57/65, 10. kat %89.
- **B. Efsanevi + Taş Mühür ödülleri** (6–10. kat, `TEMPLE_REWARDS.efs/ts/minRar`, `Temple.grant`): Efsanevi parça şansı kat başına
  0.28/0.22/0.28/0.34/1.5 koşu; 10. katta 2 zar. `rollGear(..., efs)` Zor/Kabus şartını (`minDiff`) yalnız bu kaynak için aşar; normal
  zindanlar değişmedi. Mühür zarları kata göre kademe yükseltir; ilk temizleme tek seferlik mühür verir (`TEMPLE_FIRST.ts`).
  Tekrar ödül: mevcut `claims` anahtarı (örnek kimliği + kat) ve ilk-temizleme bit maskesi; tümü `grant` içindeki tek kilitli blokta.
- **Taş Mühür sistemi:** 5 tür (saldırı, savunma, can, kritik, yetenek) × 3 kademe (Kırık / Bronz / Kadim) = 15 yığın (`ts_<tür>_<kademe>`).
  Eşya başına 1 yuva (`it.seal`, kayıtta beyaz listeli); ekipmanı yeniden yazmadan `recalc` mühür toplamını ekler. Tür başına toplam üst sınır
  (saldırı %20, savunma %25, can %30, kritik +10, yetenek %30). Takma ücretsiz; sökme altınla (1.500 / 5.000 / 15.000), mühür çantaya döner;
  3 → 1 birleştirme (Kırık→Bronz 3.000, Bronz→Kadim 12.000 altın), çanta doluysa geri alınır. Mühürlü eşya parçalanmaz / toplu satılmaz.
  `bronzparca` ve Simyacı dönüşümü değişmedi.
- **C. EXP** (`EXP_PLAN`, `expKills`, `expNeed`, `EXP_KILL_CAP`): Sv 1–50 birebir aynı. 51+ ihtiyaç = o seviyenin canavar EXP'si × gereken
  öldürme sayısı (51: 78 → 55: 195 → 60: 450 → 65: 900 → 69: 1500 → 70: 1600; ara değerler log-doğrusal). Sv 50→60 toplam maliyet 1.46 M
  (eski 0.90 M, ×1.6), 60→70 toplam 8.5 M (eski 3.97 M, ×2.1). Tek öldürme EXP'si seviye ihtiyacının %35'iyle sınırlı; tapınak kat EXP
  oranları 0.02–0.12 → ~0.005–0.04; tam tapınak turu Sv 55'te ~0.7, Sv 60'ta ~0.35 seviye.
- Testler (başsız Chromium + yerel sunucu, Playwright): `node --check` temiz; `t_logic.mjs` 21/21 (EXP, mühür, kayıt, Efsanevi zarı);
  `t_temple.mjs` 34/34 (10 kat gerçek açılış ve canavar katsayıları, dalga sayıları, ödül dağılımı 500 örnek/kat, tekrar ödül, EXP sınırı,
  çanta arayüz düğmeleri); `t_reg.mjs` (iki sınıf yeni karakter + kayıt gidiş-dönüşü, hata yok). Bu betikler depoda değil (oturum çalışma alanında).
  Masaüstündeki `run.mjs` / `tapinak.mjs` bu ortamda yoktu → çalıştırılmadı.
- Açık: gerçek cihazda grup testi YAPILMADI; mobil başarım (dalga başına en çok 8 yaratık) ve dokunmatik mühür
  düğmeleri denenmedi; denge sayıları model tahminidir, oyuncu geri bildirimiyle ince ayar gerekir. Önceden var olan: set sınıflarında
  tapınağın sıradan `gear` düşüşü Bez Zırh parçası verebilir (Efsanevi `efs` zarları bunu telafi eder).
- Yedek: `yedek/oyun-sonu-denge-oncesi`.

## 2026-10-12 — Bronz Taş Tapınağı (10 katlı grup zindanı) · `ca42025`
- Dosyalar: `index.html`; yeni `tapinak_{tas,canavar,okcu,buyucu,minib,boss,silah}.js`.
- Kararlar:
  - Dairesel çarpışma `L.circ` ile yapıldı; ızgara yalnız mini harita içindir.
  - Kararları host verir, `T` olaylarıyla dağıtır. Ödül anahtarı örnek kimliği + kat; savaşı görmeyene ödül verilmez.
  - Taş Canavarı için golem modeli kullanıldı.
  - Kat modelleri tembel yüklenir.
- Testler: `tapinak.mjs` 35/35, `tapinak_coop.mjs` 13/13 (simülasyon), `run.mjs` 36/36, `movetest.mjs` 20/20.
- Açık: denge (Sv 50 ve +9 ile tek başına çok kolay); gerçek cihazda grup testi yapılmadı.
- Yedek: `yedek/tapinak-oncesi`.

## 2026-10-12 — Token tasarruflu çalışma düzeni
- Dosyalar: `CLAUDE.md`, `PROJECT_STATE.md`, `CHANGELOG_DEV.md` oluşturuldu (önceden yoktu). Oyun koduna dokunulmadı.
- Kararlar:
  - Her görev `PROJECT_STATE.md` ile başlar; `index.html` yalnız hedefli `grep` ve aralıklarla okunur.
  - Base64 / üçüncü taraf bölgeleri atlanır.
- Testler: kod değişmediği için oyun testi çalıştırılmadı. Bölüm haritası ve semboller `grep` ile kaynaktan doğrulandı.
- Açık: tapınak dengesi, tapınak ortak oyununun cihaz testi.
