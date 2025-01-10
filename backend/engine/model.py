import torch
import torch.nn as nn
from transformers import BertModel


class IAST_BERT(nn.Module):
    """
    Модель машинного обучения для детектирования уязвимостей в
    контексте выполнения запросов.
    """

    def __init__(self, bert_model_name="bert-base-uncased", num_classes=5):  # 11
        super(IAST_BERT, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.fc_request = nn.Linear(768, 256)
        self.fc_control_flow = nn.Linear(768, 256)
        self.fc_response = nn.Linear(768, 256)
        self.fc_final = nn.Linear(256 * 3, num_classes)

    def forward(self, request_input, request_mask, control_flow_input, control_flow_mask, response_input,
                response_mask):
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