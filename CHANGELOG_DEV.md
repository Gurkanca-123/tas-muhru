# Geliştirme kaydı

Her görev sonunda kısa kayıt: tarih ve görev · değişen dosyalar · önemli kararlar · çalıştırılan testler · açık sorunlar.
Eski kayıtlar kısa tutulur; ayrıntı gerekirse git geçmişine bakılır.

## Önceki işler (özet, git geçmişinden)
- (32) Açık dünya kasma düzeltmesi (dal `ozellik/acik-dunya-performans`, yedek `yedek/acik-dunya-performans-oncesi`): örnekli listeler `WCHUNK`=30 karelerine, zemin 40 birimlik dizin karelerine bölündü (görünürlük/gölge kesmesi çalışsın); `goWild`'da `renderer.compile`; yaprak yeniden deneme beklemesi. Ölçüm (`renderer.info`): kare başı ~1,6 M → ~0,21–0,27 M üçgen, çizim çağrısı ~95 → ~165–190, görüntü aynı. `wfin` ve `wcomb` geçti; telefonda fps ölçülmedi. Açık: karakter modeli ~60k üçgen.
- (31) Fener Ovası görsel zenginleştirme + Yosunlu İn canavarları (dal `ozellik/acik-dunya`): 8 ağaç türü (meşe, huş, sonbahar akçaağacı, sakura, çam, servi, söğüt, kuru) ve biyomlar (sonbahar korusu, sakura koruluğu, huş ormanı), rüzgâr salınımı (instanced gölgelendirici), bulut gölgesi, çiçek/lavanta tarlaları, buğday tarlaları + çit + korkuluk + saman, eğrelti/mantar/kütük, sazlar/nilüfer, köprülü dere (kaynaktan göle), yel değirmeni, harabeler, Kurt Lordu ini, korucu kampı + iskele, gökyüzü kubbesi + bulut + uzak dağlar (3. şahıs), kelebek, düşen yaprak/taç yaprağı, polen; kamera–oyuncu arasındaki ağaçlar noktalı saydamlaşır. Canavarlar: ~20 kamp (kurt/yarasa Sv 1–6, köyden uzaklaştıkça artar), 3 Alfa Kurt (Sv 7), Kurt Lordu Bozkır (Sv 8, inde, 5 dk'da yeniden doğar; d1 temizleme/görev kaydı). Tepelerde y düzeltmesi: Mob, FX (addG/spawn), yer uyarıları, mermi, loot, hedef halkası, Atmo. Doğrulama: başsız tarayıcı (8 nokta erişilebilir, tüm yollar + köprü yürünebilir, kamp saldırısı, patron öldürme → d1 temizlendi + yeniden doğma, zindan/köy regresyonu); gerçek cihazda denenmedi. Bölge ~1,75 M üçgen.
- (30) Açık dünya altyapısı + 1. bölge «Fener Ovası» (dal `ozellik/acik-dunya`, yedek `yedek/acik-dunya-oncesi`): `WILD_ZONES` veri tablosu, `buildWild` (yükseklik haritası, 280×280, tepeler/göl/gölcük, yol ağı: ana yol + 5 dal + 1 döngü, orman/dik yamaç/su/sınır sırtı engelleri, tabelalar, Gözcü Tepesi/Taş Çember/Göl Kampı/Seyir Taşı, mühürlü geçit). Köy güney kapısı gerçek geçit (`kind:'wild'`), dönüş `wback`. Oyuncu/kamera/güneş `groundY` ile zemini izler. Mini haritaya dokununca büyük harita + yön işareti (bayrak, ışık sütunu, mesafe). Canavar yok. Doğrulama: başsız tarayıcı (7 nokta erişilebilir, tüm yollar çarpışmayla yürünebildi, zindan regresyonu geçti); gerçek cihazda denenmedi.
- (29) Köy sadeleştirme (dal `ozellik/koy-sadelestir`, yedek `yedek/koy-sadelestir-oncesi`): 6 oturma bankası, tüm köy/yapı fıçıları (Tüccar, Demirci, kulübe, Usta, Simyacı çevresi) ve anıtın etrafındaki 4 mangal kaldırıldı; ilgili `blockAt` çarpışmaları da silindi (karakter takılmasın). `propBarrel/propBench` fonksiyonları duruyor. Doğrulama: sözdizimi + başsız ekran görüntüsü; gerçek cihazda denenmedi.
- `1889fb6` Savaşçı sınıfı (5 gövde GLB, yeniden rig + animasyon), Sv 70 ve son oyun dengesi.
- `d9f1acd` · `f65921b` · `032b90e` · `12e578b` · `0c38673`: Savaşçı kılıçları, hareket yakalama animasyonları, yeni yetenek
  seti (Hamle, Üç Yönlü Kesme, Kılıç Çevirme, Mühür Yemini), vuruş hissi, yetenek sırasında hareket kilidi.
- `3990959` Kılıca özel +0…+9 yükseltme görünümü.
- Her büyük işten önce `main` yedek dala alındı (`yedek/*-oncesi`).

## 2026-10-15 (28) — Mühür Yemini düzenlemesi · dal `ozellik/muhur-yemini` (main'e alınmadı); (27) HUD sadeleştirme main'e alındı
- Animasyon: `skW4` klibi ölçüldü (el yüksekliği): 0–0.3 kılıç kalkar, 0.36–0.96 saplama/diz çökme, 1.02–1.62 eller havaya. Havaya kalkış oynatılmıyor: `SAVASCI_SKILL_T.w4` dur 1.82→0.92, lock 1.24→0.86, ışık sütunu (`rise`) 1.12→0.62 (saplanmış kılıçtan).
- Değerler: saldırı +%30→+%20, savunma +%20→+%15, yeni `aspdPct` +%20 (otomatik/temel saldırı hızı; seviye çarpanına girmez; `recalc` → `D.aspd`), bekleme 30→31 sn.
- Test: doğrulama betiği 3/3 (değerler, bekleme, buff etkin, D.aspd=20, atk +%19 / savunma +%15 yuvarlama). Gerçek telefonda animasyonun görünüşü: **denenmedi**.

## 2026-10-15 (27) — HUD sadeleştirme · dal `ozellik/hud-sadelestir` (main'e alınmadı)
- Sorun: üst ortada kat adı + oda kodu + görev satırı + büyük hedef çubuğu üst üste biniyor, afiş (boss adı) 44 px ile ekranın dörtte birini kaplıyordu.
- Çözüm (CSS sonuna blok): `#zone` + `#party` tek ince satırda (`#topc` sarmalayıcı; dikeyde `display:contents`), hedef çubuğu ince ve yarı saydam, çarpışmada (hedef varken) görev satırı gizli, `#toast` yatayda aşağı-orta, `#banner` küçük (en çok 22 px) ve daha yukarıda.
- Doğrulama: 900×412 yatay ve 412×900 dikey ekran görüntüleri (boss hedefli / hedefsiz). Gerçek telefon: **denenmedi**.

## 2026-10-15 (26) — Zırh ikonları (çizme baştan, kask/göğüslük ayrıntı) · dal `ozellik/efsun-set-boss` → main'e alındı (kullanıcı onayı)
- 3B ikon: çizme yandan profil ekstrüzyonuyla yeniden modellendi (kıvrık burun, topuk bloğu, taban, yan levha, burun koruması, 3 kemer + toka, kapak, taş); kaska ense koruması / tepe topuzu / göz taşları; göğüslüğe boyunluk ve etek levhaları. Süs parçaları gövde ekstrüzyonunun (bevel dahil) dışında kalacak z değerlerinde olmalı.
- Test: galeri (143 ikon) hatasız; qtest3 22/22, stest 15/15. Gerçek telefon: **denenmedi**.

## 2026-10-15 (25) — Efsun çeşitliliği, set etkileri, boss mekanikleri · dal `ozellik/efsun-set-boss` (main'e alınmadı)
- Efsun: Saldırı Hızı, Kritik Hasarı, Can Çalma, Savunma Delme, Patronlara Karşı Güç (+ stat paneli satırları).
- Set etkileri (5 adet, bkz. PROJECT_STATE): Taş Kabuk, Keskin Ritim, Efsane Öfke, Mühür Yankısı, Mühür Kalkanı; set bilgi kutusunda ✦ satırı.
- Boss: tüm normal patronlara öfke aşaması; yeni `lance` ve `pool`; yavru koruması (`dmgK 0.35`); Kurt Lordu'na `charge`, Kemik Lordu'na `bonerain`.
- Test (SwiftShader): etest 4/4, stest 15/15, btest 10/10 (yetenekler doğrudan tetiklenerek). Gerçek cihaz ve ortak oyun: **denenmedi**. Denge sayıları (yüzdeler, bekleme süreleri) ilk taslak; oynayıp ayarlanmalı.

## 2026-10-15 (24) — Yüksek kalite önceliği + son-işleme hattı · dal `ozellik/yuksek-kalite` (main'e alınmadı)
- Kullanıcı kararı: zayıf telefon / dosya boyutu kaygısı bırakıldı, görsel kalite öncelik. `CLAUDE.md` ve `PROJECT_STATE.md` güncellendi.
- `Post`: HalfFloat + MSAA sahne hedefi, 5 kademeli bloom, ACES + sRGB, kontrast/doygunluk/ton, vinyet, dither. Yeni görünüm "Yüksek kalite" (`ultra`, varsayılan; gölge 2048, piksel oranı ≥1.5); "Standart" = eski görünüm. Eski kayıtlar `ultra`ya göç eder.
- Test: qtest 40/40, qtest3 22/22, jtest 13/13 (SwiftShader); köy ve Kara Taş Tapınağı ekran görüntüleri hatasız. Gerçek telefon/GPU: **denenmedi**. SSAO henüz yok.

## 2026-10-15 (23) — Parşömenler Tüccar'da 100.000 / 150.000 + ikon kalitesi 2. geçiş · dal `ozellik/takiset-ikon` → main'e alındı (kullanıcı onayı)
- Kullanıcı düzeltmesi: ustalık parşömenleri Tüccar'da satılır (`SHOP_LIST`), fiyat Usta 100.000 / Büyük Usta 150.000; çantadan satış fiyatın %25'i (25.000 / 37.500, alım-satım açığı yok). Kabus düşüşleri (`PARCH_KABUS`) aynen kaldı.
- İkonlar: ayrı küçük WebGL renderer (256 px, MSAA, ACES ton eşleme, sRGB, fiziksel ışık) + PMREM ortam yansıması (degrade gök + parlak paneller) → PBR metal (`MeshStandardMaterial`), fasetli pırlanta taşlar (`icGem`, `MeshPhysicalMaterial` clearcoat),
  perçinler, altın süs kenarları, kavisli kılıç siperi, hilal balta ağzı, kemer/toka, zincir halkaları, şişe camı + etiket, çift kurdeleli mühürlü parşömen, kristal kümeleri. 2B son işlem: nadirlik halesi, koyu dış hat (yalnız halka;
  yarı saydam cam koyulaşmaz), Mor nadirlik / kademe 7 / kutsama ve büyük usta parşömeninde ışıltı yıldızları. Çıktı 128 px.
- Maliyet: SwiftShader'da ikon başına ~190 ms (143 ikon 28 sn; GPU'lu cihazda çok daha hızlı olması beklenir, **denenmedi**). Takılmayı azaltmak için `icon3DPrewarm`: her düzey kurulduktan sonra çanta / giyili / depo ikonları
  arka planda 40 ms arayla tek tek çizilir; ikonlar önbellekten gelir.
