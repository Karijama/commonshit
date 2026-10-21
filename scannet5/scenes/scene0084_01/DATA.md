# scene0084_01

300 исходных RGB-D пар из posed_images. Облако из points: 111833 точек. CAD: 3 экземпляров, 3 разных ассетов. Невалидных camera poses: 0.

Полное описание: [README.md](../../README.md). Все исходные имена кадров сохранены; соответствия находятся в frames.csv.

## Изображения и intrinsics

RGB shapes (H,W,C): [[968, 1296, 3]]. Depth shapes (H,W): [[480, 640]]. Depth uint16, метры = raw / 1000.

Оригинальная intrinsic.txt (4×4):

```text
1169.62109 0 646.295044 0
0 1167.1051 489.927032 0
0 0 1 0
0 0 0 1
```

Это RGB intrinsics подготовленного набора; отдельная native depth K в posed_images отсутствует.

## Невалидные camera poses

[]

Изображения и исходные pose-файлы этих кадров сохранены; используйте camera/valid_poses.npy.

## CAD-экземпляры

| instance_id | category_id | cad_id |
| --- | --- | --- |
| 0 | `02808440` | `3b222c644a783ebbfcd4910413c446d9` |
| 1 | `02747177` | `85d8a1ad55fa646878725384d6baf445` |
| 2 | `03001627` | `56e194146b9e584b3321831d2245cf06` |
