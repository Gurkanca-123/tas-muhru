# Büyücü asa klipleri (MAGE_STAFF_ANIM)

Kaynak: kullanıcının bilgisayarında `Belgeler\tas_muhru_anim\buyucu_anim.blend` (Blender 5.2).
- Sahne: `buyucu_zambak.glb` + `buyucu_asa_yildirim.glb`. `AsaKontrol` boş nesnesi asayı taşır; sağ el `SagElH`'ye,
  sol el `SolTutus` (asa üzerinde, `SolKay` ile kayar) / `SolSerbest` karışımına IK (2 kemik) + dönüş kopyası ile bağlı; ayaklar IK.
- Metin bloğu `tm_rig.py`: poz yazım kütüphanesi (`V`, `Qe`, `applyPose`, `clip`, `useClip`, `shots`). Klip kaynak eylemleri
  `src_<klip>|<nesne>` adıyla dosyada saklı (yeniden düzenlenebilir).
- Dışa aktarım: her kare için kemik deformasyonu `pose.matrix · rest⁻¹` → `mage_staff_clips.json`.
- `python3 build_clips.py` (depo kökünde, json yanında): glTF düğüm dinlenme pozuna göre yerel dönüşler → `mage_staff_anim.json`;
  içerik `index.html`'deki `const MAGE_STAFF_ANIM = …;` satırına yapıştırılır.
- Klipler: idleGuard, atkA, atkB, atkC, skM1–skM4 (24 kare/sn). Metin bloğu `tm_clips.py`: klip poz tabloları (yeniden çalıştırılabilir); atkA/B/C için güncel tablolar `tm_clips_v2.py`, oyun verisine çevirme `tm_export.py` (`bake(ad)`). Asa kontrolde 0.15 birim yukarı kaydırılmış (oyunda `MAGE_GRIP_SHIFT`). Temas/olay kareleri: `MAGE_ATK_T`, `MAGE_SKILL_T`.

## Beceri klipleri v3 ve efektler (2026-10-22)
- `tm_clips_v3.py`: skM1–skM4 poz tabloları (`spin(poz, açı)`: gövde çerçevesindeki pozu dikey eksende döndürür; skM3 360° dönüş). Pişirme: `tm_export.py` `bake(ad)` → JSON → `MAGE_STAFF_ANIM.clips`.
- `gen_fx.py`: `fx_flame0/1.png`, `fx_boom.png` (4×4 kare atlas), `fx_frost.png`. `tm_fx_lib.py` + `tm_fx_flame.py` aynı gölgelendiricinin Blender sürümü; MCP üzerinden render Blender'ı çökerttiği için dokular `gen_fx.py` ile üretildi.
- `tm_fx_more.py` `shards_export()`: buz kristalleri (`buz_sivri`, `buz_kalin`, `buz_ince`, `buz_kume`) → `buyucu_fx_buz.glb`.
- `buyucu_fx.js` = `TM_ASSETS.buyucu_fx_buz` (GLB base64) + `TM_FX_TEX` (PNG data URI). Değişince `MAGE_FX_FILE` sürüm eki artırılır.
