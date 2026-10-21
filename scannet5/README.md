# Пять сцен ScanNet из posed_images и points с CAD и GT

Набор использует **только подготовленные `posed_images` и `points`** как источники RGB-D, camera poses, intrinsics и облаков сканов. В каждой сцене ровно **300 исходных RGB-D пар**, всего **1500 пар**. Изображения, текстовые camera poses, `intrinsic.txt` и исходный `points/<scene>.bin` скопированы побайтово, с сохранением исходных имён. Кадры не перекодировались, дополнительные кадры не добавлялись, облака не реконструировались и не прореживались.

Дополнительно включены полные ShapeNetCore v2 CAD-ассеты, исходная разметка Scan2CAD и готовые GT-преобразования всех размеченных CAD-экземпляров в координаты скана. Ни полные `.sens`, ни экспорт дополнительных кадров из `.sens` в этот набор не входят.

## 1. Сцены

| Сцена | RGB-D пар | Точек | CAD-экземпляров | Разных CAD | Невалидных camera poses |
| --- | ---: | ---: | ---: | ---: | ---: |
| `scene0472_01` | 300 | 199785 | 12 | 10 | 1 |
| `scene0224_00` | 300 | 75941 | 5 | 5 | 0 |
| `scene0499_00` | 300 | 97088 | 15 | 10 | 3 |
| `scene0568_02` | 300 | 232577 | 12 | 10 | 0 |
| `scene0084_01` | 300 | 111833 | 3 | 3 | 0 |

Всего: **717224 точек, 47 CAD-экземпляров и 37 уникальных CAD-ассетов**. Один и тот же CAD может иметь несколько разных экземпляров в одной сцене и использоваться в нескольких сценах. Данные случайного выбора сохранены в `selection.json`. Все выбранные сцены имеют 300 полных троек JPG/PNG/TXT в `posed_images`.

## 2. Структура

```text
scannet5/
  README.md
  manifest.json                       сводка и конкретные параметры сцен
  selection.json                      список сцен и параметры случайного выбора
  SHA256SUMS.txt                      SHA-256 всех остальных файлов
  scenes/<scene>/
    DATA.md                           данные именно этой сцены
    posed_images/
      intrinsic.txt                   оригинальная матрица 4×4
      00000.jpg ...                    300 оригинальных RGB
      00000.png ...                    300 оригинальных depth PNG
      00000.txt ...                    300 оригинальных camera-to-world poses
    points/
      <scene>.bin                      оригинальное полное облако XYZRGB float32
      pointcloud.ply                   то же облако в PLY
      pointcloud.npz                   те же XYZ и RGB в numpy
    frames.csv                        RGB/depth/pose и валидность по кадрам
    camera/poses.npy                  (300,4,4), float64 из исходных TXT
    camera/valid_poses.npy            (300,), bool
    annotations/
      source_annotation.json          полная исходная запись Scan2CAD
      instances_scannet.json          ID, готовые GT-матрицы, TRS, bbox, keypoints
      T_cad_to_scannet.npy             (M,4,4), float64
      gt_poses_scannet.csv             M строк, без заголовка
      gt_cads_scannet.ply              готовые размещённые GT CAD для просмотра
      cad_appearances.json             число экземпляров каждого CAD в сцене
    validation.json                   проверки исходных данных и GT
  assets/shapenet/<category>/<cad>/
    models/model_normalized.obj       исходная CAD-геометрия
    models/model_normalized.mtl       исходные материалы, если имеются
    models/model_normalized.json      исходные метаданные ShapeNet
    models/*.binvox                   исходные вспомогательные voxel-файлы
    images/*                          исходные текстуры, если имеются
  annotations/full_annotations_selected.json
  annotations/cad_appearances.json
  provenance/source_files.json        пути источников, размеры и SHA-256
  provenance/environment.json         версии библиотек при экспорте
  tools/verify_package.py              проверка файлов; стандартная библиотека Python
```

Все пути внутри архива самостоятельны. CAD хранится один раз в `assets/`, даже если появляется многократно. Материалы и текстуры скопированы вместе с геометрией; ссылки OBJ → MTL → images проверены. Не переносите один OBJ отдельно от зависимых материалов и текстур.

