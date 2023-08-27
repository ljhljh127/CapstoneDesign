import json
from dataclasses import dataclass
from typing import Dict, List

# 디플로이먼트 Response Class

@dataclass
class DeploymentResponse:
    kind: str
    apiVersion: str
    metadata: Dict
    items: List


