# scene0499_00

300 исходных RGB-D пар из posed_images. Облако из points: 97088 точек. CAD: 15 экземпляров, 10 разных ассетов. Невалидных camera poses: 3.

Полное описание: [README.md](../../README.md). Все исходные имена кадров сохранены; соответствия находятся в frames.csv.

## Изображения и intrinsics

RGB shapes (H,W,C): [[968, 1296, 3]]. Depth shapes (H,W): [[480, 640]]. Depth uint16, метры = raw / 1000.

Оригинальная intrinsic.txt (4×4):

```text
1161.74597 0 658.041992 0
0 1159.10706 486.467102 0
0 0 1 0
0 0 0 1
```

Это RGB intrinsics подготовленного набора; отдельная native depth K в posed_images отсутствует.

## Невалидные camera poses

[{"frame_id": "00270", "reason": "nonfinite_source_pose"}, {"frame_id": "00271", "reason": "nonfinite_source_pose"}, {"frame_id": "00272", "reason": "nonfinite_source_pose"}]

Изображения и исходные pose-файлы этих кадров сохранены; используйте camera/valid_poses.npy.

## CAD-экземпляры

| instance_id | category_id | cad_id |
| --- | --- | --- |
| 0 | `04379243` | `51c7851a252ed0ff8211891ea560a7f0` |
| 1 | `02747177` | `c21d8f5641be31a285cac25b72167160` |
| 2 | `02747177` | `c21d8f5641be31a285cac25b72167160` |
| 3 | `04379243` | `899f815eaad62b56d8cad143689f8b51` |
| 4 | `04379243` | `525d48d65079b2003f222a37719e9945` |
| 5 | `04379243` | `525d48d65079b2003f222a37719e9945` |
| 6 | `03001627` | `1ab4c6ef68073113cf004563556ddb36` |
| 7 | `03001627` | `a1575aa70fbaab0fc05575120a46cd3b` |
| 8 | `04379243` | `2b2d827267baf5e75510d59f3ab1ed64` |
| 9 | `03001627` | `708fabd1e1a39a77aa6bb5920f533ce3` |
| 10 | `03001627` | `708fabd1e1a39a77aa6bb5920f533ce3` |
| 11 | `04256520` | `556166f38429cdfe29bdd38dd4a1a461` |
| 12 | `04256520` | `556166f38429cdfe29bdd38dd4a1a461` |
| 13 | `03001627` | `d27be0741f13327efc66b92945eed242` |
| 14 | `03001627` | `d27be0741f13327efc66b92945eed242` |