## 3. Полные point clouds

Основной исходный файл — `points/<scene>.bin`. Он **в точности совпадает с исходным `scannet/points/<scene>.bin`**. Это бинарный файл без заголовка: на точку приходится 6 little-endian float32 в порядке **x, y, z, r, g, b**, всего 24 байта. XYZ заданы в метрах в исходной системе координат ScanNet; RGB хранится как float32 со значениями 0…255, а не 0…1.

```python
from pathlib import Path
import numpy as np
root = Path('scenes/scene0472_01')
cloud = np.fromfile(root / 'points/scene0472_01.bin', dtype='<f4').reshape(-1, 6)
xyz = cloud[:, :3]
rgb = cloud[:, 3:]  # RGB, не BGR
```

`pointcloud.npz` содержит массивы `points: (P,3), float32` и `colors: (P,3), float32` с теми же значениями и порядком. `pointcloud.ply` содержит те же XYZ как float32 и RGB как uint8; все исходные RGB оказались целочисленными и преобразуются без потерь. Каждая точка исходного BIN сохранена. Дополнительная вокселизация, случайная подвыборка, центрирование, axisAlignment и изменение масштаба не применялись.

Облако описывает доступную поверхность исходного скана. Это не объединение depth-пикселей выбранных 300 кадров и не гарантия отсутствия дыр или окклюзий. В ZIP нет дополнительно скачанного меша: источник геометрии — именно `points`.

## 4. RGB-D и соответствие кадров

Каталог `posed_images` сохраняет все 901 исходный файл сцены: 300 JPG, 300 PNG, 300 TXT с числовыми именами и один `intrinsic.txt`. Имена сохранены, включая ведущие нули. JPG/PNG/TXT с одинаковой основой относятся к одному подготовленному кадру.

Эти индексы относятся к **подготовленному posed_images**. Они не переименовывались в индексы исходной полной сенсорной записи. В posed_images не представлены исходные timestamps или таблица соответствия индексам `.sens`; они не восстанавливались и не выдумывались.

RGB — исходный JPG. При чтении через OpenCV результат имеет порядок BGR; для RGB используйте `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`. Depth — исходный одноканальный PNG `uint16`. Для метрического depth ScanNet:

```text
Z_camera_metres = depth_uint16 / 1000.0
```

Ноль означает отсутствующее измерение. Depth задаёт Z в системе камеры, а не длину евклидова луча. Читайте его с `cv2.IMREAD_UNCHANGED`; обычное 8-битное чтение теряет метрическую информацию. Никакие ненулевые значения depth не обрезались и не заменялись.

`frames.csv` содержит:

| Поле | Содержание |
| --- | --- |
| `frame_id` | Оригинальная основа имени в posed_images |
| `rgb`, `depth`, `pose` | Пути относительно каталога сцены |
| `pose_valid` | 1 для конечной жёсткой camera-to-world матрицы, иначе 0 |
| `pose_issue` | Причина невалидности либо пустая строка |

Порядок строк — по числовому frame_id. `camera/poses.npy[i]` и `camera/valid_poses.npy[i]` соответствуют строке i этого CSV, без заголовка.

## 5. Camera poses, координаты и intrinsics

Исходный `posed_images/<frame>.txt` содержит матрицу **camera → original ScanNet world**, 4×4. При столбцах координат:

```text
p_scannet_h = T_camera_to_scannet @ p_camera_h
p_camera_h  = inverse(T_camera_to_scannet) @ p_scannet_h
```

Оптическая система камеры: X вправо, Y вниз, Z вперёд. Изображение индексируется `(v,u)` = `(row,column)`, начало пиксельных координат в верхнем левом углу. Матрицы TXT читаются построчно; это не меняет соглашение об умножении столбцов координат. Camera poses, облако points и экспортированный GT CAD согласованы в исходной системе ScanNet, в метрах.

`camera/poses.npy` получен прямым чтением исходных TXT в float64. Исходные TXT сохранены побайтово; массив не означает повышения точности исходных значений. Невалидные позы не исправлялись и кадры не удалялись. Используйте `valid_poses.npy` для операций в общей 3D-системе. Конкретные кадры перечислены в `validation.json` и `DATA.md` каждой сцены.

