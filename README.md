# KeyframeFace: Language-Driven Facial Animation via Semantic Keyframes

![KeyframeFace Architecture](./image/teaser.jpg)

Official inference code for **KeyframeFace: Language-Driven Facial Animation via Semantic Keyframes**.

[Paper](https://arxiv.org/abs/2512.11321) | [Model](https://modelscope.cn/models/chaochaooooooo/KeyframeFace) | [Dataset](https://modelscope.cn/datasets/chaochaooooooo/KeyframeFace_Dataset)

KeyframeFace generates sparse, semantically meaningful facial keyframes from language. Each keyframe is represented by 52 ARKit blendshapes and 9 head/eye pose parameters, and can be used directly in an ARKit/MetaHuman animation pipeline.

The accompanying dataset contains 2,100 expressive scripts with monocular videos, per-frame ARKit coefficients, contextual backgrounds, manually defined keyframes, and multi-perspective language annotations.

This public release intentionally contains only the lightweight inference interface and format converter, following the release style of [SemanticFace](https://github.com/kangzejian1896/SemanticFace). Training and dataset-processing code are not included.

## Installation

```bash
conda create -n keyframeface python=3.10
conda activate keyframeface
pip install -U ms-swift
pip install vllm modelscope
```

## Model Download

Download the released LoRA adapter to `./adapters`:

```bash
modelscope download --model chaochaooooooo/KeyframeFace --local_dir ./adapters
```

## Inference

`example.jsonl` contains one request per semantic keyframe. Each request includes the full expression sequence and asks the model to generate one target keyframe, preserving global consistency.

```bash
bash infer.sh
```

Results are saved to `example_result.jsonl` in the following form:

```json
{"Keyframe_one": {"EyeBlinkLeft": 0.0, "...": 0.0, "RightEyeRoll": 0.0}}
```

If vLLM runs out of memory, change `--infer_backend vllm` to `--infer_backend pt` in `infer.sh`.

## Convert to MetaHuman CSV

```bash
python jsonl2csv.py
```

The generated `example_result.csv` uses the same 61-channel order as the model output and can be imported into an ARKit-compatible animation workflow.

## Citation

```bibtex
@misc{wu2026keyframeface,
  title         = {KeyframeFace: Language-Driven Facial Animation via Semantic Keyframes},
  author        = {Jingchao Wu and Zejian Kang and Haibo Liu and Yuanchen Fei and Xiangru Huang},
  year          = {2026},
  eprint        = {2512.11321},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV},
  doi           = {10.48550/arXiv.2512.11321}
}
```

## Acknowledgement

The lightweight inference release and MetaHuman CSV interface are inspired by [SemanticFace](https://github.com/kangzejian1896/SemanticFace).
