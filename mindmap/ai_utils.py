import os
import json
import requests
from typing import Dict, List, Any, Optional

class AIAssistant:
    """DeepSeek AI助手，用于想法扩展和对话"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化AI助手"""
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
    def expand_idea(self, idea: str) -> Dict[str, Any]:
        """将简短想法扩展为完整概念"""
        if not self.api_key or self.api_key.strip() == "":
            return self._mock_expand_idea(idea)
            
        prompt = f"""请将以下简短想法扩展为更完整的概念。
想法: {idea}

请按以下JSON格式返回:
{{
  "title": "核心概念标题",
  "summary": "概念的简短总结(150字以内)",
  "details": "详细解释(300-500字)",
  "related_concepts": ["相关概念1", "相关概念2", "相关概念3"],
  "action_items": ["可执行的行动项1", "可执行的行动项2"]
}}
"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                # 解析JSON响应
                try:
                    return json.loads(content)
                except:
                    return {"error": "无法解析AI响应", "expanded": idea}
            else:
                if "error" in result:
                    error_msg = result.get("error", {}).get("message", "未知错误")
                    return {"error": f"API错误: {error_msg}", "expanded": idea}
                return {"error": "AI响应为空", "expanded": idea}
            
        except Exception as e:
            return {"error": f"AI扩展失败: {str(e)}", "expanded": idea}
            
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """与AI对话"""
        if not self.api_key or self.api_key.strip() == "":
            return self._mock_chat(messages)
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                if "error" in result:
                    error_msg = result.get("error", {}).get("message", "未知错误")
                    return f"API错误: {error_msg}"
                return "AI回复获取失败。请稍后再试。"
            
        except Exception as e:
            return f"AI对话失败: {str(e)}"
            
    def _mock_expand_idea(self, idea: str) -> Dict[str, Any]:
        """生成模拟的AI扩展响应（无API密钥时使用）"""
        # 简单处理输入想法
        words = idea.split()
        title = " ".join(words[:min(5, len(words))]).capitalize()
        
        return {
            "title": f"{title}",
            "summary": f"这是关于'{idea}'的扩展概念。在实际部署中，这里会显示由DeepSeek AI生成的内容摘要，大约150字。",
            "details": f"这是关于'{idea}'的详细解释。在实际部署中，这部分会由DeepSeek AI生成300-500字的详细阐述，包括概念背景、重要性以及应用场景等。这是模拟数据，实际使用时请配置有效的API密钥。",
            "related_concepts": [
                f"与{idea}相关的概念1", 
                f"与{idea}相关的概念2", 
                f"与{idea}相关的概念3"
            ],
            "action_items": [
                f"关于{idea}的行动项1", 
                f"关于{idea}的行动项2"
            ]
        }
        
    def _mock_chat(self, messages: List[Dict[str, str]]) -> str:
        """生成模拟的AI对话响应（无API密钥时使用）"""
        last_message = messages[-1]["content"] if messages else ""
        
        return f"AI助手: 您提到了'{last_message}'。这是一个模拟回复。在实际部署时，这里会显示DeepSeek AI的真实回复。请在设置页面配置有效的API密钥以获得完整功能。" 