`posed_images/intrinsic.txt` — исходная матрица 4×4 подготовленного набора. Для проекции используется её верхний левый блок 3×3:

```python
K = np.loadtxt(root / 'posed_images/intrinsic.txt')[:3, :3]
```

Эта матрица соответствует подготовленным RGB-изображениям. RGB и depth имеют разные разрешения; фактические размеры каждой сцены перечислены в manifest и DATA.md. **Отдельной нативной depth-матрицы, color/depth extrinsics и сенсорного заголовка в posed_images нет**, поэтому они не добавлялись из другого источника и не заменялись приблизительными матрицами.

Для точной backprojection depth требуется K_depth, соответствующая этому depth: `p_camera = z * inverse(K_depth) @ [u,v,1]^T`. Нельзя без оговорки считать масштабированную RGB-матрицу точной depth-калибровкой. Предоставленное облако `points` уже существует в общей 3D-системе и не пересчитывалось через такую аппроксимацию. При необходимости точного повторного восстановления depth-лучей потребуется отдельно получить совместимую depth-калибровку; в этом архиве сохранён именно состав исходного posed_images.

## 6. CAD-ассеты и appearances

Каждый CAD определяется парой строк `(category_id, cad_id)`. Сохраняйте ведущие нули category_id. Исходная геометрия находится в `assets/shapenet/<category_id>/<cad_id>/models/model_normalized.obj`. Повторная нормализация, перестановка осей и центрирование CAD не выполнялись.

`cad_appearances.json` имеет структуру `{scene_id: {category_id + '_' + cad_id: count}}`. Count задаёт число отдельных экземпляров CAD в сцене, а не число файлов. У одинаковых CAD ID могут быть разные переносы, повороты и масштабы. Counts проверены по исходным appearances и `aligned_models`.

## 7. Оригинальная разметка и переход между системами

`source_annotation.json` сохраняет все поля и численные значения исходной записи Scan2CAD. `full_annotations_selected.json` содержит пять таких записей списком. Это структурно точная выдержка: форматирование JSON после выделения поднабора может отличаться от исходного полного файла. SHA-256 полного источника записан в provenance.

Оригинальный `scene.trs` переводит **ScanNet world → Scan2CAD annotation world**; `aligned_models[i].trs` переводит **CAD local → тот же annotation world**. Annotation world — отдельная система координат разметки этой сцены. Для TRS:

```text
q = [qw, qx, qy, qz]                       порядок wxyz, Hamilton
M = T(translation) @ R(q) @ diag(sx,sy,sz,1)
M_scan = matrix(scene.trs)
M_cad  = matrix(aligned_models[i].trs)
M_gt   = inverse(M_scan) @ M_cad
p_scannet_h = M_gt @ p_cad_h
```

Масштаб применяется по локальным осям CAD до поворота. Коэффициенты scale не являются размерами bounding box. Translation задаёт положение преобразованного **исходного начала координат CAD**, не обязательно центра объекта. Дополнительный сдвиг `-center` отсутствует. Сохранённый `scene.trs` используется непосредственно, без пересчёта по центру облака.

GT взят из исходной Scan2CAD разметки и заново не подгонялся. Это аннотированные приближённые совмещения: наличие GT не гарантирует идеального совпадения поверхностей или разметки каждого предмета интерьера.

## 8. Поля GT и готовые размещения

`instances_scannet.json` содержит матрицу `T_scannet_to_annotation` и список `instances` в исходном порядке `aligned_models`. `instance_id` — индекс от 0 до M−1 внутри сцены. Порядок записей JSON, строк CSV и матриц NPY совпадает.

