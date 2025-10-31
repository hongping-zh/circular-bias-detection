"""
Hugging Face 数据收集脚本
用于下载和预处理高风险评估数据集，以检测训练-评估交叉污染

作者: Hongping Zhang
日期: 2024-10-27
"""

import os
import json
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datasets import load_dataset, list_datasets
from tqdm import tqdm
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HuggingFaceDataCollector:
    """Hugging Face 数据集收集器"""
    
    # 优先级数据集配置
    PRIORITY_DATASETS = {
        "qa": [
            {"id": "squad_v2", "name": "SQuAD v2.0", "risk": "high", "task": "question_answering"},
            {"id": "natural_questions", "name": "Natural Questions", "risk": "high", "task": "question_answering"},
            {"id": "trivia_qa", "name": "TriviaQA", "risk": "high", "task": "question_answering", "config": "unfiltered"},
        ],
        "summarization": [
            {"id": "cnn_dailymail", "name": "CNN/DailyMail", "risk": "high", "task": "summarization", "config": "3.0.0"},
            {"id": "xsum", "name": "XSum", "risk": "high", "task": "summarization"},
        ],
        "translation": [
            {"id": "wmt14", "name": "WMT14", "risk": "medium", "task": "translation", "config": "de-en"},
        ],
        "training_corpus": [
            {"id": "wikipedia", "name": "Wikipedia", "risk": "high", "task": "corpus", "config": "20220301.en"},
        ]
    }
    
    def __init__(self, output_dir: str = "./collected_data"):
        """
        初始化数据收集器
        
        Args:
            output_dir: 输出目录路径
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "metadata"), exist_ok=True)
        logger.info(f"数据收集器初始化完成，输出目录: {output_dir}")
    
    def search_datasets_by_keyword(self, keywords: List[str], limit: int = 50) -> List[str]:
        """
        根据关键词搜索 Hugging Face 数据集
        
        Args:
            keywords: 搜索关键词列表
            limit: 返回结果数量限制
            
        Returns:
            匹配的数据集ID列表
        """
        logger.info(f"搜索关键词: {keywords}")
        all_datasets = list_datasets()
        
        matching = []
        for dataset_id in all_datasets:
            dataset_lower = dataset_id.lower()
            if any(keyword.lower() in dataset_lower for keyword in keywords):
                matching.append(dataset_id)
                if len(matching) >= limit:
                    break
        
        logger.info(f"找到 {len(matching)} 个匹配的数据集")
        return matching
    
    def download_dataset(
        self,
        dataset_id: str,
        config: Optional[str] = None,
        split: str = "train",
        max_samples: Optional[int] = None,
        cache_dir: Optional[str] = None
    ) -> pd.DataFrame:
        """
        下载并加载 Hugging Face 数据集
        
        Args:
            dataset_id: 数据集ID
            config: 配置名称（如果需要）
            split: 数据集分割 (train/validation/test)
            max_samples: 最大采样数量
            cache_dir: 缓存目录
            
        Returns:
            pandas DataFrame 格式的数据集
        """
        try:
            logger.info(f"开始下载数据集: {dataset_id}")
            
            # 加载数据集
            if config:
                dataset = load_dataset(dataset_id, config, cache_dir=cache_dir)
            else:
                dataset = load_dataset(dataset_id, cache_dir=cache_dir)
            
            # 获取指定分割
            if split not in dataset:
                logger.warning(f"分割 '{split}' 不存在，使用第一个可用分割")
                split = list(dataset.keys())[0]
            
            data = dataset[split]
            
            # 采样
            if max_samples and len(data) > max_samples:
                logger.info(f"采样 {max_samples} 条数据（总共 {len(data)} 条）")
                data = data.shuffle(seed=42).select(range(max_samples))
            
            # 转换为 DataFrame
            df = pd.DataFrame(data)
            logger.info(f"成功下载 {len(df)} 条数据")
            
            return df
            
        except Exception as e:
            logger.error(f"下载数据集失败: {dataset_id}, 错误: {str(e)}")
            return pd.DataFrame()
    
    def extract_qa_pairs(
        self,
        dataset_df: pd.DataFrame,
        context_col: str = "context",
        question_col: str = "question",
        answer_col: str = "answers"
    ) -> List[Dict]:
        """
        从问答数据集提取问答对
        
        Args:
            dataset_df: 数据集 DataFrame
            context_col: 上下文列名
            question_col: 问题列名
            answer_col: 答案列名
            
        Returns:
            问答对列表
        """
        qa_pairs = []
        
        for idx, row in dataset_df.iterrows():
            try:
                context = row.get(context_col, "")
                question = row.get(question_col, "")
                answers = row.get(answer_col, [])
                
                # 处理不同的答案格式
                if isinstance(answers, dict):
                    answer_texts = answers.get("text", [])
                elif isinstance(answers, list):
                    answer_texts = answers
                else:
                    answer_texts = [str(answers)]
                
                qa_pairs.append({
                    "id": idx,
                    "context": context,
                    "question": question,
                    "answers": answer_texts,
                    "answer_text": answer_texts[0] if answer_texts else ""
                })
            except Exception as e:
                logger.warning(f"处理第 {idx} 行时出错: {str(e)}")
                continue
        
        logger.info(f"提取了 {len(qa_pairs)} 个问答对")
        return qa_pairs
    
    def extract_summarization_pairs(
        self,
        dataset_df: pd.DataFrame,
        article_col: str = "article",
        summary_col: str = "highlights"
    ) -> List[Dict]:
        """
        从摘要数据集提取文章-摘要对
        
        Args:
            dataset_df: 数据集 DataFrame
            article_col: 文章列名
            summary_col: 摘要列名
            
        Returns:
            文章-摘要对列表
        """
        pairs = []
        
        for idx, row in dataset_df.iterrows():
            try:
                article = row.get(article_col, "")
                summary = row.get(summary_col, "")
                
                pairs.append({
                    "id": idx,
                    "article": article,
                    "summary": summary,
                    "article_length": len(article.split()),
                    "summary_length": len(summary.split())
                })
            except Exception as e:
                logger.warning(f"处理第 {idx} 行时出错: {str(e)}")
                continue
        
        logger.info(f"提取了 {len(pairs)} 个摘要对")
        return pairs
    
    def sample_wikipedia_corpus(
        self,
        max_docs: int = 10000,
        categories: Optional[List[str]] = None,
        min_length: int = 500
    ) -> pd.DataFrame:
        """
        采样 Wikipedia 语料作为训练集代表
        
        Args:
            max_docs: 最大文档数量
            categories: 类别过滤（如果支持）
            min_length: 最小文档长度（字符数）
            
        Returns:
            采样的 Wikipedia 文档 DataFrame
        """
        logger.info(f"开始采样 Wikipedia 语料，目标 {max_docs} 个文档")
        
        try:
            # 加载 Wikipedia 数据集（使用流式加载以节省内存）
            dataset = load_dataset("wikipedia", "20220301.en", split="train", streaming=True)
            
            sampled_docs = []
            for i, item in enumerate(tqdm(dataset, desc="采样 Wikipedia", total=max_docs)):
                if len(sampled_docs) >= max_docs:
                    break
                
                text = item.get("text", "")
                if len(text) >= min_length:
                    sampled_docs.append({
                        "id": item.get("id", f"wiki_{i}"),
                        "title": item.get("title", ""),
                        "text": text,
                        "length": len(text),
                        "word_count": len(text.split())
                    })
            
            df = pd.DataFrame(sampled_docs)
            logger.info(f"成功采样 {len(df)} 个 Wikipedia 文档")
            return df
            
        except Exception as e:
            logger.error(f"采样 Wikipedia 失败: {str(e)}")
            return pd.DataFrame()
    
    def create_dataset_inventory(self) -> pd.DataFrame:
        """
        创建数据集清单
        
        Returns:
            数据集清单 DataFrame
        """
        inventory = []
        
        for task_type, datasets in self.PRIORITY_DATASETS.items():
            for ds in datasets:
                inventory.append({
                    "dataset_id": ds["id"],
                    "dataset_name": ds["name"],
                    "task_type": task_type,
                    "risk_level": ds["risk"],
                    "config": ds.get("config", "default"),
                    "status": "pending"
                })
        
        df = pd.DataFrame(inventory)
        
        # 保存到文件
        output_path = os.path.join(self.output_dir, "metadata", "dataset_inventory.csv")
        df.to_csv(output_path, index=False)
        logger.info(f"数据集清单已保存到: {output_path}")
        
        return df
    
    def collect_all_priority_datasets(
        self,
        max_samples_per_dataset: int = 1000,
        save_format: str = "csv"
    ) -> Dict[str, pd.DataFrame]:
        """
        收集所有优先级数据集
        
        Args:
            max_samples_per_dataset: 每个数据集的最大采样数
            save_format: 保存格式 (csv/json/parquet)
            
        Returns:
            数据集字典 {dataset_id: DataFrame}
        """
        logger.info("开始收集所有优先级数据集")
        collected = {}
        
        for task_type, datasets in self.PRIORITY_DATASETS.items():
            logger.info(f"\n处理任务类型: {task_type}")
            
            for ds_config in datasets:
                dataset_id = ds_config["id"]
                config = ds_config.get("config")
                
                try:
                    # 下载数据集
                    df = self.download_dataset(
                        dataset_id=dataset_id,
                        config=config,
                        split="train",
                        max_samples=max_samples_per_dataset
                    )
                    
                    if not df.empty:
                        collected[dataset_id] = df
                        
                        # 保存数据
                        output_path = os.path.join(
                            self.output_dir,
                            f"{dataset_id}_{task_type}.{save_format}"
                        )
                        
                        if save_format == "csv":
                            df.to_csv(output_path, index=False)
                        elif save_format == "json":
                            df.to_json(output_path, orient="records", indent=2)
                        elif save_format == "parquet":
                            df.to_parquet(output_path, index=False)
                        
                        logger.info(f"✓ 已保存: {output_path}")
                    
                except Exception as e:
                    logger.error(f"✗ 收集失败: {dataset_id}, 错误: {str(e)}")
                    continue
        
        logger.info(f"\n收集完成！共收集 {len(collected)} 个数据集")
        return collected
    
    def generate_collection_report(self, collected_datasets: Dict[str, pd.DataFrame]) -> str:
        """
        生成数据收集报告
        
        Args:
            collected_datasets: 已收集的数据集字典
            
        Returns:
            报告文本
        """
        report = []
        report.append("=" * 60)
        report.append("数据收集报告")
        report.append("=" * 60)
        report.append(f"\n总计收集数据集: {len(collected_datasets)} 个\n")
        
        for dataset_id, df in collected_datasets.items():
            report.append(f"数据集: {dataset_id}")
            report.append(f"  - 样本数: {len(df)}")
            report.append(f"  - 列数: {len(df.columns)}")
            report.append(f"  - 列名: {', '.join(df.columns.tolist())}")
            report.append(f"  - 内存占用: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            report.append("")
        
        report.append("=" * 60)
        
        report_text = "\n".join(report)
        
        # 保存报告
        report_path = os.path.join(self.output_dir, "metadata", "collection_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        
        logger.info(f"收集报告已保存到: {report_path}")
        return report_text


def main():
    """主函数：演示数据收集流程"""
    
    # 初始化收集器
    collector = HuggingFaceDataCollector(output_dir="./collected_data")
    
    # 步骤 1: 创建数据集清单
    print("\n步骤 1: 创建数据集清单...")
    inventory = collector.create_dataset_inventory()
    print(inventory)
    
    # 步骤 2: 搜索相关数据集
    print("\n步骤 2: 搜索相关数据集...")
    qa_datasets = collector.search_datasets_by_keyword(
        keywords=["question", "answering", "qa"],
        limit=10
    )
    print(f"找到问答数据集: {qa_datasets[:5]}")
    
    # 步骤 3: 收集优先级数据集（演示模式，只下载少量样本）
    print("\n步骤 3: 收集优先级数据集...")
    collected = collector.collect_all_priority_datasets(
        max_samples_per_dataset=100,  # 演示模式：每个数据集只下载 100 个样本
        save_format="csv"
    )
    
    # 步骤 4: 生成收集报告
    print("\n步骤 4: 生成收集报告...")
    report = collector.generate_collection_report(collected)
    print(report)
    
    print("\n✅ 数据收集完成！")


if __name__ == "__main__":
    main()
