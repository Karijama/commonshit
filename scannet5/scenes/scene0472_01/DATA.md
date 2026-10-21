# scene0472_01

300 исходных RGB-D пар из posed_images. Облако из points: 199785 точек. CAD: 12 экземпляров, 10 разных ассетов. Невалидных camera poses: 1.

Полное описание: [README.md](../../README.md). Все исходные имена кадров сохранены; соответствия находятся в frames.csv.

## Изображения и intrinsics

RGB shapes (H,W,C): [[968, 1296, 3]]. Depth shapes (H,W): [[480, 640]]. Depth uint16, метры = raw / 1000.

Оригинальная intrinsic.txt (4×4):

```text
1165.65601 0 653.70105 0
0 1165.33203 479.037018 0
0 0 1 0
0 0 0 1
```

Это RGB intrinsics подготовленного набора; отдельная native depth K в posed_images отсутствует.

## Невалидные camera poses

[{"frame_id": "00101", "reason": "nonfinite_source_pose"}]

Изображения и исходные pose-файлы этих кадров сохранены; используйте camera/valid_poses.npy.

## CAD-экземпляры

| instance_id | category_id | cad_id |
| --- | --- | --- |
| 0 | `04256520` | `a109fd29656079e714b96b665a8ac321` |
| 1 | `02818832` | `76db17c76f828282dcb2f14e2e42ec8d` |
| 2 | `03337140` | `4ecbfec208b1aac12f84cb7932f866fd` |
| 3 | `04379243` | `91f6f0813eaf4e52707cdefe012d0353` |
| 4 | `03001627` | `5a4c550b1b41114c3d2617f9171b5ccb` |
| 5 | `03001627` | `5a4c550b1b41114c3d2617f9171b5ccb` |
| 6 | `04379243` | `e0229fb0e8d85e1fbfd790572919a77f` |
| 7 | `04330267` | `b296fbfbbe5dccf09c12d6260da9ac2b` |
| 8 | `02933112` | `146c3a9cbe3d8f703fe047712e43e185` |
| 9 | `02933112` | `da5d7b5dfa92abdace5d6e9371bb5c33` |
| 10 | `02933112` | `8382308b895aa93286d53ab0fe94e911` |
| 11 | `02933112` | `8382308b895aa93286d53ab0fe94e911` |
