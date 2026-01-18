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

        # 打印调用日志
        print("=" * 60)
        print("🔍 Google 搜索工具调用")
        print("=" * 60)
        print(f"📌 搜索关键词: {query}")
        print(f"📊 返回结果数: {min(num_results, 10)}")
        print(f"📍 起始索引: {start_index}")
        print(f"🌐 语言限制: {language}")
        print(f"🔗 API URL: {self.base_url}")

        try:
            # 使用代理发送请求
            proxies = get_proxies()
            if proxies:
                print(f"🔧 使用代理: {proxies.get('http://', '直接连接')}")
            else:
                print("🔧 代理配置: 直接连接（无代理）")

            print("⏳ 正在发送请求...")
            with httpx.Client(proxies=proxies, timeout=10.0) as client:
                response = client.get(
                    self.base_url,
                    params=params
                )

            print(f"📡 HTTP 状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                total_results = data.get('searchInformation', {}).get('totalResults', 'N/A')
                search_time = data.get('searchInformation', {}).get('searchTime', 'N/A')

                print(f"✅ 搜索成功")
                print(f"   📈 找到约 {total_results} 条结果")
                print(f"   ⏱️  搜索耗时: {search_time} 秒")

                # 打印前3个结果的标题
                items = data.get("items", [])
                if items:
                    print(f"   📋 前 {min(3, len(items))} 个结果:")
                    for i, item in enumerate(items[:3], 1):
                        print(f"      {i}. {item.get('title', 'N/A')}")

                print("=" * 60)
                return data
            else:
                print(f"❌ 搜索失败")
                print(f"   HTTP 状态码: {response.status_code}")
                print(f"   响应内容: {response.text[:200]}")
                print("=" * 60)
                return None

        except httpx.ProxyError:
            print("❌ 代理错误: 请检查代理配置")
            print("=" * 60)
            return None
        except httpx.TimeoutException:
            print("❌ 请求超时: 网络连接较慢")
            print("=" * 60)
            return None
        except Exception as e:
            print(f"❌ 搜索异常: {type(e).__name__}")
            print(f"   错误信息: {str(e)}")
            print("=" * 60)
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


def search_with_ai(prompt: str, max_retries: int = 2) -> str:
    """
    调用阿里百炼AI生成回复（阻塞式）

    Args:
        prompt: 用户输入的提示文本
        max_retries: 最大重试次数，默认为2次

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

    # 重试逻辑
    for attempt in range(max_retries + 1):
        try:
            # 阿里百炼AI是国内服务，不需要代理
            if attempt > 0:
                print(f"📡 正在重试第 {attempt} 次...")
            else:
                print(f"📡 正在调用 AI API...")
            print(f"   URL: {url}")
            print(f"   模型: {settings.AI_TEXT_MODEL}")

            # 不使用代理，直接连接
            # 增加超时时间到 360 秒（6分钟），因为评估 prompt 可能很长
            timeout_config = httpx.Timeout(
                connect=10.0,      # 连接超时 10 秒
                read=360.0,        # 读取超时 360 秒（6分钟）
                write=30.0,        # 写入超时 30 秒
                pool=30.0          # 连接池超时 30 秒
            )

            with httpx.Client(timeout=timeout_config) as client:
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

        except httpx.TimeoutException as e:
            # 如果是超时错误，且还有重试次数，则重试
            if attempt < max_retries:
                print(f"⏱️  AI调用超时，准备重试 ({attempt + 1}/{max_retries})...")
                continue
            else:
                import traceback
                print(f"❌ AI调用超时（已重试 {max_retries} 次）: {type(e).__name__} - {str(e)}")
                print(f"   详细错误:\n{traceback.format_exc()}")
                raise  # 重新抛出异常，让调用方处理

        except Exception as e:
            # 其他异常也重试
            if attempt < max_retries:
                print(f"⚠️  AI调用异常，准备重试 ({attempt + 1}/{max_retries}): {type(e).__name__} - {str(e)}")
                continue
            else:
                import traceback
                print(f"❌ AI调用异常（已重试 {max_retries} 次）: {type(e).__name__} - {str(e)}")
                print(f"   详细错误:\n{traceback.format_exc()}")
                raise  # 重新抛出异常，让调用方处理


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
