import torch
from pathlib import Path
from model import HandSignClassifier

ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "data" / "hand_sign_model.pth"
OUTPUT_PATH = ML_DIR / "data" / "hand_sign_model.onnx"

model = HandSignClassifier(num_classes=7)

model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

example_inputs =torch.randn(1, 21, 2, dtype=torch.float32)

onnx_program = torch.onnx.export(model, example_inputs, dynamo=True)
onnx_program.save(OUTPUT_PATH)