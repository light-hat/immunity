import sys

import torch
import torch.nn as nn
from transformers import BertModel

import json
import requests
from transformers import AutoTokenizer

import base64
import logging
import ast
import traceback

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class IAST_BERT(nn.Module):
    def __init__(self, bert_model_name="bert-base-uncased", num_classes=10):
        super(IAST_BERT, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.fc_request = nn.Linear(768, 256)
        self.fc_control_flow = nn.Linear(768, 256)
        self.fc_response = nn.Linear(768, 256)
        self.fc_final = nn.Linear(256 * 3, num_classes)

    def forward(self, request_input, request_mask, control_flow_input, control_flow_mask, response_input, response_mask):
        # Request
        request_outputs = self.bert(input_ids=request_input, attention_mask=request_mask)
        request_features = self.fc_request(request_outputs.pooler_output)

        # Control Flow
        control_flow_outputs = self.bert(input_ids=control_flow_input, attention_mask=control_flow_mask)
        control_flow_features = self.fc_control_flow(control_flow_outputs.pooler_output)

        # Response
        response_outputs = self.bert(input_ids=response_input, attention_mask=response_mask)
        response_features = self.fc_response(response_outputs.pooler_output)

        # Объединение
        combined_features = torch.cat([request_features, control_flow_features, response_features], dim=1)
        logits = self.fc_final(combined_features)

        return logits

def main(base64_encoded_data):
    # Декодируем Base64 обратно в строку JSON
    json_data = base64.b64decode(base64_encoded_data).decode('utf-8')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Укажите репозиторий
    repo_id = "l1ghth4t/immunity"

    # Загрузка конфигурации
    config_path = f"https://huggingface.co/{repo_id}/resolve/main/config.json"
    config = json.loads(requests.get(config_path).text)

    label2id = {'CWE-16': 0,
        'CWE-352': 1,
        'CWE-400': 2,
        'CWE-502': 3,
        'CWE-639': 4,
        'CWE-77': 5,
        'CWE-79': 6,
        'CWE-89': 7,
        'CWE-918': 8,
        'Clean': 9
    }
    id2label = {idx: label for label, idx in label2id.items()}

    # Инициализация модели
    model = IAST_BERT(
        bert_model_name=config["bert_model_name"],
        num_classes=11
    )
    model = model.to(device)

    # Загрузка весов
    state_dict_path = f"https://huggingface.co/{repo_id}/resolve/main/pytorch_model.bin"
    state_dict = torch.hub.load_state_dict_from_url(state_dict_path, map_location=device)
    model.load_state_dict(state_dict)

    # Загрузка токенизатора
    tokenizer = AutoTokenizer.from_pretrained(repo_id)

    # Модель готова
    model.eval()

    def preprocess(example):
        json_example = ast.literal_eval(example)
        # Обработка блока Request
        request_text = f"URL: {json_example['request']['url']}\n" \
                       f"Method: {json_example['request']['method']}\n" \
                       f"Headers: {json_example['request']['headers']}\n" \
                       f"Body: {json_example['request']['body']}"
        request_tokens = tokenizer(request_text, truncation=True, padding="max_length", max_length=512,
                                   return_tensors="pt")

        # Обработка блока Control Flow
        control_flow_text = "\n".join([f"{k}: {v}" for k, v in json_example['control_flow'].items()])
        control_flow_tokens = tokenizer(control_flow_text, truncation=True, padding="max_length", max_length=512,
                                        return_tensors="pt")

        # Обработка блока Response
        response_text = f"Status Code: {json_example['response']['status_code']}\n" \
                        f"Headers: {json_example['response']['headers']}"
        response_tokens = tokenizer(response_text, truncation=True, padding="max_length", max_length=512,
                                    return_tensors="pt")

        return {
            "request_input_ids": request_tokens["input_ids"].squeeze(0).to(device),
            "request_attention_mask": request_tokens["attention_mask"].squeeze(0).to(device),
            "control_flow_input_ids": control_flow_tokens["input_ids"].squeeze(0).to(device),
            "control_flow_attention_mask": control_flow_tokens["attention_mask"].squeeze(0).to(device),
            "response_input_ids": response_tokens["input_ids"].squeeze(0).to(device),
            "response_attention_mask": response_tokens["attention_mask"].squeeze(0).to(device),
        }

    context_processed = preprocess(json_data)

    logits = model(
        request_input=context_processed["request_input_ids"].unsqueeze(0).to(device),
        request_mask=context_processed["request_attention_mask"].unsqueeze(0).to(device),
        control_flow_input=context_processed["control_flow_input_ids"].unsqueeze(0).to(device),
        control_flow_mask=context_processed["control_flow_attention_mask"].unsqueeze(0).to(device),
        response_input=context_processed["response_input_ids"].unsqueeze(0).to(device),
        response_mask=context_processed["response_attention_mask"].unsqueeze(0).to(device)
    )

    predicted_class = torch.argmax(logits, dim=1).item()
    print(id2label[predicted_class])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Ошибка: необходимо указать одну строку в качестве аргумента.")
        sys.exit(1)

    base64_encoded_data = sys.argv[1]
    try:
        main(base64_encoded_data)
    except Exception:
        error_traceback = traceback.format_exc()
        logging.error("Произошла ошибка:\n", error_traceback)
        sys.exit(2)
    else:
        sys.exit(0)
