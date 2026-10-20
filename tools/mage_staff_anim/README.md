# Büyücü asa klipleri (MAGE_STAFF_ANIM)

Kaynak: kullanıcının bilgisayarında `Belgeler\tas_muhru_anim\buyucu_anim.blend` (Blender 5.2).
- Sahne: `buyucu_zambak.glb` + `buyucu_asa_yildirim.glb`. `AsaKontrol` boş nesnesi asayı taşır; sağ el `SagElH`'ye,
  sol el `SolTutus` (asa üzerinde, `SolKay` ile kayar) / `SolSerbest` karışımına IK (2 kemik) + dönüş kopyası ile bağlı; ayaklar IK.
- Metin bloğu `tm_rig.py`: poz yazım kütüphanesi (`V`, `Qe`, `applyPose`, `clip`, `useClip`, `shots`). Klip kaynak eylemleri
  `src_<klip>|<nesne>` adıyla dosyada saklı (yeniden düzenlenebilir).
- Dışa aktarım: her kare için kemik deformasyonu `pose.matrix · rest⁻¹` → `mage_staff_clips.json`.
- `python3 build_clips.py` (depo kökünde, json yanında): glTF düğüm dinlenme pozuna göre yerel dönüşler → `mage_staff_anim.json`;
  içerik `index.html`'deki `const MAGE_STAFF_ANIM = …;` satırına yapıştırılır.
- Klipler: idleGuard, atkA, atkB, atkC, atkShot, skM1–skM4 (24 kare/sn). Temas/olay kareleri: `MAGE_ATK_T`, `MAGE_SKILL_T`.
