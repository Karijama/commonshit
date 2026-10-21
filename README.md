# commonshit-main

Экспериментальный пайплайн для оценки позы CAD-объекта по нескольким изображениям сцены с помощью локальной VLM-модели. Проект разделён на три независимых этапа:

1. выбор информативных ракурсов объекта;
2. подготовка запроса и запуск Qwen через локальный Ollama;
3. независимая оценка предсказанной позы относительно ground truth.

Модель не обучается и не получает ground-truth позу объекта во время инференса.

## Структура проекта

```text
commonshit-main/
├── experiments/vlm_pose/
│   ├── select_views.py       # выбор ракурсов и подготовка model_input/
│   ├── run_qwen.py           # запрос к локальному Ollama/Qwen
│   ├── evaluate_pose.py      # расчёт метрик по готовому prediction.json
│   ├── test_*.py             # модульные тесты
│   └── results/              # результаты запусков и диагностические галереи
├── scannet5/
│   └── manifest.json         # описание доступного набора данных
└── requirements.txt
```

## Данные

По умолчанию скрипты ожидают датасет в каталоге `scannet5/`. В манифесте указано 5 сцен, 1500 RGB-кадров, 47 CAD-инстансов и 37 уникальных CAD-ассетов. Координаты заданы в исходной мировой системе ScanNet, единица измерения — метр.

Проверить описание набора можно в [`scannet5/manifest.json`](scannet5/manifest.json).

## Установка

Требуется Python 3.10+ и установленный Ollama для этапа инференса.

```powershell
cd commonshit-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Зависимости: NumPy, SciPy, Pillow и requests.

## 1. Выбор ракурсов

Выбрать три ракурса для всех сцен:

```powershell
python experiments/vlm_pose/select_views.py `
  --root scannet5 `
  --output experiments/vlm_pose/results `
  --scenes all `
  --views 3
```

Для одной сцены:

```powershell
python experiments/vlm_pose/select_views.py `
  --root scannet5 `
  --output experiments/vlm_pose/results `
  --scenes scene0084_01
```

Для каждого CAD-инстанса создаются:

- `model_input/` — изображения и `input.json`, которые разрешено передавать модели;
- `selection.json` — оценки всех кадров и выбранные кадры;
- `evaluation_only.json` — ground truth, предназначенный только для оценки;
- `gt_projection_*.jpg` — диагностические проекции;
- `index.html` — HTML-галерея результатов сцены.

Красные точки на диагностических изображениях — это проекция вершин CAD, а не маска сегментации.

Основные параметры выбора:

- `--score in_frustum_vertices` — ранжирование по числу вершин в поле зрения;
- `--score approx_unoccluded_vertices` — ранжирование с приближённой проверкой окклюзий;
- `--min-angle 15` — исключение почти одинаковых направлений обзора;
- `--cell 4`, `--scan-radius 1`, `--tolerance 0.10` — параметры приближённого z-buffer.

## 2. Запуск Qwen через Ollama

Установить и запустить Ollama, затем загрузить модель:

```powershell
ollama pull qwen3.5:9b
```

Подготовить запрос без запуска инференса:

```powershell
python experiments/vlm_pose/run_qwen.py `
  --root scannet5 `
  --input experiments/vlm_pose/results/scene0084_01/instance_00/model_input/input.json `
  --output runs/scene0084_01_instance_00 `
  --prepare-only
```

Запустить локальный инференс:

```powershell
python experiments/vlm_pose/run_qwen.py `
  --root scannet5 `
  --input experiments/vlm_pose/results/scene0084_01/instance_00/model_input/input.json `
  --output runs/scene0084_01_instance_00
```

Скрипт принимает только loopback-адрес Ollama (`127.0.0.1`, `localhost` или `::1`). Результаты сохраняются в каталог запуска:

- `cad_preview.jpg` — канонические виды CAD с локальными осями;
- `request.json` — сформированный запрос;
- `response.json` — сырой ответ Ollama;
- `prediction.json` — проверенное предсказание;
- `model_info.json`, `ollama_models.json` — информация о модели и доступных тегах.

Формат успешного предсказания:

```json
{
  "status": "ok",
  "translation": [0.0, 0.0, 0.0],
  "rotation_wxyz": [1.0, 0.0, 0.0, 0.0],
  "scale_xyz": [1.0, 1.0, 1.0],
  "confidence": 0.5,
  "explanation": "..."
}
```

Преобразование имеет вид:

```text
p_world = R(rotation_wxyz) · diag(scale_xyz) · p_cad + translation
```

Для статусов `ambiguous`, `not_visible` и `insufficient` поля позы должны быть `null`.

## 3. Оценка позы

Оценить ранее сохранённое предсказание:

```powershell
python experiments/vlm_pose/evaluate_pose.py `
  --root scannet5 `
  --prediction runs/scene0084_01_instance_00/prediction.json `
  --ground-truth experiments/vlm_pose/results/scene0084_01/instance_00/evaluation_only.json `
  --output runs/scene0084_01_instance_00/evaluation.json
```

Отчёт содержит:

- ошибку переноса в метрах;
- сырую ошибку вращения в градусах;
- относительную ошибку масштаба по трём локальным осям;
- среднюю ошибку соответствующих вершин;
- среднюю ошибку от предсказанных вершин до ближайших ground-truth вершин.

Ошибка вращения не инвариантна к симметриям объекта. Информация о симметрии сохраняется в отчёте, но автоматически не применяется.

## Тесты

Запустить все тесты:

```powershell
python -m unittest discover -s experiments/vlm_pose -p "test_*.py"
```

Тесты проверяют преобразования координат, проекцию и z-buffer, отбор ракурсов, валидацию позы и корректное изменение камеры при уменьшении изображений.

## Ограничения и воспроизводимость

- Видимость оценивается приближённым point z-buffer, а не трассировкой лучей по треугольникам.
- Неизвестная глубина ScanNet отдельно учитывается и не считается доказательством видимости.
- Ground-truth проекции и `evaluation_only.json` нельзя передавать модели.
- Скрипт `run_qwen.py` не выполняет геометрическое уточнение после ответа модели.
- Результаты и временные запуски (`results/`, `runs/`, `prepared_*/`) исключены из Git через [`.gitignore`](.gitignore).

Готовые диагностические результаты текущего запуска доступны через [`experiments/vlm_pose/results/`](experiments/vlm_pose/results/).
