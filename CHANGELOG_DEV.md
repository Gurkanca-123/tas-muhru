# Geliştirme kaydı

Her görev sonunda kısa kayıt: tarih ve görev · değişen dosyalar · önemli kararlar · çalıştırılan testler · açık sorunlar.
Eski kayıtlar kısa tutulur; ayrıntı gerekirse git geçmişine bakılır.

## Önceki işler (özet, git geçmişinden)
- `1889fb6` Savaşçı sınıfı (5 gövde GLB, yeniden rig + animasyon), Sv 70 ve son oyun dengesi.
- `d9f1acd` · `f65921b` · `032b90e` · `12e578b` · `0c38673`: Savaşçı kılıçları, hareket yakalama animasyonları, yeni yetenek
  seti (Hamle, Üç Yönlü Kesme, Kılıç Çevirme, Mühür Yemini), vuruş hissi, yetenek sırasında hareket kilidi.
- `3990959` Kılıca özel +0…+9 yükseltme görünümü.
- Her büyük işten önce `main` yedek dala alındı (`yedek/*-oncesi`).

## 2026-10-13 (12) — Çanta sayfaları + Görevler düğmesi + Görev defteri yeniden tasarımı · dal `ozellik/gorev-sistemi`
- Çanta: 3 sayfa × 40 yuva. 2. ve 3. sayfa sırayla `INV_PAGE_COST` (100.000 altın, onaylı) ile açılır. Kayıt: `P.invPages` (1…3, `applySave` doğrular; eski kayıt = 1 sayfa).
  `P.inv` tek düz dizi olarak kaldı (uzunluk `invCap()`), yalnız `UI.invGrid` sayfa sekmeleri çizer ve gerçek dizin ofsetiyle çağırır → Depocu, Tüccar, Demirci ve ganimet kodu değişmedi. `Sırala` tüm sayfaları birlikte sıralar.
- HUD: sol üstte iksirlerin altında parşömen simgeli «Görevler» düğmesi (`#b-quest`, ❗ yeni / ✔ teslim). Üstteki görev satırı (`#qline`) durur.
- `UI.p_quest` yeniden: hikâye kutusu (konuşan rol) + hedef kartı (sayaç çubuğu) + yol haritası (sıradaki 3 görev, kilitli) + sağ sütunda ödül kartı (altın, EXP, eşya slotları).
- Düzeltme: «Usta'a git» → yönelme hâli eki (`NPC_DAT`).
- Testler: Playwright 22/22 (çanta sayfaları, satın alma, kayıt gidiş-dönüş, eski kayıt, sınırlar, Depocu/Tüccar/Demirci panelleri) + görev testleri 40/40; `node --check`. DENENMEDİ: gerçek telefon; ücret (100.000 / sayfa) dengesi.

