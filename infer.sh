#!/usr/bin/env bash
set -e
set -o pipefail

export MODELSCOPE_CACHE=./cache
export PYTORCH_ALLOC_CONF=expandable_segments:True

CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0} \
VLLM_DISABLE_DISTRIBUTED=1 \
swift infer \
  --model Qwen/Qwen3-14B \
  --adapters ./adapters \
  --infer_backend vllm \
  --temperature 0 \
  --max_new_tokens 1024 \
  --val_dataset ./example.jsonl \
  --result_path ./example_result.jsonl