- Testler: `jtest` 13/13 (fiyat beklentisi güncellendi, stat karşılaştırması rastgele bonus satırından arındırıldı), `qtest3` 22/22, `qtest` 40/40. Gerçek telefonda görünüm ve süre **denenmedi**.

## 2026-10-15 (22) — Sv 55 / Sv 65 takı setleri, ustalık parşömeni ve kutsama fiyatları, 3B envanter ikonları · dal `ozellik/takiset-ikon` (yedek: `yedek/takiset-oncesi`)
- Dosya: yalnız `index.html`.
- Yeni adlı takı setleri (`GEAR_SETS.bronzm` / `ulumuhur`, `jewel: true`): Bronz Mühür Takı Seti (Sv 55, kademe 7 × 1.15, +1 kritik; 2: kritik +5, canavara +%5 · 3: saldırı / can +%12) ve Ulu Mühür Takı Seti (Sv 65, × 1.38, +2 kritik; 2: kritik +7,
  canavara +%8 · 3: saldırı / can +%17, savunma +%6). `setInfoOf` adlı takıyı kendi setinde sayar (kademe 7 Efsane setine sayılmaz), `gearStats` / `sellPrice` mul uygular. Rastgele düşmezler.
- Kaynaklar: Bronz Mühür yalnız Bronz Taş Tapınağı 6. kat (patron) ödülünde %35 (`TEMPLE_REWARDS[5].jset`); Ulu Mühür tapınak 8 / 9 / 10. kat %10 / %14 / %35 ve Kara Taş Tapınağı Kabus'ta Kırık Taş Mühür (`minimetin`) kırılınca %18 (`JSET_KABUS`).
- Ustalık parşömenleri (sonra (23) ile değişti): Tüccar'dan kaldırıldı; çantadan satış Usta 100.000 / Büyük Usta 150.000. Kara Taş Tapınağı ve Kemik Taht Kabus'ta düşer (`PARCH_KABUS`: normal %0,2 / elit %1,2+%0,4 / taş %5+%2 / patron %8+%3).
  Kutsama Kağıdı Tüccar fiyatı 2.500 → 10.000 (çantadan satış 300 aynı).
