# Taş Mührü — proje durumu (kısa teknik hafıza)

Son güncelleme: 2026-10-12 · `main` = `ca42025` (Bronz Taş Tapınağı). Satır numaraları bu sürüme göredir ve kayar;
her zaman `grep -n` ile doğrula.

## Dosyalar
- `index.html` (~5.8 MB, 17.4k satır): tüm oyun. 1–503 CSS + DOM · 504–511 betik etiketleri + `window.TM_NET` (Supabase) ·
  sonrası tek büyük `<script>`. ~2700–7700 gömülü SkeletonUtils + GLTFLoader (üçüncü taraf, dokunma) · ~7777–7800
  `OUTFIT_DATA` + `GEAR_GLTF` (base64 kılıç/balta/kıyafet GLB'leri).
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
- **Karakter:** sınıflar `baltaci` (Baltacı) ve `warrior` (Savaşçı); ikisi de GLB gövde + AnimationMixer, zırh setine göre gövde
  değişir. Yetenek animasyonu kilidi `SKILL_LOCK` / `SAVASCI_SKILL_T`. Statlar `recalc()` → `D`.
- **Beceri ustalığı (Aşama 1, main):** DENEME: iki parşömen Tüccar'da geçici satılık (`SHOP_LIST`, `price`) — kaynakları belirlenince kaldır. `P.mastery[beceriId]` 0 normal · 1…10 M1…M10 · 11…15 G1…G5 (`MASTERY`, `masteryOf`, `masteryLabel`, `skillLvText`). Geçişler yalnız parşömenle: `usta_parsomen` (Seviye `SKILL_MAX` → M1), `busta_parsomen` (M10 → G1) — `MASTERY_SCROLLS`, `masteryCheck`, `useMasteryScroll`, çanta `UI.masteryActs`. Güç etkisi yok; `applySave` doğrular.
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

## Bilinen sorunlar / kısıtlar
- **Tapınak dengesi:** 2026-10-12'de yeniden dengelendi (simülasyon tabanlı; CHANGELOG_DEV.md). Gerçek oyuncu geri bildirimiyle ince ayar
  gerekir; kaldıraçlar `TEMPLE_POW`, `TEMPLE_FLOORS` dalgaları, `MOBS` çarpanları. Mühür / Efsanevi şansları `TEMPLE_REWARDS`.
- Set sınıflarında tapınağın sıradan `gear` düşüşü Bez Zırh parçası verebilir (önceden var; Efsanevi `efs` zarları telafi eder).
- **Tapınak ortak oyunu gerçek cihazlarda grupla doğrulanmadı;** yalnız tek tarayıcıda olay simülasyonuyla test edildi.
- Tapınak: tam temizleme anında bağlantısı kopan ve savaştan sonra dönen oyuncu o katın ödülünü almaz (bilinçli).
  Taş Canavarı için dört ayaklı model yok (golem kullanılıyor). Mini patron iskeleti tahmini. 8. kat ~296k üçgen
  (gölge dahil; Yosunlu İn ~254k).
- GitHub Pages'te bulut kaydı yok: tarayıcının "çerezler ve site verileri" silinirse karakterler gider (Menü → Kodu kopyala ile yedek).
- `run.mjs` Baltacı "Yer Sarsan" kontrolü rastgele düzende ara sıra kalıyor (oyun hatası değil).
- Yerel `src/` projesi bu depoyla eşitli değil.

## Son tamamlanan büyük özellikler
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
