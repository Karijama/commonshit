# scene0224_00

300 исходных RGB-D пар из posed_images. Облако из points: 75941 точек. CAD: 5 экземпляров, 5 разных ассетов. Невалидных camera poses: 0.

Полное описание: [README.md](../../README.md). Все исходные имена кадров сохранены; соответствия находятся в frames.csv.

## Изображения и intrinsics

RGB shapes (H,W,C): [[968, 1296, 3]]. Depth shapes (H,W): [[480, 640]]. Depth uint16, метры = raw / 1000.

Оригинальная intrinsic.txt (4×4):

```text
1170.18799 0 647.75 0
0 1170.18799 483.75 0
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
| 0 | `02871439` | `465bb5a9ed42ad40a5817f81a1efa3cc` |
| 1 | `04256520` | `8efa91e2f3e2eaf7bdc82a7932cd806` |
| 2 | `03938244` | `b5cb58fb099204fea5c423249b53dbc4` |
| 3 | `02818832` | `f6fb20673932fe50230e608bf41b643e` |
| 4 | `02933112` | `8bd6e4ce15468e1ad6eefa796d2f261c` |
