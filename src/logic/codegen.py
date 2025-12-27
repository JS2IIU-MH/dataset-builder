"""
codegen.py
処理履歴からPandasコード自動生成
"""
from typing import List

def generate_code(history: List[str]) -> str:
    """履歴リストからPandasコードを生成"""
    code = "import pandas as pd\n"
    for step in history:
        code += step + "\n"
    return code