## 2026-10-13 (11) — Ana görev zinciri + oyuncu yönlendirmesi (Fener Köyü hikâyesi) · dal `ozellik/gorev-sistemi` (yedek: `yedek/gorev-oncesi`)
- Yeni: `QUESTS` (23 görev, Sv 1→70) + `Quest` motoru (`index.html`, «Ana görev zinciri» bölümü, Ortak oyun'dan önce). Doğrusal zincir, aynı anda tek aktif görev.
  Hikâye: Kadim Mühür çatlıyor → 3 perde (Sv 1-38 Çatlayan Mühür · 38-45 Mührün Gölgesi · 45-70 Bronz Mühür). NPC'ler yalnız rolle anılır (Bekçi, Demirci, Tüccar, Depocu, Usta, Simyacı).
- Arayüz: HUD satırı `#qline` (dokununca Görev defteri), NPC üstünde ❗ (yeni görev) / ✔ (teslim), `UI.p_quest` (hikâye + hedef + ödül; NPC'de teslim),
  Menü → «Görev defteri», Bekçi listesinde hedef zindana ★. Görev ödülleri mevcut yığınlardan (usta parşömeni, Taş Mühür, Kutsama, Ruh Taşı, Bronz Mühür Parçası) — ustalık / mühür döngüsüne kaynak sağlar.
- Kayıt: `P.quest = { done: [kimlik…], cur: { id, n, ready, brief } | null }` (`applySave` doğrular, bilinmeyen kimlik süzülür). Alanı olmayan eski kayıt ilk açılışta ilerlemesi kadar görevi ÖDÜLSÜZ atlar (`Quest.migrate`).
- Olay kancaları (tek satır): `killMob`, zindan / metin boss temizleme (`markDiffClear` yanı), `Temple.grant`, `addExp`, yükseltme başarısı, `doEfsun`, `spendPoint`, `useSkill`, Usta (yetenek öğrenme), `socketSeal`, `useMasteryScroll`.
- Sınıf bağımsız: yetenekler sınıfın `CLASSES[cls].skills` sırasıyla (`sk(i)`) anılır; Büyücü / Şaman eklenince görev satırları değişmez. Yeni zindan → `QUESTS`'e `type:'clear'` satırı.
- Testler (Playwright + Chromium, tek tarayıcı): 40/40 mantık/arayüz (23 görev tutarlılığı, iki sınıf, akış, panel, kayıt gidiş-dönüş, eski kayıt göçü) + gerçek işlev kancaları (Bekçi etkileşimi, `killMob`, `socketSeal`, `useMasteryScroll`); `node --check`; sayfa hatası yok.
- DENENMEDİ: gerçek telefonda dokunma / yerleşim, ortak oyunda misafir tarafında görev ilerlemesi, Sv 70'e kadar tam oynayış ve ödül dengesi, tapınak (`floor`) görevlerinin gerçek tapınak oyununda tetiklenmesi (yalnız olay simülasyonu).

## 2026-10-13 (10) — Beceri Ustalığı Aşama 2: M1→M10 yükseltme + kademe başına hasar artışı · dal `ozellik/ustalik-asama2`
- Usta Yetenek Parşömeni artık M1→M2→…→M10 yükseltir (aynı parşömen). Şans tablosu `MASTERY_RATE` (M1–M3 %100, M4 %95, M5 %92, M6 %88, M7 %84,
  M8 %80, M9 %75, M10 %70). Başarısızlıkta parşömen yanar, kademe aynı kalır (düşmez) — «Demirci gibi» düşüş seçeneği kullanıcıya sorulmadı, güvenli varsayım.
- Güç: `skillPowerOf` = seviye çarpanı + M kademesi × 0.08 (+ G × 0.12). M10 = 2.52, G1 = 2.64 (Sv5 = 1.72). Normal seviye skalası değişmedi.
  Hasar, iyileştirme (`useSkill` `pw`) ve `skillMult` bu çarpanı kullanır. Çanta düğmesi şansı gösterir: «Hamle · M3 → M4 (%95)».
- Yapılmadı (sonraki aşama): becerilerin güç skalasını baştan dengeleme, G2…G5, ustalık görsel efektleri, kaynak/düşme, Tüccar denemesinin kaldırılması.
- Testler: `t_mastery` 29/29 (başarısızlık oranı 6000 denemeyle ölçüldü), `t_logic` 21/21, `t_temple` 34/34, `t_reg`, `node --check`. Cihazda denenmedi.

## 2026-10-13 (9) — Boss adı kısaltıldı: «Kadim Mühür» · dal `ozellik/kadim-muhur`
- Kullanıcı isteği: «Kadim mühür yeterli». Son zindan boss'u `Kadim Kırık Taş Mühür` → `Kadim Mühür` (banner `KADİM MÜHÜR`, tüm metinler). Küçük taş «Kırık Taş Mühür» kaldı.
- Kod kimlikleri ve kayıt alanları değişmedi. Testler: `node --check`, `t_logic`, `t_temple`.

## 2026-10-13 (8) — Metin taşı yeniden adlandırıldı: «Kırık Taş Mühür» · dal `ozellik/kirik-tas-muhur`
- Yalnız oyuncuya görünen metinler: küçük taş `Metin Taşı` → `Kırık Taş Mühür`; son zindan boss'u `Kadim Metin` → `Kadim Kırık Taş Mühür`
  (bannerlar, günlük görev, bildirimler, zindan/eşya açıklamaları, giriş/zafer metni). Ekler uyumlu: «…Mühür'ü», «…Mühür'den», «…Mühür'ün».
- Kod kimlikleri (`metin`, `minimetin`, `DROP.metin`, `rank`, `model`, `updateMetin`) ve kayıt alanları DEĞİŞMEDİ → eski kayıtlar etkilenmez.
- Testler: `node --check`, `t_logic` 21/21, `t_temple` 34/34, `t_reg` hatasız. Cihazda görsel doğrulama yapılmadı.

## 2026-10-13 (7) — DENEME: ustalık parşömenleri Tüccar'da + Tüccar bedava alım hatası düzeltildi · `main`
- Kullanıcı isteği (geçici): `SHOP_LIST`'e `usta_parsomen` (3.000 altın) ve `busta_parsomen` (10.000 altın) eklendi. Kaynakları belirlenince `SHOP_LIST`'ten ve `price` alanlarından kaldırılacak.
- Hata düzeltmesi (`p_shop` `buy`): çantada hiç olmayan bir yığın alınınca yeni yuvaya giren nesnenin adedi 0'a inmediği için `bought = n - it.n` 0 çıkıyor, altın düşmüyordu (ilk alım bedavaydı; tüm Tüccar eşyaları). Artık alınan adet `countStack` farkıyla hesaplanır.
- Testler: `node --check` tamam; Tüccar alım kontrolü (parşömen ilk alım 3.000 düşer, ikinci alım yığına eklenir, 10'lu iksir doğru ücret, yetersiz altında alım yok); `t_mastery` 21/21, `t_logic` 21/21, `t_temple` 34/34, `t_reg` temiz.
- Beceri ustalığı Aşama 1 ve bu deneme birlikte `main`'e alındı (kullanıcı isteği). Yedek: `yedek/beceri-ustalik-oncesi`.

## 2026-10-13 (6) — Beceri Ustalığı Aşama 1: veri yapısı + iki parşömen · dal `ozellik/beceri-ustalik` (sonra main'e alındı, bkz. 7)
- Dosya: `index.html` (+ bu kayıt, `PROJECT_STATE.md`). Yedek: `yedek/beceri-ustalik-oncesi` (= `b208b14`).
- Veri: `P.mastery = { [beceriId]: aşama }` — 0 normal, 1…10 M1…M10, 11…15 G1…G5 (`MASTERY`, `masteryOf`, `masteryLabel`). Anahtar beceri kimliği → beceri başına tek kayıt; yalnız 0'dan büyük aşamalar saklanır. Güce / bekleme süresine / maliyete etkisi YOK (sonraki aşama).
- Kayıt: `newCharacter` şablonuna `mastery: {}`; `applySave` beyaz listesi: yalnız sınıfın becerileri, 1…15 aralığı ve normal seviyesi `SKILL_MAX` olan beceriler kabul edilir; eski kayıtta alan yoksa `{}`.
- Parşömenler (`STACKS`, `kind: 'scroll'`, `MASTERY_SCROLLS`): `usta_parsomen` Usta Yetenek Parşömeni (normal Seviye 5 → M1), `busta_parsomen` Büyük Usta Yetenek Parşömeni (M10 → G1). `masteryCheck` uygun değilse nedeni döndürür ve parşömen tüketilmez; `useMasteryScroll` kontrol → 1 parşömen düş → aşamayı yaz (senkron, ikinci çağrı reddedilir). Hiçbir düşüş / ödül / dükkân tablosuna bağlı değil; satış fiyatı (500 / 2000) geçici.
- Arayüz: çantada parşömen seçilince `Kullan` → sınıfın becerileri listelenir (`UI.masteryActs`); uygun olan iki dokunuşla onaylanır, uygun olmayan nedeniyle kilitli görünür. Karakter ve Usta (hoca) panellerinde seviye metni `skillLvText`: eski "M (usta)" etiketi M1 ile karışmasın diye "Seviye 5 (tam)" oldu; ustalıkta "M1" / "G1".
- `__tm` test kancasına ustalık sembolleri eklendi.
- Testler: `node --check` tamam; yeni `t_mastery.mjs` 21/21 (yeni karakter / eski kayıt varsayılanı, Usta ve Büyük Usta uygun / uygunsuz durumlar, tüketilmeme, çift kullanım, kayıt-yükleme, bozuk veri temizliği, çanta seçim akışı, Baltacı); regresyon `t_logic` 21/21, `t_temple` 34/34, `t_reg` temiz. Masaüstündeki `run.mjs` / `movetest.mjs` bu ortamda yok → çalıştırılmadı.
- Açık: M1→M10 ve G1→G5 yükseltme akışı, güç etkisi, düşüş kaynakları; ortak oyunda başka oyuncunun ustalık aşaması gösterilmiyor (gerekmiyor).

## 2026-10-13 (5) — Alev haresi azaltıldı · `main`
- Kullanıcı: "hareler biraz fazla, ışıltı güzel". `makeFlameShell`: kenar şişmesi 0.0085 → 0.006, alev alfası 1.2 → 0.72, geniş hare 0.2 → 0.07; `gildSparks` aura sprite opaklığı üst sınırı 0.32 → 0.16. Isınmış metal / derz çizgileri (`GILD_ARM`) değişmedi.
- Testler: `node --check` tamam, `t_armorfx` geçti, yakın ekran görüntüsü kontrol edildi. Cihazda denenmedi. Yedek: `yedek/alev-hare-oncesi`.

## 2026-10-13 (4) — Demirci +7…+9 zorlaştırma ve Sv 45+ EXP 2 kat · dal `ozellik/demirci-exp-zorluk`
- Dosya: `index.html` (+ bu kayıt, `PROJECT_STATE.md`). `__tm` test kancasına `UPG, expNeed, expNeed0` eklendi. Kullanıcı isteğiyle `UPG.rate` (CLAUDE.md'deki "geliştirme oranlarına dokunma" kuralının istisnası); `UPG.bonus` (eşya gücü) değişmedi.
- **Demirci:** başarı oranı (+N → +N+1): +6→+7 %50→%42, +7→+8 %35→%25, +8→+9 %25→%12 (+1…+6 aynı). Altın: +7 ×1.5, +8 ×2.2, +9 ×3.2 (`GEL_MULT`). Malzeme: ruh taşı ve yuva cevheri 1.5 kat (yukarı yuvarlanır). Başarısızlık kuralları aynı (+7'ye kadar bir düşer, +8/+9 hedefinde +0; Kutsama korur).
  - Örnek (kademe 5 göğüs): +7 6.695 altın · 5 ruh taşı · 2 yuva cevheri; +8 12.240 · 6 · 3; +9 21.623 · 8 · 5. +6'dan +9'a Kutsama'lı beklenen deneme ~8.9 → ~14.7.
- **EXP:** `expNeed` artık Sv ≥ 45 için `expNeed0` (eski eğri) × 2 (`EXP_X2_LV`, `EXP_X2`). Görev / tapınak / ilk temizleme ödülleri ve tek-kill sınırı eski eğriyi (`expNeed0`) kullanır: ödüller mutlak değerde aynı, seviye gerçekten 2 kat yavaş. Sv 1–44 aynı. Örnek: Sv 45 30.294 → 60.588, Sv 50 38.078 → 76.156, Sv 60 377.634 → 755.268.
- Testler: `node --check` tamam; `t_logic` 21/21 (3 EXP kontrolü yeni 2 kat kurala göre güncellendi: Sv 1–44 aynı, 51–60 ve 61–69 maliyet oranları ×2), `t_temple` 34/34, `t_reg` temiz, `t_armorfx` 7/7 (zaman zaman "aura 0" ile takılır: testin 600 ms'lik bekleme aralığı yavaş başsız çizimde yetmiyor, oyun hatası değil). Yeni kontrol betiği `t_dem.mjs` oranları, maliyetleri ve EXP katlarını doğruladı.
- Açık: mevcut karakterlerin EXP çubuğu Sv 45+'da yarıya iner (EXP değeri aynı, gereken 2 kat); denge cihazda oynanarak ayarlanmalı.

## 2026-10-13 (3) — Zırh +7…+9 alev kabuğu ve ısınmış metal · dal `ozellik/zirh-alev-kabugu` (main'e alınmadı)
- Dosya: `index.html` (+ bu kayıt). Neden: kullanıcı +7/+8/+9'da referanstaki "yanıyormuş gibi" hare ve alev dillerini istedi (sarmal şerit gerekmiyor, kare parçacık yok).
- `makeFlameShell`: gövde kemikli mesh'inin aynı geometri / iskeletle `SkinnedMesh` kopyası (toplamalı, depthWrite kapalı). Köşeler normal + yukarı yönde 3B gürültüyle uzar (dalgalanan alev dilleri), yalnız silüete yakın pikseller parlar; renk altın → turuncu (uçlarda ve +9'da daha turuncu). Parçacık yok.
- Seviye gövde ışıltısıyla aynı `uLv` dizisinden gelir; `gildShellVis` en yüksek bölge < +7 iken kabuğu gizler (maliyet sıfır). `H.shell` iki model kurulumunda (Baltacı, Savaşçı) üretilir; malzeme `disposeGild` ile temizlenir.
- `GILD_ARM`: ısınmış metal terimi (+7…+9): plakanın kendi dokusu altın yanar, detay korunur.
- Testler: `node --check` tamam; `t_armorfx` 7/7, `t_logic` 21/21, `t_temple` 34/34, `t_reg` temiz; yakın ve uzak başsız ekran görüntüleri. Gerçek cihazda denenmedi.
- Açık: kask / kalkan / ayrı modüler parçalar alev kabuğuna dahil değil; açık zeminde toplamalı alev düşük kontrastlı, koyu zeminde daha iyi okunur.

## 2026-10-13 (2) — Zırh parlaması düzeltmesi: dokudan gelen derz çizgileri, kare parçacıklar kaldırıldı · dal `ozellik/zirh-parlama-duzeltme`
- Dosya: `index.html` (+ bu kayıt, `PROJECT_STATE.md`). Neden: cihazda zırh düz altın sis gibi yıkanıyordu, etrafta beyaz/sarı kare parçacıklar çıkıyordu, referansa benzemiyordu.
- Gölgelendirici (`GILD_ARM`): matematiksel elmas ızgara (rünik çizgiler) bırakıldı; yerine DOKU tabanlı derz çizgileri: albedo'nun bulanık (`texture2D(map, vMapUv, 2.5)`) haline göre daha koyu pikseller (plaka derzleri / oyuklar) parlar → çizgiler plaka desenini birebir izler, ekran ölçeğinden bağımsızdır. Eşik kademeyle düşer: +4 yalnız en derin derzler, +9 zırh boyunca yoğun çizgiler; aralarda koyu zırh görünür.
- Siluet kenar ışığı inceltildi (`pow 3`), +8/+9'da alev gibi titreyen kenar + ayaktan başa yükselen alev dilimleri. Eski +7…+9 yaldız bloğu (iplik dokuma / yıkama) zırhta tamamen kapatıldı (`if (false)`); silahlarda aynen çalışır.
- `gildSparks`: tüm kare parçacıklar (sarmal şerit, köz, kıvılcım) kaldırıldı; yalnız aura sprite'ı kaldı, opaklığı ~3 kat azaltıldı (gövdeyi yıkamasın).
- Dokunulmadı: kılıcın kendi köz / alev parçacıkları (`upgEmbers`, obsidyen kılıçta mor-beyaz kareler görünür) — istenirse ayrıca kaldırılır.
- Testler: `node --check` tamam; `t_armorfx` 7/7, `t_logic` 21/21, `t_temple` 34/34, `t_reg` temiz; yakın (3. şahıs) ve uzak başsız ekran görüntüleri. Gerçek cihazda denenmedi.

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
