import sys
from pathlib import Path

# 确保 app 目录在路径中，以便能导入 core 模块
# 这必须在导入 core 之前执行
app_dir = Path(__file__).parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

import httpx
from typing import List, Dict, Optional
from backend.app.core.config import settings
from backend.app.core.proxy import get_proxies


class GoogleSearchTool:
    """Google 搜索工具类"""

    def __init__(self):
        """初始化 Google 搜索工具"""
        self.api_key = settings.GOOGLE_API_KEY
        self.cse_id = settings.GOOGLE_CSE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(
        self,
        query: str,
        num_results: int = 10,
        start_index: int = 1,
        language: str = "lang_zh-CN"
    ) -> Optional[Dict]:
        """
        执行 Google 搜索

        Args:
            query: 搜索关键词
            num_results: 返回结果数量 (1-10)
            start_index: 起始索引 (用于分页)
            language: 语言限制

        Returns:
            搜索结果字典，失败返回 None
        """
        if not self.api_key or not self.cse_id:
            print("❌ 未配置 Google API 密钥")
            return None

        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "num": min(num_results, 10),  # Google API 限制最多10条
            "start": start_index,
            "lr": language
        }

        try:
            # 使用代理发送请求
            proxies = get_proxies()
            with httpx.Client(proxies=proxies, timeout=10.0) as client:
                response = client.get(
                    self.base_url,
                    params=params
                )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ 搜索成功: 找到约 {data.get('searchInformation', {}).get('totalResults', 'N/A')} 条结果")
                return data
            else:
                print(f"❌ 搜索失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return None

        except httpx.ProxyError:
            print("❌ 代理错误: 请检查代理配置")
            return None
        except httpx.TimeoutException:
            print("❌ 请求超时: 网络连接较慢")
            return None
        except Exception as e:
            print(f"❌ 搜索异常: {type(e).__name__} - {str(e)}")
            return None

    def extract_results(self, search_data: Dict) -> List[Dict]:
        """
        从搜索结果中提取有用信息

        Args:
            search_data: search() 返回的数据

        Returns:
            结果列表，每个结果包含标题、链接、摘要等
        """
        if not search_data:
            return []

        items = search_data.get("items", [])
        results = []

        for item in items:
            result = {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "displayLink": item.get("displayLink", "")
            }
            results.append(result)

        return results


def search_pnd_medical(query: str) -> List[Dict]:
    """
    搜索围产期抑郁相关的医学信息

    Args:
        query: 搜索关键词

    Returns:
        搜索结果列表
    """
    tool = GoogleSearchTool()

    # 添加医学相关关键词提高搜索质量
    medical_query = f"{query} 围产期抑郁 医学 指南"

    search_data = tool.search(medical_query)
    results = tool.extract_results(search_data)

    return results


def search_with_ai(prompt: str) -> str:
    """
    调用阿里百炼AI生成回复（阻塞式）

    Args:
        prompt: 用户输入的提示文本

    Returns:
        AI生成的回复文本
    """
    # 动态导入以避免模块路径问题
    # core 模块已在文件顶部导入

    if not settings.AI_TEXT_KEY:
        return "抱歉，AI服务未配置。请联系管理员配置AI_TEXT_KEY。"

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {settings.AI_TEXT_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": settings.AI_TEXT_MODEL,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "max_tokens": 2000,
            "temperature": 0.7
        }
    }

    try:
        # 阿里百炼AI是国内服务，不需要代理
        print(f"📡 正在调用 AI API...")
        print(f"   URL: {url}")
        print(f"   模型: {settings.AI_TEXT_MODEL}")

        # 不使用代理，直接连接
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                url,
                headers=headers,
                json=body
            )

        print(f"📊 HTTP 状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # 尝试多种可能的响应格式
            # 格式1: 阿里百炼新格式 (output.choices[0].message.content)
            if "output" in data and "choices" in data["output"] and len(data["output"]["choices"]) > 0:
                result = data["output"]["choices"][0]["message"]["content"].strip()
                print(f"✅ AI 回复成功: {result[:50]}...")
                return result

            # 格式2: 阿里百炼标准格式 (output.text)
            elif "output" in data and "text" in data["output"]:
                result = data["output"]["text"].strip()
                print(f"✅ AI 回复成功: {result[:50]}...")
                return result

            # 格式3: OpenAI 兼容格式 (choices.message.content)
            elif "choices" in data and len(data["choices"]) > 0:
                result = data["choices"][0]["message"]["content"].strip()
                print(f"✅ AI 回复成功: {result[:50]}...")
                return result

            # 格式4: 直接返回内容
            elif "content" in data:
                result = data["content"].strip()
                print(f"✅ AI 回复成功: {result[:50]}...")
                return result

            # 格式5: 直接返回 text
            elif "text" in data:
                result = data["text"].strip()
                print(f"✅ AI 回复成功: {result[:50]}...")
                return result

            else:
                print(f"⚠️  无法识别的响应格式")
                print(f"   响应键: {list(data.keys())}")
                return f"AI生成回复格式错误。响应数据: {str(data)[:200]}"
        else:
            print(f"❌ AI调用失败: HTTP {response.status_code}")
            print(f"   响应: {response.text[:500]}")
            return f"AI调用失败: HTTP {response.status_code}"

    except Exception as e:
        import traceback
        print(f"❌ AI调用异常: {type(e).__name__} - {str(e)}")
        print(f"   详细错误:\n{traceback.format_exc()}")
        return f"AI调用异常: {str(e)}"


# 示例使用
if __name__ == "__main__":
    print("="*50)
    print("Google 搜索工具测试")
    print("="*50)
    print()

    # 基本搜索
    tool = GoogleSearchTool()

    # 测试1: 搜索围产期抑郁
    print("测试1: 搜索 '围产期抑郁 筛查工具'")
    results = tool.search("围产期抑郁 筛查工具")

    if results:
        items = tool.extract_results(results)
        print(f"\n找到 {len(items)} 条结果:\n")

        for i, item in enumerate(items, 1):
            print(f"{i}. {item['title']}")
            print(f"   链接: {item['link']}")
            print(f"   摘要: {item['snippet'][:100]}...")
            print()

    # 测试2: 搜索 EPDS 量表
    print("\n" + "="*50)
    print("测试2: 搜索 'EPDS 量表 使用指南'")
    print("="*50)
    results = tool.search("EPDS 量表 使用指南")

    if results:
        items = tool.extract_results(results)
        print(f"\n找到 {len(items)} 条结果")

        for i, item in enumerate(items[:3], 1):  # 只显示前3条
            print(f"\n{i}. {item['title']}")
            print(f"   {item['snippet'][:150]}...")