| Поле | Смысл |
| --- | --- |
| `instance_id`, `source_aligned_models_index` | Индекс исходного CAD-экземпляра |
| `category_id`, `cad_id` | ID исходного ассета |
| `asset_path` | Путь OBJ относительно корня scannet5 |
| `T_cad_to_scannet` | Готовая 4×4 GT-матрица CAD local → ScanNet world |
| `trs_scannet` | Эквивалентные translation, rotation wxyz и scale |
| `T_cad_to_annotation` | Исходная матрица CAD в annotation world |
| `sym` | Исходный флаг вращательной симметрии Scan2CAD |
| `bbox_center_cad` | Центр bbox в CAD local |
| `bbox_half_extent_cad` | Половины локальных размеров bbox |
| `bbox_corners_scannet` | Восемь углов bbox после GT-преобразования |
| `keypoints_cad_scannet` | CAD-ключевые точки разметки в ScanNet world |
| `keypoints_scan_scannet` | Парные scan-ключевые точки в ScanNet world |

В исходном Scan2CAD JSON **обе группы ключевых точек уже находятся в annotation world**, включая `keypoints_cad.position`. Для них применяется только `inverse(M_scan)`; повторное применение M_cad было бы ошибкой. Соответствия задаются одинаковым индексом пары; исходный плоский массив имеет вид `[x1,y1,z1,...]`.

`T_cad_to_scannet.npy` содержит `(M,4,4)` float64. `gt_poses_scannet.csv` не имеет заголовка, одна строка на экземпляр, ровно 12 полей:

```text
category_id,cad_id,tx,ty,tz,qw,qx,qy,qz,sx,sy,sz
p_scan = R(q) @ diag(sx,sy,sz) @ p_cad + [tx,ty,tz]
```

Кватернион единичный; знак выбран с `qw >= 0`. q и −q эквивалентны. Кватернион уже включает переход в координаты скана и поэтому может отличаться от оригинального annotation-world кватерниона.

`gt_cads_scannet.ply` — объединённый меш всех GT CAD, уже размещённых в той же системе, что и `points/pointcloud.ply`. Откройте оба файла вместе без дополнительного преобразования. Свойство вершины `instance_id` указывает запись JSON. Цвета этого обзорного меша искусственные, для различения экземпляров; исходные материалы сохранены у отдельных CAD в assets.

AxisAlignment ни к облакам, ни к камерам, ни к CAD не применяется. Если используете дополнительную общую матрицу A, применяйте её последовательно ко всем представлениям: `p_new=A@p_scannet`, `T_camera_new=A@T_camera_to_scannet`, `T_cad_new=A@T_cad_to_scannet`.

## 9. Проверки и источники

Проверено по 300 полных RGB/depth/pose троек каждой сцены; все JPG и PNG декодированы, depth имеет dtype uint16. Каждый исходный файл posed_images, каждый points.bin и все CAD-файлы сверены с копиями по SHA-256. Готовый PLY сверён со всеми исходными точками и цветами без изменения порядка. Невалидные camera poses сохранены и помечены.

GT проверен независимыми реализациями кватернионной матрицы; для всех размещённых вершин проверен переход обратно в annotation world. JSON/CSV TRS воспроизводят GT-матрицы, appearances совпадают с исходными counts. Подробные результаты находятся в validation.json.

Точные источники указаны в `selection.json` и `provenance/source_files.json`: RGB-D, poses и intrinsic из локального `scannet/posed_images`; геометрия из `scannet/points`; CAD и GT из локального Scan2CAD. Это именно копия подготовленных входов; побайтовая идентичность JPEG исходному `.sens` в этом экспорте не заявляется.

После распаковки проверить все файлы можно так:

```sh
cd scannet5
python tools/verify_package.py
# или:
sha256sum -c SHA256SUMS.txt
```

SHA256SUMS охватывает каждый другой файл набора, включая документацию и скрипт; собственный хеш он не содержит. Для ZIP рядом предоставляется отдельный `.sha256`. Каждый член архива после записи проверен по CRC32 и SHA-256.

Формат исходной CAD-разметки описан в [Scan2CAD README](https://github.com/skanti/Scan2CAD#format-of-the-datasets), исходная геометрическая конвенция — в [Annotation2Mesh.py](https://github.com/skanti/Scan2CAD/blob/master/Routines/Script/Annotation2Mesh.py). Численные GT-преобразования в этом наборе вычислены из локальных исходных аннотаций.