- 3B envanter ikonları (`iconSpec`, `IC_BUILD`, `icon3DRender`, `stackIcon`): her eşya türü için prosedürel three.js modeli (kılıç, balta, miğfer, zırh, çizme, kalkan, yüzük, kolye, tılsım, iksir, parşömen, cevher, kristal, kemik,
  Taş Mührü), kademe / set / nadirliğe göre renk + ışıma + ek parça (kürk, kanat, boynuz). Ana renderer ile 256 px render hedefi → 112 px tuval (sRGB çevrimi, yumuşak kenar, nadirlik halesi), anahtara göre önbellek.
  Data URL `i3=1` parametresi CSS'te pikselleştirmeyi kapatır. Renderer hazır değilse eski 2B ikon. Dükkân / Simyacı / geliştirme malzeme satırları da 3B (`stackIcon`).
- Testler: yeni `jtest` 13/13 (set adları, şartlar, statlar, set sayımı, fiyatlar, tapınak ödül tablosu, Kabus düşüş simülasyonu d6 / d7 / d5, Zor'da düşmemesi), `qtest` 40/40, `qtest3` 22/22, `qtest4` 32/32, `qtest5` 26/26.
  İkon üretimi SwiftShader'da ~33 ms/ikon (143 ikon 4,7 sn); gerçek telefonda süre ve görünüm **denenmedi** (ilk çanta açılışında kısa takılma olabilir, sonra önbellekten).
- Açık: q20 görev ödülü Usta parşömeni artık 100.000'e satılabilir; set parçalarının özel 3B modeli yok (renk/ek parça farkı).

## 2026-10-14 (21) — Görsel kalite geçişi: tüm zindan canavarları, NPC'ler, köy yapıları · dal `ozellik/koy-modeller` → main'e alındı (kullanıcı onayı; yedek `yedek/main-koy-kalite-oncesi`)
- Dosya: yalnız `index.html`. Bronz Taş Tapınağı (GLB) ve Kemik Kral (GLB) dokunulmadı; Metin taşı aynı kaldı.
- Canavarlar (`buildMobModelRaw`, 8 prosedürel tür, tüm seçkin/patron renk varyantları): kurt (yele, çene/diş, iki bölüm bacak + pati, kuyruk, seçkinde dikenli tasma), yarasa (parmak kemikli zar kanat), örümcek (diz eklemli 8 bacak, 8 göz, keliser, karın deseni),
  iskelet (göz çukuru + ışık, çene/diş, omurga, bez; zırhlıda dikenli omuzluk, bel plakası, yırtık pelerin, boynuz; okçuda sadak), ifrit (boynuz, kanat, kuyruk, pençe, kor çatlakları), lav kaplumbağası (plakalar arası lav, volkan dikenleri),
  golem (kaya kütleleri, ışıyan çekirdek + çatlaklar, boğumlu yumruk; buzda kristal, taşta yosun + rün), cadı / gölge / ruh büyücüsü (çan cüppe + yırtık etek, kuşak, pelerin, türüne göre kukuleta / buz tacı / kafatası, elde ışık küresi).
- NPC'ler (`buildNPC` + `humanoidDetail` `o.hq`): boyun, yaka, yüz (burun, kaş, kulak, ağız), dolgun sakal/bıyık, kemer tokası, kese, manşet, çizme konçu. Kişiye özel: Demirci alet kemeri, Tüccar şapka + yelek + defter,
  Bekçi göğüs plakası + armalı kalkan + pelerin + siperlik, Usta uzun sakal + topuz + şal + tespih, Simyacı kukuleta + iksirler + ışık küresi + gözlük, Depocu anahtar + defter.
- Köy: `roofGable` kademeli iki tonlu kiremit, uç tahtası, yuvarlak mahya + süs, alınlık ahşabı; `stoneBase` düzensiz taş kaide; `propWindow` eşik/lento/kepenk çıtası/çiçek; kulübeler yarım ahşap çerçeve, kemerli kapı + menteşe, sarmaşık, saksı, fıçı;
  bacalarda duman (`addSmoke`, 3 sprite); Depocu ambarı yeniden (`buildShed`: tahta duvar, raflar, kiremit sıralı çatı, anahtar tabelası).
- Performans: `mergePivotMeshes` (canavar/NPC pivotu başına birleştirme) + `cachedMobModel` (tür başına şablon, doğuşta klon) + ışımasız düz renkleri KÖŞE RENGİYLE tek malzemede birleştirme (`vcMat`); `mergeStatic` de aynı yöntemle (tüm düzeyler).
  Ölçüm (SwiftShader, ~30–40 canavarlı zindan girişi): çizim çağrısı main 106/184/229/173 → 138/118/181/174 (zindan 1/3/4/5), üçgen ~+%3–7. Köy: 149 → 87 çağrı, ~170k → 188k üçgen.
- Testler: `vtest` 23/23, `qtest` 40/40, `qtest3` 22/22, `qtest4` 32/32, `qtest5` 26/26 (ilk denemede sayfa yükleme zaman aşımı, tekrarında geçti). Gerçek telefonda FPS / görünüm **denenmedi**.
- Açık: zindan ortamları (duvar/zemin/dekor) bu geçişte değişmedi; canavar animasyonları eski basit salınım (yeni parçalar aynı pivotlarda).

## 2026-10-14 (20) — Köy: küçük özgün yapılar (Demirci, Tüccar, Usta sundurması, kulübeler) + yerleşim · dal `ozellik/koy-modeller` (köy yeniden tasarımı dalı + main birleşik; yedek: `yedek/koy-modeller-oncesi`)
- Dosya: yalnız `index.html` (köy). Önce kullanıcının iki GLB'si (Demirci / Tüccar) denendi; diğer yapılarla uyumsuz bulunduğu için KALDIRILDI (`koy_*.js`, `VillageAssets` yok). Referans görseller ve modeller esas alınıp yapılar oyunun kutu-tabanlı diliyle yeniden yazıldı.
- Yeni yapılar (`WP`, `roofGable`, `propWindow`, `propHangLantern`, `buildCottage`, `buildSmithy`, `buildMerchant`, `propDummy`, `buildPavilion`): eski evlerin ~%60'ı boyutunda (≈7×6 birim, duvar 2.5–3 yükseklik). Demirci: arduvaz çatı, taş baca, ÖNDE parlayan ocak + kırmızı gölgelik, örs, odun yığını, tabela. Tüccar: kırmızı kiremit çatı, çizgili + mavi gölgelik, tezgâh/mallar, para kesesi tabelası.
  Usta: açık eğitim sundurması (mavi-arduvaz çatı, kalkanlar, silah rafı, bayraklar, mangallar, 2 dummy). Küçük kulübeler 3 stil (kuzeybatı, kuzeydoğu, güneydoğu, Simyacı evi).
- Yerleşim: kamera güneyden baktığı için yapı NPC'nin ARKASINDA (kuzeyde), ön yüz meydana ≈31° çevrik; NPC yapı önünde. Usta batıya (eskiden güneydoğuda evin çatısı arkasında kalıyordu), Depocu doğuda, Simyacı çadırı güneybatıda. `blockRot` dönük yapı çarpışması. Meydan yuvarlak kaldı; meydandan yapı önlerine yollar (z≈24 ve z≈40) + kulübe patikaları.
- Çatı detayı (7 kiremit sırası + derz), Demirci ocağı çatı eteği kameraya kapatacağı için sundurma dışına alındı.
- Testler (Playwright + SwiftShader): `vtest` 23/23 (6 NPC BFS erişimi, paneller, tek parça yürünebilir alan), köy render 149 çağrı / ~170k üçgen. Gerçek telefonda FPS ve görünüm **denenmedi**.
- Açık: Depocu kulübesi eski boyutta (çatı büyük); Demirci iç mekânı kameradan görünmez; köyü büyütme (yeni yol ağı) yapılmadı, yalnız yollar eklendi.

## 2026-10-14 (19) — Beceri Ustalığı son dengeleme main'e alındı (kayıt 2026-10-13 (11) ile aynı iş) · `ozellik/ustalik-asama2` → main, kullanıcı onayıyla (yedek: `yedek/main-ustalik-denge-oncesi`)
- Yedek: `yedek/ustalik-denge-oncesi`. Değişen tek veri: `MASTERY_STEP` M 0.08→0.04, G 0.12→0.06 (`index.html`, 1 satır + yorum).
- Çarpanlar: Sv5 1.72 · M1 1.76 · M5 1.92 · M10 2.12 · G1 2.18 · G3 2.30 · G5 2.42 (formül `Sv5 + 0.04·min(aşama,10) + 0.06·max(0,aşama−10)`; beklenen tabloyla birebir).
- Dokunulmadı: normal Sv1–5 skalası, Taş Mührü sınırları (beceri %30, saldırı %20), başarı oranları, parşömen fiyat/tüketim, buff/bekleme/animasyon, demirci, EXP, tapınak.
- Testler: yeni `t_denge` 16/16 (16 aşamanın tamamı, gerçek savaşta `hitMob` çarpanı Sv5/M10/G5), `t_mastery` 29/29, `t_logic` 21/21, `t_temple` 34/34, `t_reg` hatasız, `node --check`.
- Kapsam: ustalığın sayısal altyapısı bu kayıtla kapandı. Sonraki ayrı iş: ustalık animasyon/ışıklandırma efektleri, G2…G5 yükseltmesi, kaynak/düşme (Tüccar denemesi duruyor).

## 2026-10-14 (18) — Bekleme kılıç açısı + ince kılıçlar · dal `ozellik/savasci-durus`
- Kullanıcı: tutuş başarılı, bilek kırılması yok; ama kılıç fazla yana bakıyor, kılıçlar fazla kalın.
- `idleReady`: kılıç hedefi kalça çerçevesinde (-0,66, 0,62, 0,42) → (-0,40, 0,66, 0,64) (daha ileri-yukarı, daha az yana); önkol hafif az içe.
- `buildGearSword`: `SWORD_W = 0,76` (genişlik) ve `SWORD_T = 0,62` (kalınlık) ile namlu inceltildi; uzunluk, tutma ve siper konumu aynı. 1,0 yapılırsa eski kalınlık.
- Testler: qtest 40/40, qtest3 22/22; görüntü 6 açı. Gerçek telefonda DENENMEDİ; diğer kılıç kademeleri (Hurda/Lonca/Magma…) tek tek bakılmadı.

## 2026-10-14 (17) — Bekleme: kılıç tutuşu Metin 2'ye yaklaştırıldı (bilek düzeltmesi) · dal `ozellik/savasci-durus`
- Kullanıcı geri bildirimi: bekleme (idleReady) kılıç aşağı tutuyor, bilek doğal görünmüyor; Metin 2 tutuşu daha doğal.
- `idleReady`: sağ kol öne alındı (dirsek ~90° bükük, önkol ileri-hafif içe), kılıç yana-yukarı-ileri açık (kalça çerçevesi ~ (-0,66, 0,62, 0,42)); bilek önkolla ~45° (kavrama açısı), kırık değil.
  Ölçüm: namlu–bacak 0,69, namlu–gövde 0,71, uç yerden 1,15 (eskiden 0,41). Walk/runReady değişmedi.
- Testler: qtest 40/40, geçişler (bekle→koş→yürü→koş→dur) doğru; görüntü 4 açıdan. Gerçek telefonda DENENMEDİ.
- Blender: kullanıcının bilgisayarında Blender MCP bağlandı, `savasci_fantazi.glb` aktarıldı; bağlantı ağır görüntü isteğinde koptu. Poz iyileştirmesi şimdilik oyun içi görüntüyle yapıldı.

## 2026-10-14 (16) — Savaşçı Combat Idle + doğal kılıçlı koşu (kullanıcının görev metni) · dal `ozellik/savasci-durus`
- Analiz: özgün `run`/`walk` klipleri iki kolu doğal sallıyor, gövde karşılıklı dönüyor; sorun yalnız bilek — kılıç aşağı-geri dönüp
  bacaktan geçiyordu (namlu–bacak ekseni en az 0,28). (15)'teki ilk sürüm kolları gövdeye kilitlediği için koşu mekanikti; idle'da kılıç yukarıdaydı.
- `svBuildClips` yeniden yazıldı (yine yükleme anında üretilen AnimationClip, Mixer ile normal oynar):
  - `idleReady` 3,2 sn: omuz genişliği, sol ayak önde, ayaklar 2 kemikli IK ile yere sabit (`svLegIK`), dizler bükük, kalça bacaktan bacağa kayar,
    gövde hafif önde, kılıç çapraz aşağı-ileri-dışa, dirsekler bükük; nefes, omuz, baş ve kılıçta küçük hareketler. Tüm salınımlar döngünün tam katı (kesintisiz).
  - `walkReady` / `runReady`: özgün klibin tüm kemikleri korunur; kılıç kolu gövde çerçevesinde dışa açılır (koşu −0,20, yürüme −0,16 rad),
    bilek salınımın ortasında hedef yöne bakan sabit yerel dönüşe alınır → kılıç önkolla ritme katılır; %35 sabit yöne çekilir ve kalça çerçevesinde sınırlanır (y ≥ 0,42, −0,40 ≤ x ≤ −0,12, z ≥ 0,2).
  - `svSolve`: kalça konumu parametresi, `ctx.wp`, `{w}` ve `{l, pre}` spec türleri.
- Ölçüm (fantazi, dünya birimi): koşu namlu–bacak en az 0,28 → 0,60, namlu en alçak 0,35 → 1,20; yürüme 0,29 → 0,48. El ileri-geri genliği özgünle aynı
  (sol −0,32…0,48, sağ −0,17…0,35). Bekleme: ayak hızı 0 (kayma yok), namlu ucu yerden 0,41. Koşu ayak kayması özgün klipteki gibi (değişmedi).
- Testler: 5 kostüm önden/yandan görüntü, geçişler (bekle→koş→yürü→koş→dur→saldırı→yetenek, köyde kınlı klipler), qtest 40/40, qtest3 22/22, qtest4 32/32, qtest5 26/26.
  Gerçek telefonda DENENMEDİ; ölçüm kemik eksenine göre (zırh kalınlığı hesaba katılmadı).

## 2026-10-14 (15) — Savaşçı silahlı duruş / yürüme / koşma animasyonları · dal `ozellik/savasci-durus` (yedek: `yedek/savasci-durus-oncesi`)
- Sorun: zindan beklemesi (`idleReady`) çömelmiş duruyordu; silah elde yürüme/koşmada kılıç yana-geriye savruluyordu.
- Çözüm (GLB dosyalarına dokunulmadı): `buildSavasciModel` içinde gövde başına bir kez `svBuildClips` çalışır; iskeletin dinlenme pozundan
  yön tabanlı klipler üretir: `idleReady` (özgün klibin yerine; 2,6 sn, Metin2 savaşçısı: geniş basış, dik gövde, kılıç sağ elde yukarı-yana, sol yumruk belde),
  `walkReady` / `runReady` (kalça + bacaklar özgün yürüme/koşudan, gövde-baş-kollar yeni; kılıç kolu sabit, sol kol sallanır).
- `PlayerEnt.animateGltf`: zindanda / düelloda (`armed`) `C.runCombat` / `C.walkCombat` kullanılır; köydeki kınlı yürüme/koşma/bekleme DEĞİŞMEDİ.
- Kapatma: `SV_READY = false` → eski klipler.
- Testler: 5 gövdeden 4'ü (bez, kurt, nihai, efsane) + fantazi bekleme/koşu görüntüleri elle incelendi; geçişler (bekle→koş→yürü→dur→saldırı→yetenek) başsız tarayıcıda doğrulandı;
  qtest 40/40, qtest3 22/22, qtest4 32/32, qtest5 26/26. Gerçek telefonda DENENMEDİ.
- Açık: saldırı/yetenek klipleri değişmedi (silah elde klipler arası geçişte kısa karışma olabilir); kılıç açısı gözle ayarlandı, beğenilmezse `svBuildClips` içindeki `blade` / kol yönleri.
## 2026-10-13 (14) — Köy meydanı yeniden tasarımı (referans görsele göre) · dal `ozellik/koy-meydani` (yedek: `yedek/koy-oncesi`)
- Dosya: `index.html` (yalnız köy: `buildVillage` + yeni yardımcılar + `THEMES.village`); oyun mantığı / kayıt / savaş değişmedi.
- Yerleşim (kuzey = ekran üstü): ortada **Merkez Anıt** (`buildMonument`: 3 kademeli platform, mavi rünlü dikilitaş, 2 yan taş, zincir, dönen rünler, 4 köşe mangal); üstte **Zindan Girişi** (`buildDungeonHall` salon + merdiven + 2 mangal, iki gözcü kulesi `buildTower`, Bekçi basamakların önünde);
  solda Demirci (ocak, eski yeri) + **Simyacı mor çadırı** (`buildTent`, kazan çadırın içinde, arduvaz çatılı ev = `HOUSE_STYLES[3]`); sağda Tüccar (yukarı kaydı), **Depocu kulübesi** (`buildShed`, sağa taşındı), Usta (aynı yer, bayrak eklendi); altta **köy çıkışı** kapısı (`buildExitGate`: sütunlar, kiriş, bayrak, mangal, basamak). Çit, ağaç, kayalar (`propRock`) ve bayraklar (`propBannerCloth`) eklendi.
- Kaldırıldı: eski çeşme, eski portal platformu ve ayrı «Portal Taşı» etkileşimi (Bekçi aynı `id:'portal'` ile zindan panelini açar; görev motoru etkilenmedi). İpucu ve q01 metni «zindan girişi / Bekçi» olarak güncellendi.
- Atmosfer: `THEMES.village` akşam tonuna çekildi (daha düşük hemi/güneş, sıcak güneş, mor-gri sis). Işık sayısı sabit; mangal alevleri tek `InstancedMesh` (`addFlameInst` / `flushFlames`), haleler tek sprite (`addGlowSprite`).
- `buildHouse` yeni `opts.noDoor` (kapıyı çağıran kurar). Kayıt alanı eklenmedi.
- Testler (Playwright + SwiftShader, tek tarayıcı): yeni köy testi 23/23 (6 NPC'ye BFS erişim, spawn/dönüş noktası yürünebilir, tek parça yürünebilir alan, NPC panelleri, zindana gidiş-dönüş, anıt/salon çarpışması, JS hatası yok); görev 40/40, çanta 22/22, HUD 32/32, pencereler 26/26; `node --check` OK.
- Maliyet (SwiftShader ölçümü): üçgen ~+4% (170k→176k), köy sahne nesnesi 249→281; gerçek telefonda FPS **denenmedi**.
- Açık: gerçek cihazda performans ve okunabilirlik; köy çıkışı yalnız görsel (dünya haritası yok); eski testlerdeki «Portal Taşı» etiketine bakan betik varsa güncellenmeli.

## 2026-10-13 (13) — Minimal fantastik arayüz yenilemesi (Aşama 1 HUD + Aşama 2 Çanta/Görev defteri) · dal `ozellik/arayuz-minimal` (yedek: `yedek/arayuz-oncesi`)
- Taban: `ozellik/gorev-sistemi` ucu `6b9e2d4` (HUD'daki Görevler düğmesi ve çanta sayfaları `main`'de yok; `main` = `10f7a92`, değişmedi).
- **Aşama 1 (HUD):** yalnız CSS, stil sayfasının SONUNDAKİ «HUD: minimal fantastik» bloğu (eski kuralları ezer, geri almak = bloğu silmek). Koyu yarı saydam panel + 1px pirinç çizgi (`#hud` kapsamı).
  Görsel boyutlar: portre 44→36, iksir / menü düğmesi 44→36, Görevler 96×30→80×26, can-mana çubuğu 170×14→140×11, minimap 104→88. Dokunma alanı görselden ayrı: `::before{inset:-4px}` ile ~44px etkin alan (yalnız `#hud .ibtn/.potbtn/.qbtn`).
  Savaş düğmeleri (saldırı, yetenek, joystick) boyutça aynı; yetenek çerçevesi inceltildi. Görev satırı genişliği yatayda ekrana göre (`100vw − 412px`), hedef kartı görev satırının altına alındı, dikeyde bölge adı alta (eski kural) korundu.
- **Aşama 2 (Pencereler):** `#panel[data-p="bag"|"quest"]` kapsamlı CSS (aynı blok sonrası); diğer paneller değişmedi. Çanta ızgarası `auto-fill` sütun (8 sütuna kadar), kısa yatay ekranda (`max-height:420px`) kompakt ekipman alanı. Nadirlik / +N ışıltı kuralları ezilmedi.
- Testler (Playwright + Chromium, tek tarayıcı): HUD 32/32 (844×390, 640×360, 568×320 yatay; 390×844, 360×640 dikey: taşma, çakışma, dokunma alanı, iksir / çanta / Görevler genişletilmiş alandan tıklama), Çanta+Görev 26/26 (Giy / Parçala / Sırala, sayfa satın alma + yeniden yükleme kalıcılığı, görev teslimi), eski görev 40/40 ve çanta sayfası 22/22; `node --check`.
- DENENMEDİ: gerçek telefon (dokunma hissi, safe-area / çentik, parlaklıkta okunabilirlik). Dokunmatik cihazda dikey ekran «Telefonu yatay çevir» uyarısı gösterir; dikey HUD yalnız dokunmatik olmayan tarayıcıda ölçüldü. 568 px genişlikte görev satırı üç satıra sarabilir.

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
