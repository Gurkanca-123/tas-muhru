# Taş Mührü — proje durumu (kısa teknik hafıza)

Son güncelleme: 2026-10-18 · `main`: beceri ustalığı görsel kademesi (`SkillVis`, `SKILL_FX`) dahil; görev zinciri + çanta/arayüz yenilemesi + Savaşçı silahlı bekleme/koşu/yürüme animasyonları ve ince kılıçlar (`SWORD_W/SWORD_T`) dahil. köy yeniden tasarımı + küçük köy yapıları + canavar/NPC/köy görsel kalite geçişi (`ozellik/koy-modeller` → main, kullanıcı onayıyla; yedek `yedek/main-koy-kalite-oncesi`). Satır numaraları bu sürüme göredir ve kayar;
her zaman `grep -n` ile doğrula.

## Dosyalar
- `index.html` (~5.8 MB, 17.4k satır): tüm oyun. 1–503 CSS + DOM · 504–511 betik etiketleri + `window.TM_NET` (Supabase) ·
  sonrası tek büyük `<script>`. ~2700–7700 gömülü SkeletonUtils + GLTFLoader (üçüncü taraf, dokunma) · ~7777–7800
  `OUTFIT_DATA` + `GEAR_GLTF` (base64 kılıç/balta/kıyafet GLB'leri).
- İhtiyaçta yüklenen (Büyücü): `buyucu_{baslangic,zambak,zumrut,mavi,ametist}.js`, `buyucu_asalar.js`.
- Açılışta yüklenen: `three.min.js` (r158), `baltaci_{ciplak,bez,kurt,bronzz}.js`, `boneking.js`, `boneking_sword.js`.
- İhtiyaçta yüklenen (`window.TM_ASSETS[ad]` = base64 GLB): `savasci_{fantazi,bez,kurt,nihai,efsane}.js` (`SAVASCI_FILES`),
  `tapinak_{tas,canavar,okcu,buyucu,minib,boss,silah}.js` (`TEMPLE_FILES`, kata göre).
- `manifest.webmanifest`, `icon-*.png`, `README.md`. Araç / test betikleri depoda yok (bkz. `CLAUDE.md`).

## Bölüm haritası (index.html)
| Satır~ | Bölüm / önemli semboller |
|---|---|
| 516 | yardımcılar (`rand`, `pick`, `clamp`, `dist`, `el`, `esc`, `fmtFull`, `mulberry32`), 562 `SFX` |
| 629–1005 | oyun verisi: `MAX_LV`=70, `EXP_PLAN`/`expKills`/`expNeed` (639–651), `CLASSES` (baltaci, warrior), `SKILLS`, `DUNGEONS` (691), `MOBS` (709), `RANK`, `mobBase`, `SLOTS`, `GEAR_SETS`, `STACKS` (880; Taş Mühür yığınları `ts_*` ve `SEAL_GRADES`/`SEAL_STATS` ~934), `UPG`/`upgradeCost`, `DROP` (963), `DIFFS` (984), `DAILY_KINDS`, `THEMES` |
| 2091–2660 | eşya sistemi (`makeGear`, `rollGear`, `itemName`, `sellPrice`), kayıt (`newCharacter` 2318, `saveGame` 2387, `applySave` 2459), `recalc` 2530, envanter (`addItem`, `countStack`, `removeStack`), `addExp` 2661; Taş Mühür: `sealParse`/`sealBonusOf`/`socketSeal`(~2680)/`unsocketSeal`/`mergeSeal` |
| 7804 | `Cloud` (yalnız claude.ai Artifact içinde; GitHub Pages'te kapalı → kayıt yalnız localStorage) |
| 7930–8020 | karakter GLB yükleyicileri: `BALTACI_BODIES`, `SAVASCI_FILES`/`savasciLoad`, `BONEKING` |
| 8039 | zorluk (`diffUnlocked`, `markDiffClear`), `Daily` |
| 8123 / 8333 / 8593 | `Net` (Supabase Realtime, oda kodu) · `Duel` · `RemotePlayer` · `Coop` (ortak zindan, 8609) |
| 8992–10306 | low-poly modeller, `buildSavasciModel` (9618), Baltacı modeli (`BALTACI_SKILL_T`, `SKILL_LOCK`), `SAVASCI_SKILL_T`, `buildMobModel` (~10080) |
| 10307–11415 | görsel katman: `LightPool` (3 sabit ışık), dokular, köy parçaları, kıyafet sistemi, +7…+9 ışıltı, `buildBoneKing` |
| 11416–12690 | sahne/köy/zindan üretimi: ızgara (`tileAt`, `walkable` 11507, `canStand`, `moveEntity`, `bfsField`), `newLevel`, `makePortal`, `buildDungeon`/`buildDungeonInner` (12074) |
| 12690 | `FX` (parçacık, halka, `seal`, `flash`, kılıç izi), `telegraph` |
| 13214 | `class Mob` (13223): durum makinesi, `doAttack`, `trySkill`, `animate`, `updateDeath`; `spawnMob` |
| 13773–14510 | **Bronz Taş Tapınağı** (aşağıda) |
| 14511 / 14563 | `Proj` (mermiler) · yerdeki loot |
| 14637 | `class PlayerEnt` (oyuncu, animasyon karışımı) |
| 15029 | `Combat`: `calc`, `hitMob`, `killMob`, `rollLoot`, `useSkill`, `damagePlayer`, `basicAttack` |
| 15661 / 15732 | girdi · `UI` (paneller `p_<ad>`; `open`, `close`, `render`, `btn`, `footCard`) |
| 16959 | ana döngü: `goVillage` (~16996), `goDungeon` (~17010), `update` (~17034), `frame`; 17375 `window.__tm` test kancası |

## Sistemler
- **Büyücü (`mage`, dal `ozellik/buyucu`):** GLB gövde `buyucu_<ad>.js` (`MAGE_FILES`, `mageLoad`, `mageModelKey`, `buildMageModel`; boş → baslangic, Bez → zambak, Kurt/Nihai → zumrut, Bronz Taş → mavi, Efsanevi → ametist), asalar tek betik `buyucu_asalar.js` (`mageStaffLoad` → `GEAR_GLTF['buyucu/asa_<ad>.glb']`, `OUTFIT_DATA` `buyucu_<ad>_asa`, `gripY:0, full:true`). Asa tutuşu `mageMounts` (idleReady ilk karesinden). Beceriler m1–m4, zamanlamalar `MAGE_SKILL_T`; göğüs adları `CLS_GEAR_NAMES.mage`. Gövdeler 1 birim, `MAGE_SCALE` 2.12; klipler: idleA, idleReady, idleLook, walk, run (Savaşçı hareket yakalamasından aktarım), walkReady/runReady (aynısı + sağ kol asayı tutar; zindan/açık dünya), atkA/B/C, skM1–4, hit, death (hit/death kodda kullanılmıyor). Asa kavrama yüksekliği `OUTFIT_DATA` `gripAt`.
- **Karakter:** sınıflar `baltaci` (Baltacı) ve `warrior` (Savaşçı); ikisi de GLB gövde + AnimationMixer, zırh setine göre gövde
  değişir. Yetenek animasyonu kilidi `SKILL_LOCK` / `SAVASCI_SKILL_T`. Statlar `recalc()` → `D`.
  Savaşçı silahlı klipleri (`idleReady`, `walkReady`, `runReady`) GLB'de değil, yükleme anında `svBuildClips` (buildSavasciModel'in üstü) ile üretilir:
  idle = yön/IK tabanlı poz; walk/runReady = özgün klip + kılıç kolu dışa açılır + sabit bilek ve sınırlı kılıç yönü. `SV_READY=false` eskiye döner.
  `animateGltf` zindan/düelloda `C.runCombat/walkCombat` seçer. Ölçüm araçları depoda değil (namlu–bacak mesafesi, ayak hızı).
- **Beceri ustalığı (Aşama 1–2 + son dengeleme; sayısal altyapı KAPALI — main'de):** DENEME: iki parşömen Tüccar'da geçici satılık (`SHOP_LIST`, `price`) — kaynakları belirlenince kaldır. `P.mastery[beceriId]` 0 normal · 1…10 M1…M10 · 11…15 G1…G5 (`MASTERY`, `masteryOf`, `masteryLabel`, `skillLvText`). Geçişler yalnız parşömenle: `usta_parsomen` (Sv `SKILL_MAX` → M1 → … → M10; her kademe `MASTERY_RATE` şansıyla, başarısızlıkta parşömen yanar, kademe düşmez), `busta_parsomen` (M10 → G1, kesin; G2…G5 yok) — `MASTERY_SCROLLS`, `masteryCheck`, `masteryNext`, `useMasteryScroll`, çanta `UI.masteryActs`. Güç: `skillPowerOf(id)` = `skillPower(Sv)` + `masteryBonus` (M +0.04, G +0.06 / kademe; `MASTERY_STEP`; Sv5 1.72 · M1 1.76 · M5 1.92 · M10 2.12 · G1 2.18 · G3 2.30 · G5 2.42) → `useSkill` `pw` ve `skillMult`. Normal Sv1–5 skalası (1.0…1.72) DEĞİŞMEDİ; becerilerin güç skalasını baştan dengeleme ve G2…G5 yükseltmesi sonraki aşama. `applySave` doğrular. Görsel kademe: `SKILL_VIS` + `SkillVis` (N / M altın / G mor-beyaz; `pal` → useSkill'deki `vc(renk)` tüm efektleri boyar, `cast` useSkill sonunda, `hit` vuruş noktalarında, gövde kabuğu `H.sAura` (`makeSkillShell`), bloom `Post.boost`, kılıç izi `pl._sv` → `FX.bladeOn`) ; beceriye özel kimlik `SKILL_FX` (renkler, `ult` rün dairesi + `castBolts`, `boltHit`, `tornado`, `magma`) — yeni beceride renkleri `vc(...)` ile yaz ve darbe noktasına `SkillVis.hit(id, x, z, r, ağır)` ekle.
- **Ana görev zinciri (dal `ozellik/gorev-sistemi`):** `QUESTS` tablosu (sıra = zincir sırası; alanlar dosyadaki bölüm başlığında) + `Quest` motoru
  (`ensure` aktif görevi başlatır, `ev(tür, veri)` olayları işler, `atNpc` / `turnIn` / `complete`, `migrate` eski kayıt, `hud` HUD satırı + NPC işaretleri).
  Kayıt: `P.quest = { done, cur: { id, n, ready, brief } }`. Arayüz: `#qline`, `UI.p_quest`, Menü düğmesi, Bekçi listesinde `Quest.star`. Kancalar tek satırlık `Quest.ev(...)`.
  **Yeni zindan** eklenince: `QUESTS`'e `{type:'clear', d:'<id>'}` satırı (sıra + `lv` ile). **Yeni sınıf** (Büyücü / Şaman): `CLASSES[cls].skills` sırası yeterli (metinlerde `sk(i)`);
  sınıfa özel görev gerekirse `cls:['kimlik']` alanı (`Quest.ok`). Günlük görevler (`Daily`) ayrı sistemdir. NPC adları yalnız rol (`NPC_ROLE`).
- **Arayüz teması:** stil sayfası sonunda iki üzerine-yazan blok: «HUD: minimal fantastik» (`#hud` değişkenleri `--hud-bg/--hud-line`, küçük görseller + `::before` dokunma alanı) ve «Pencereler: minimal fantastik» (`#panel[data-p=bag|quest]`; yeni panel eklemek için `:is([...])` listesine ekle). Geri almak = ilgili bloğu silmek. Savaş düğmeleri boyutça değişmedi.
- **Takı setleri / ikonlar (main, `ozellik/takiset-ikon`'dan; yedek `yedek/takiset-oncesi`):** adlı takı setleri `GEAR_SETS[*].jewel` (bronzm Sv 55, ulumuhur Sv 65; kaynaklar `TEMPLE_REWARDS[*].jset`, `JSET_KABUS`); ustalık parşömenleri Tüccar'da 100.000 / 150.000 (çantadan %25) + `PARCH_KABUS` (Kara Taş + Kemik Taht Kabus). Envanter ikonları `itemIcon` → `icon3DRender(iconSpec(it))` (ayrı küçük WebGL renderer + PMREM, 2B dış hat/hale/ışıltı, önbellekli; `icon3DPrewarm` setLevel'de arka planda; yedek 2B `spriteIcon`); yığın listeleri `stackIcon(id)`.
- **Model kalitesi / performans (dal `ozellik/koy-modeller`):** prosedürel canavarlar `buildMobModelRaw` (switch tür başına) → `buildMobModel` önbellekli şablon (`cachedMobModel`, M referansları yol ile klona taşınır; tapınak/boneking/metin hariç). `mergePivotMeshes` ve `mergeStatic` ışımasız düz renkleri köşe rengiyle `vcMat` tek malzemesinde birleştirir — sonradan `mat()` rengini değiştirmek birleşmiş parçaya YANSIMAZ. Ayrıntı yardımcıları: `limb`, `spike`, `membrane`, `shadeC/liftC`, `humanoidDetail` (`o.hq`), `sbox`, `stoneBase`, `propIvy`, `addSmoke`.
- **Köy yapıları (dal `ozellik/koy-modeller`):** `buildSmithy` / `buildMerchant` / `buildPavilion` / `buildCottage` (+ `roofGable`, `WP` yerel→dünya, `blockRot` dönük çarpışma). Kural: yapı NPC'nin güneyinde DEĞİL kuzeyinde/yanında olsun (kamera güneyden bakar, çatı NPC'yi kapatmasın). GLB denendi ve uyumsuz bulunup kaldırıldı.
- **Köy meydanı (aynı dal):** `buildVillage` (31×31 ızgara, `T`=2, merkez `C`=31; kuzey = ekran üstü). Yerleşim: Merkez Anıt (C,C) · Bekçi (C,12.6) zindan girişi salonunun merdiveninde · Demirci (19.8,28.2) · Tüccar (41.6,24.5) · Depocu (47,33.2, kulübe x 49–57) · Usta (47,40.4) · Simyacı (25.2,44.2, çadır 20.2,47.5) · çıkış kapısı z≈57.6.
  Parçalar `buildMonument/buildDungeonHall/buildExitGate/buildTower/buildShed/buildTent`, süsler `propBannerCloth/propBrazier/propRock/propChest`. Alevler `addFlameInst` (köy sonunda `flushFlames`), haleler `addGlowSprite`. Çarpışma `block(i0,j0,i1,j1)` / `blockAt` ile (yeni bina eklerken ızgarayı kapat; NPC'ye `r`≈3.2 içinde yürünebilir hücre kalmalı). Ayrı «Portal Taşı» yok: Bekçi `id:'portal'`. Atmosfer `THEMES.village` (akşam). Köy çıkışı yalnız görsel.
- **Çanta sayfaları:** `P.invPages` (1…3), `INV_SIZE` = sayfa boyutu (40), `INV_PAGES_MAX`, `INV_PAGE_COST` (100.000), `invCap()`, `buyInvPage()`. `P.inv` düz dizi; sayfa sekmeleri yalnız `UI.invGrid`'te (dizin = gerçek). Yeni sayfa ücretini / sayısını bu sabitlerden değiştir.
- **Savaş:** `Combat.calc` (atk, def, kritik) → `hitMob` → `killMob` (EXP seviye farkıyla ölçeklenir, `rollLoot`). Canavar
  gücü `mobBase(Sv) × RANK × MOBS çarpanı × L.mobPow × DIFFS`. Ortak oyunda ek oyuncu başına can +%60 (`COOP_HP`).
- **Eşya / envanter:** yuvalar `SLOTS`; set sınıfları `GEAR_SETS` (Bez, Kurt Dişi, Nihai, Bronz Taş, Efsanevi…); yığınlar `STACKS`;
  **Taş Mühür:** eşya başına 1 yuva (`it.seal`), 5 tür × 3 kademe, tür üst sınırı; `recalc` ekler, UI `UI.sealActs` (çanta);
  geliştirme `UPG` + `upgradeCost` (+7…+9 için yuva özü `RAREMAT`); Simyacı (`p_alchemist`).
- **Seviye / ödül:** `expNeed` = `expNeed0` × 2 (Sv ≥ 45, `EXP_X2_LV`; ödüller `expNeed0` kullanır); `expNeed0`: Sv ≤50 eski formül; 51+ `EXP_PLAN` (canavar EXP'si × gereken öldürme, merkezi tablo), tek kill EXP'si `EXP_KILL_CAP` (%35) ile sınırlı, günlük görevler `Daily`, zindan ilk temizleme ödülü `killMob` içinde.
- **Zindanlar:** `DUNGEONS` d1–d7 ızgara tabanlı (`buildDungeonInner`, oda + koridor, tohumlu düzen); d6 son katı Kadim Mühür (eski ad: Kadim Metin; kod kimlikleri `metin`/`minimetin` aynı kaldı; küçük taş = «Kırık Taş Mühür»)
  arenası; d7 Kemik Taht (Kemik Kral, kod-animasyonlu GLB). Zorluk Normal / Zor / Kabus (`DIFFS`).
- **d8 Bronz Taş Tapınağı (dIdx 7):**
  - Veri: `TEMPLE_FLOORS` (10 kat ve dalgalar), `TEMPLE_POW` (can/saldırı/savunma/`cd`/`sk`), `templeFloorLv` (46 + 2·kat), `TEMPLE_REWARDS` / `TEMPLE_FIRST`
    (merkezi ödül tablosu; 6–10. katta `efs` Efsanevi, `ts` Taş Mühür, `minRar`).
  - Kat kurulumu: `buildTempleFloor` kurar. Çarpışma gerçek dairedir (`L.circ`, `templeWalk`); ızgara yalnız mini harita içindir.
  - Akış: `Temple` nesnesi; dalga / temizleme / ödül / panel `p_tapinak`.
  - Patron: `bossPick`, `bossPhase` / `applyPhase`, mühür noktaları `sealsOn` / `sealTick`, `templeShock` / `telegraphRing`.
  - Düşmanlar: `MOBS` içindeki `model:'tapinak'` olanlar; `buildTempleMob`, `animateTempleMob`, `tmPlay`, `tmDie`.
    Vuruş anı klipteki `ev.hit` ile hizalanır (`TM_ALIGN`).
  - Kayıt: `P.temple = {best, bestClear, first, runs, seals, claims}`.
- **Ortak oyun:** `Net` (Supabase Realtime kanalı `tm-<KOD>`, durum yayını), `Coop` (aynı `levelKey` 'd<dIdx>-<kat>' + tohum
  → aynı örnek). Host canavarları yönetir, misafir kukla tutar. Olaylar: `n` doğum, `k` ölüm, `a` saldırı, `t` yer uyarısı,
  `v` yaylım, `c` eylem, `x` mesaj, `d` hasar, `T` tapınak (`w` / `c` / `ph` / `so` / `sb`), `tr` halka şok.
  `fullState` / `applyFull` ile yeniden eşitlenir; host düşerse `promote` devralır.
- **Zırh güçlendirme görseli:** gövde kostümünde tek skinned mesh + `gildMaterial` (`GILD_FRAG`); kademe `armorLevel(it)` → `uLv[bölge]`
  (`setBodyGild`), silah `gildLevel` ayrı. Yeni katmanlar `#ifdef GILD_ARM`; aura/kıvılcım `gildSparks`. Tapınak renkleri `THEMES.bronze` + `templeAccent` + `buildTempleFloor`.
- **Model / animasyon:** GLB'ler base64 betiklerden `GLTFLoader.parse`, `SkeletonUtils.clone`; klipler GLB'ye gömülü (araçlarla
  üretildi). Kemik Kral klipsiz, kodla poz (`animateBoneKing`). Tapınak düşmanları: idle / walk / run / death + atk / slam /
  spin / roar / plant / cast / seal / shoot; sahne extras `enemy.{handMount, handMountL, shieldMount, ev}`.

## Kalite politikası (kullanıcı kararı 2026-10-15)
- Öncelik yüksek görsel kalite; zayıf telefon ve dosya boyutu artık kısıt değil. Varsayılan görünüm `gfx:'ultra'` ("Yüksek kalite"); eski kayıtlardaki `lowpoly` bir kez `ultra`ya göç eder (`settings.gfxv`).
- `Post` (index.html, "Son-işleme" bölümü): sahne HalfFloat + 4x MSAA hedefe çizilir → 5 kademeli bloom → tek geçişte ACES + sRGB + kontrast/doygunluk/ton + vinyet + dither. Tema bazlı ayar: `THEMES[x].grade = {bloom,thr,sat,con,tint,vig}` (isteğe bağlı). `gfx:'ultra'` dışındaki modlar doğrudan `renderer.render` kullanır.
- Ultra: gölge haritası 2048, piksel oranı en az 1.5 (en çok 2). `renderer.info.render` artık yalnız son geçişi gösterir (son-işlemde calls=1); çizim sayısı ölçümü için `Post.on=false` yap.
- Sıradaki kalite adımları: PBR/ortam yansıması (sahne materyalleri), SSAO/derinlik, dokulu yüksek ayrıntılı modeller, zindan ortamı.

## Efsun / set etkileri / boss mekanikleri (dal `ozellik/efsun-set-boss`)
- `BONUS_POOL` yeni satırlar: `aspd` Saldırı Hızı (`D.aspd`, üst sınır %40; `basicAttack` bekleme süresini böler), `cdmg` Kritik Hasarı (`Combat.critMul()` = 1.8 + cdmg/100), `steal` Can Çalma (hitMob, dot hariç), `pierce` Savunma Delme (calc'ta hedef savunmasını düşürür), `boss` Patronlara Karşı Güç (`D.bossP`). Efsun (`rollBonus`) hepsini zarlar; eski eşyalar etkilenmez. Yeni satır eklerken `gearStats`/`recalc` anahtar listelerine de ekle.
- Set etkileri: `SET_FX` (ad+metin) + `SETFX` (çalışma durumu; `recalc` `activeSets().fx` ile `SETFX.on`'u doldurur). Set `bonus[n].fx = '<id>'` ile bağlanır (toplama dışı). Etkiler: tasKabuk (bronzz 4), keskinRitim (nihai 4), efsaneOfke (efsane 4), muhurYanki (bronzm 3), muhurKalkan (ulumuhur 3). Kancalar: `damagePlayer`, `hitMob`, `killMob`, `basicAttack`, `sealEcho`. Süre/bekleme `G.time` ile.
- **Efsun Kağıdı / 4 satır (dal `ozellik/efsun-kagidi`):** `EFSUN_MAX`=4 satır; `baseLines(set, rarity)` (adlı takı setlerinde `GEAR_SETS[*].lines`=4, yoksa `RARITY.lines`). `STACKS.efsun_kagit` (Tüccar 100.000): Simyacı → Efsun'da `UI.doEfsunPaper` → `useEfsunPaper` → `addBonusLine` yeni satır ekler (eskiler kalır). `doEfsun` (yeniden zarlama) mevcut satır sayısını korur. Kaynaklar: `TEMPLE_REWARDS[5..9].efk`, `EFSUN_DROP` (Kemik Taht d7). Yeni satır türü eklenirse `BONUS_POOL` yeterli.
- Boss (d1–d6 normal patronlar): hepsine `enrage:true` (can %50). Yeni yetenekler `trySkill`'te: `lance` (hat atılımı, tek vuruş), `pool` (5–6 vuruşluk kalıcı alanlar, `later` ile tekrarlayan telegraph; renk `t.pool`, ad `t.poolName`). Yavru koruması: `summon` sonrası yavrular yaşadıkça `dmgK = 0.35`, ölünce dağılır (`minions`). Tapınak patronları (`t.phases`) bunun dışında. Ortak oyunda yer uyarıları `Coop.ev('t')` ile gider; banner'lar yalnız host'ta görünür.

## Açık dünya (dal `ozellik/acik-dunya`)
- Veri: `WILD_ZONES[]` (`paths` ana yol + dallar, `creek` dere, `hills`, `lakes`, `pads`, `biomes`, `fields`, `windmill/ruins/den`, `start/back/gate`; canavar: `dId/dIdx/mobs/elite/boss/bossLv/mobLv/junk`). Yeni bölge = yeni kayıt + `THEMES` girdisi; `buildWild(zi)` kurar, `goWild(zi)` geçer (kamp canavarlarını doğurur). Bölge `type:'dungeon'`, `L.wild` işaretli; `L.dg.id = dId` (Fener Ovası → 'd1': patron öldürünce `P.cleared.d1`, görev `clear d1`, ödül kademesi `dIdx`). Patronda çıkış portalı açılmaz, `respawnTime` ile döner. `Coop.levelKey` = `'w'+idx`; ortak oyun senkronu yok.
- Zemin: `L.hg` (+ `groundY`). Zemini izleyenler: oyuncu, kamera (`G.camGY`), güneş, `Mob.animate/updateDeath`, `FX.spawn` (zemine göre; dünya koordinatı için `FX.spawnW`), `FX.addG` (yer efektleri zeminde taşıyıcı grupla), `telegraph/telegraphRing`, `Proj`, `updateDrops`, hedef halkası, `Atmo`. Düz seviyelerde `groundY`=0 → davranış değişmez.
- Görsel: instanced listeler `WDEF` (+ `wildMat`/`wildPatch`: rüzgâr `[genlik,y0,y1]`, bulut gölgesi `cloudTex`, su dalgası, kamera–oyuncu arası ağaç saydamlaşması `WILD_PL/WILD_CAM`). Ağaç türleri `buildWild` içindeki `oak/birch/maple/sakura/pine/cypress/willow/deadTree`, seçim `species()` (biyom, yükseklik, su yakınlığı). `WPAL` renkleri. Gökyüzü kubbesi + bulut sprite'ları + uzak dağlar; açık dünyada kamera `far` = `L.camFar` (700; `setLevel` ayarlar).
- Engeller ızgaradan (`L.grid`, T=2): sınır sırtı, göl/dere suyu, dik yamaç (>0.62), yoğun orman, ağaç/kaya/yapı (`blockDisc/blockCell`); yollar, köprüler ve ilgi noktaları açıklık. `wildReach(L)` → `{poi, spawns}` erişim testi.
- Kamplar: yoldan 7–24 birim uzak açıklıklar, seviye köyden yürüme (BFS) uzaklığıyla `mobLv` aralığında; orman/su yakını kamplarda yarasa. En uzak 3 kampta elit. `L.camps`, `L.bossSpawn`.
- Geçitler: `wback` köye, `wnext` sonraki bölge (`WILD_ZONES[idx+1]` yoksa mühürlü). Köy çıkışı `kind:'wild'`, dönüş `spawnGate`.
- Büyük harita: `UI.openMap/closeMap/drawBigMap/mapTap`, `#bigmap`; mini haritaya dokun (veya M). Yön işareti `L.wp` + `L.beacon`. Hücre renkleri `L.cellCol`, tam harita `L.mapAll`, yerler `L.poi` (`gate/deco/boss`).
- Üçgen: bölge toplam ~1,75 M ama **görünürlük kesmesi için karelere bölünmüş**: örnekli listeler `WCHUNK` (30 birim) karelerinde ayrı `InstancedMesh`, zemin 40 birimlik karelerde ayrı `Mesh` (ortak köşe tamponu). Karede çizilen ~0,2–0,27 M (ölçüm: `renderer.info`). Karakter modeli (~60k üçgen) artık en büyük tek kalem. Yeni örnekli liste/büyük ağ eklerken tek parça yapma. `goWild` geçişte `renderer.compile` ile shader'ları önceden derler.

## Bilinen sorunlar / kısıtlar
- **Tapınak dengesi:** 2026-10-12'de yeniden dengelendi (simülasyon tabanlı; CHANGELOG_DEV.md). Gerçek oyuncu geri bildirimiyle ince ayar
  gerekir; kaldıraçlar `TEMPLE_POW`, `TEMPLE_FLOORS` dalgaları, `MOBS` çarpanları. Mühür / Efsanevi şansları `TEMPLE_REWARDS`.
- Set sınıflarında tapınağın sıradan `gear` düşüşü Bez Zırh parçası verebilir (önceden var; Efsanevi `efs` zarları telafi eder).
- **Tapınak ortak oyunu gerçek cihazlarda grupla doğrulanmadı;** yalnız tek tarayıcıda olay simülasyonuyla test edildi.
- Tapınak: tam temizleme anında bağlantısı kopan ve savaştan sonra dönen oyuncu o katın ödülünü almaz (bilinçli).
  Taş Canavarı için dört ayaklı model yok (golem kullanılıyor). Mini patron iskeleti tahmini. 8. kat ~296k üçgen
  (gölge dahil; Yosunlu İn ~254k).
- GitHub Pages'te bulut kaydı yok: tarayıcının "çerezler ve site verileri" silinirse karakterler gider (Menü → Kodu kopyala ile yedek).
- **Görev sistemi:** gerçek cihazda ve ortak oyun misafir tarafında denenmedi; ödül dengesi (altın / parşömen / mühür) oyuncu geri bildirimiyle ince ayar ister (`QUESTS[].reward`).
- `run.mjs` Baltacı "Yer Sarsan" kontrolü rastgele düzende ara sıra kalıyor (oyun hatası değil).
- Yerel `src/` projesi bu depoyla eşitli değil.

## Son tamamlanan büyük özellikler
- 2026-10-13 Köy meydanı yeniden tasarımı (anıt, zindan girişi salonu, çadır, kulübe, çıkış kapısı, akşam atmosferi) — dal `ozellik/koy-meydani` (main'e alınmadı).
- 2026-10-13 Ana görev zinciri (23 görev, HUD satırı, Görev defteri, NPC ❗/✔, eski kayıt göçü) — main (`c6eba8e`…`a364f0d`; çanta sayfaları + Görevler düğmesi + minimal arayüz dahil).
- 2026-10-13 Beceri Ustalığı Aşama 1 (veri + iki parşömen; parşömenler geçici olarak Tüccar'da) + Tüccar bedava ilk alım hatası düzeltildi — main.
- 2026-10-13 Alev haresi azaltıldı — main.
- 2026-10-13 Demirci +7…+9 daha zor (`UPG.rate`, `GEL_MULT`, malzeme ×1.5) ve Sv 45+ EXP 2 kat (`expNeed`/`expNeed0`) — dal `ozellik/demirci-exp-zorluk`.
- 2026-10-13 Zırh +7…+9 alev kabuğu (`makeFlameShell`, `H.shell`) — main.
- 2026-10-13 Zırh parlaması: doku tabanlı derz çizgileri (`GILD_ARM`, albedo bulanık karşılaştırması), kare parçacıklar kaldırıldı (`gildSparks` yalnız aura) — dal `ozellik/zirh-parlama-duzeltme`.
- 2026-10-13 Zırh +1…+9 efekti referans görsellere göre sıcak altın→alev paletiyle yeniden yazıldı (rünik çizgiler `uLatA`, sarmal şerit parçacıkları) — dal `ozellik/zirh-efekt-referans` (main'e alınmadı).
- 2026-10-12 Görsel: zırh +1…+9 kademeli efekt (`ARMOR_LV`, `GILD_ARM`) ve tapınak renk paleti — dal `ozellik/gorsel-zirh-tapinak` (main'e alınmadı).
- 2026-10-12 Oyun sonu dengesi: tapınak zorluğu, Efsanevi + Taş Mühür ödülleri, Sv 51–70 EXP eğrisi (dal `ozellik/oyun-sonu-denge`).
- 2026-10-12 Bronz Taş Tapınağı (10 katlı dairesel arena grup zindanı) — `ca42025`.
- Kılıç yükseltme görünümü +0…+9 (`3990959`) · yetenek kararlılık penceresi (`0c38673`) · Savaşçı yetenekleri ve animasyonları
  (`032b90e`, `12e578b`, `f65921b`) · Savaşçı sınıfı ve Sv 70 son oyun dengesi (`1889fb6`).
