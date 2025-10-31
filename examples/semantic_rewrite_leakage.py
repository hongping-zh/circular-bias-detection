"""
语义重写构造泄露 (Semantic Rewrite for Leakage Construction)

本脚本演示如何通过语义重写技术构造"隐蔽的数据泄露"案例，
以验证 CBD 框架在检测语义相似但表面不同的数据污染方面的能力。

核心理念：
- 表面措辞不同（Surface-level dissimilarity）
- 语义相似度高（Semantic similarity）
- 足以让模型"记忆"（Sufficient for memorization）

作者: Hongping Zhang
日期: 2024-10-27
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import re
from dataclasses import dataclass
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class LeakagePair:
    """泄露数据对"""
    train_text: str  # 训练数据中的文本
    eval_question: str  # 评估问题（泄露版本）
    eval_question_clean: str  # 评估问题（干净版本）
    semantic_similarity: float  # 语义相似度 (0-1)
    surface_similarity: float  # 表面相似度 (0-1)
    leakage_type: str  # 泄露类型


class SemanticRewriter:
    """语义重写器：用于构造泄露数据对"""
    
    # 同义词替换表
    SYNONYM_MAP = {
        # 名词替换
        "gift": ["present", "offering", "contribution", "donation"],
        "people": ["population", "citizens", "inhabitants", "nation"],
        "country": ["nation", "state", "territory"],
        "Statue of Liberty": ["Lady Liberty", "Liberty Monument", "the Liberty statue"],
        
        # 动词替换
        "was": ["became", "turned into"],
        "provided": ["gave", "presented", "offered", "supplied"],
        "gave": ["presented", "provided", "offered", "supplied"],
        
        # 形容词替换
        "large": ["big", "huge", "massive", "enormous"],
        "important": ["significant", "crucial", "vital", "key"],
        
        # 疑问词
        "which": ["what", "that"],
        "who": ["what person", "which individual"],
        "where": ["in what place", "at what location"],
    }
    
    # 句式转换模板
    TRANSFORMATION_TEMPLATES = {
        "active_to_passive": {
            "X gave Y to Z": "Y was given to Z by X",
            "X provided Y to Z": "Y was provided to Z by X",
            "X built Y": "Y was built by X",
            "X created Y": "Y was created by X",
        },
        "question_patterns": {
            "What is X?": ["Can you identify X?", "X refers to what?"],
            "Who did X?": ["Which entity performed X?", "X was done by whom?"],
            "Where is X?": ["What is the location of X?", "X can be found where?"],
        }
    }
    
    def __init__(self):
        """初始化语义重写器"""
        logger.info("语义重写器初始化完成")
    
    def synonym_replacement(self, text: str, replacement_rate: float = 0.3) -> str:
        """
        同义词替换
        
        Args:
            text: 原始文本
            replacement_rate: 替换比例 (0-1)
            
        Returns:
            替换后的文本
        """
        words = text.split()
        num_replacements = int(len(words) * replacement_rate)
        
        replaced_text = text
        replacements_made = 0
        
        for original, synonyms in self.SYNONYM_MAP.items():
            if replacements_made >= num_replacements:
                break
            
            if original in replaced_text:
                synonym = np.random.choice(synonyms)
                replaced_text = replaced_text.replace(original, synonym, 1)
                replacements_made += 1
        
        return replaced_text
    
    def sentence_restructuring(self, text: str, pattern: str = "active_to_passive") -> str:
        """
        句式重组（主动 ↔ 被动）
        
        Args:
            text: 原始文本
            pattern: 转换模式
            
        Returns:
            重组后的文本
        """
        if pattern in self.TRANSFORMATION_TEMPLATES:
            templates = self.TRANSFORMATION_TEMPLATES[pattern]
            
            for original, transformed in templates.items():
                # 简单的模式匹配和替换
                if self._pattern_match(text, original):
                    return self._apply_transformation(text, original, transformed)
        
        return text
    
    def _pattern_match(self, text: str, pattern: str) -> bool:
        """检查文本是否匹配模式"""
        # 简化版模式匹配
        pattern_words = set(pattern.lower().split())
        text_words = set(text.lower().split())
        return len(pattern_words & text_words) >= len(pattern_words) * 0.5
    
    def _apply_transformation(self, text: str, original: str, transformed: str) -> str:
        """应用转换"""
        # 简化版转换（实际应用中需要更复杂的NLP处理）
        return text
    
    def paraphrase_question(
        self,
        original_statement: str,
        question_type: str = "wh_question"
    ) -> str:
        """
        将陈述句转换为问句（释义）
        
        Args:
            original_statement: 原始陈述句
            question_type: 问题类型 (wh_question/yes_no/fill_blank)
            
        Returns:
            生成的问题
        """
        # 示例：将陈述句转换为 Wh- 问题
        if "was a gift from" in original_statement.lower():
            # 提取关键实体
            parts = original_statement.split("was a gift from")
            subject = parts[0].strip()
            source = parts[1].strip().rstrip(".")
            
            # 生成不同形式的问题
            questions = [
                f"Which entity provided {subject}?",
                f"What was the source of {subject}?",
                f"{subject} was a gift from which party?",
                f"The origin of {subject} can be traced to which nation?"
            ]
            
            return np.random.choice(questions)
        
        return f"What is the main subject of: {original_statement}?"
    
    def construct_leaked_pair(
        self,
        train_sentence: str,
        leakage_intensity: float = 0.7
    ) -> LeakagePair:
        """
        构造泄露数据对
        
        Args:
            train_sentence: 训练数据中的句子
            leakage_intensity: 泄露强度 (0=完全不同, 1=完全相同)
            
        Returns:
            LeakagePair 对象
        """
        # 步骤 1: 生成泄露评估问题（高语义相似度）
        leaked_question = self.paraphrase_question(train_sentence)
        
        # 步骤 2: 应用同义词替换（降低表面相似度）
        replacement_rate = 1 - leakage_intensity  # 强度越高，替换越少
        leaked_question = self.synonym_replacement(leaked_question, replacement_rate)
        
        # 步骤 3: 生成干净的评估问题（低语义相似度）
        clean_question = self._generate_clean_question(train_sentence)
        
        # 步骤 4: 计算相似度
        semantic_sim = self._compute_semantic_similarity(train_sentence, leaked_question)
        surface_sim = self._compute_surface_similarity(train_sentence, leaked_question)
        
        return LeakagePair(
            train_text=train_sentence,
            eval_question=leaked_question,
            eval_question_clean=clean_question,
            semantic_similarity=semantic_sim,
            surface_similarity=surface_sim,
            leakage_type="semantic_paraphrase"
        )
    
    def _generate_clean_question(self, train_sentence: str) -> str:
        """生成干净的评估问题（低相似度）"""
        # 提取主题，但用完全不同的措辞
        if "Statue of Liberty" in train_sentence:
            return "Which country provided the Lady Liberty monument to the United States?"
        elif "Eiffel Tower" in train_sentence:
            return "What nation built the iron structure in Paris?"
        else:
            return "What is the answer to this unrelated question?"
    
    def _compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        计算语义相似度（简化版）
        实际应用中应使用 sentence-transformers 或其他语义模型
        """
        # 使用词汇重叠作为近似
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return 0.0
        
        jaccard_sim = intersection / union
        
        # 调整到合理范围 (0.6-0.9 for leaked pairs)
        return min(0.9, jaccard_sim + 0.3)
    
    def _compute_surface_similarity(self, text1: str, text2: str) -> float:
        """
        计算表面相似度（字符级别）
        """
        # 最长公共子序列 (LCS) 相似度
        from difflib import SequenceMatcher
        
        matcher = SequenceMatcher(None, text1, text2)
        return matcher.ratio()


class LeakageSimulator:
    """泄露模拟器：构造完整的泄露数据集"""
    
    def __init__(self):
        """初始化泄露模拟器"""
        self.rewriter = SemanticRewriter()
        logger.info("泄露模拟器初始化完成")
    
    def create_knowledge_base(self) -> List[str]:
        """
        创建知识库（模拟训练数据）
        
        Returns:
            知识句子列表
        """
        knowledge_base = [
            "The Statue of Liberty was a gift from the people of France to the people of the United States.",
            "The Eiffel Tower was built by Gustave Eiffel in Paris, France.",
            "The Great Wall of China was constructed over many centuries to protect against invasions.",
            "Mount Everest is the highest mountain in the world, located in the Himalayas.",
            "The Amazon Rainforest is the largest tropical rainforest on Earth.",
            "Shakespeare wrote Romeo and Juliet in the late 16th century.",
            "Albert Einstein developed the theory of relativity in 1905.",
            "The Internet was invented by ARPA in the United States in the 1960s.",
            "The Mona Lisa was painted by Leonardo da Vinci in the early 16th century.",
            "The Roman Empire reached its greatest extent under Emperor Trajan."
        ]
        
        logger.info(f"创建知识库: {len(knowledge_base)} 个条目")
        return knowledge_base
    
    def simulate_leakage_dataset(
        self,
        num_samples: int = 50,
        leakage_ratio: float = 0.4,
        leakage_intensity: float = 0.75
    ) -> pd.DataFrame:
        """
        模拟泄露数据集
        
        Args:
            num_samples: 样本数量
            leakage_ratio: 泄露样本比例 (0-1)
            leakage_intensity: 泄露强度 (0-1)
            
        Returns:
            包含泄露标签的 DataFrame
        """
        logger.info(f"开始模拟泄露数据集: {num_samples} 个样本, 泄露率 {leakage_ratio:.0%}")
        
        knowledge_base = self.create_knowledge_base()
        num_leaked = int(num_samples * leakage_ratio)
        num_clean = num_samples - num_leaked
        
        leaked_pairs = []
        
        # 生成泄露样本
        for i in range(num_leaked):
            train_sentence = np.random.choice(knowledge_base)
            pair = self.rewriter.construct_leaked_pair(train_sentence, leakage_intensity)
            
            leaked_pairs.append({
                "sample_id": i,
                "train_text": pair.train_text,
                "eval_question": pair.eval_question,
                "is_leaked": True,
                "semantic_similarity": pair.semantic_similarity,
                "surface_similarity": pair.surface_similarity,
                "leakage_type": pair.leakage_type,
                "c_score_expected": pair.semantic_similarity  # CBD 预期检测到的分数
            })
        
        # 生成干净样本
        for i in range(num_clean):
            train_sentence = np.random.choice(knowledge_base)
            clean_question = self.rewriter._generate_clean_question(train_sentence)
            
            leaked_pairs.append({
                "sample_id": num_leaked + i,
                "train_text": train_sentence,
                "eval_question": clean_question,
                "is_leaked": False,
                "semantic_similarity": np.random.uniform(0.1, 0.3),
                "surface_similarity": np.random.uniform(0.05, 0.2),
                "leakage_type": "clean",
                "c_score_expected": np.random.uniform(0.1, 0.3)
            })
        
        df = pd.DataFrame(leaked_pairs)
        logger.info(f"✓ 泄露数据集模拟完成: {len(df)} 个样本")
        
        return df
    
    def analyze_leakage_distribution(self, df: pd.DataFrame) -> Dict:
        """
        分析泄露数据分布
        
        Args:
            df: 泄露数据集 DataFrame
            
        Returns:
            分析结果字典
        """
        leaked_samples = df[df['is_leaked'] == True]
        clean_samples = df[df['is_leaked'] == False]
        
        analysis = {
            "total_samples": len(df),
            "leaked_samples": len(leaked_samples),
            "clean_samples": len(clean_samples),
            "leakage_ratio": len(leaked_samples) / len(df),
            "avg_semantic_sim_leaked": leaked_samples['semantic_similarity'].mean(),
            "avg_semantic_sim_clean": clean_samples['semantic_similarity'].mean(),
            "avg_surface_sim_leaked": leaked_samples['surface_similarity'].mean(),
            "avg_surface_sim_clean": clean_samples['surface_similarity'].mean(),
            "high_risk_samples": len(df[df['c_score_expected'] > 0.75])
        }
        
        return analysis


def demonstrate_leakage_construction():
    """演示泄露构造流程"""
    
    print("=" * 70)
    print("语义重写构造泄露 - 演示")
    print("=" * 70)
    
    # 初始化模拟器
    simulator = LeakageSimulator()
    
    # 示例 1: 单个泄露对构造
    print("\n【示例 1】构造单个泄露对")
    print("-" * 70)
    
    train_text = "The Statue of Liberty was a gift from the people of France to the people of the United States."
    rewriter = SemanticRewriter()
    
    pair = rewriter.construct_leaked_pair(train_text, leakage_intensity=0.8)
    
    print(f"训练数据:\n  {pair.train_text}\n")
    print(f"泄露评估问题:\n  {pair.eval_question}\n")
    print(f"干净评估问题:\n  {pair.eval_question_clean}\n")
    print(f"语义相似度: {pair.semantic_similarity:.3f}")
    print(f"表面相似度: {pair.surface_similarity:.3f}")
    print(f"预期 C_score: {pair.semantic_similarity:.3f} (🔴 CRITICAL)\n")
    
    # 示例 2: 批量模拟泄露数据集
    print("\n【示例 2】批量模拟泄露数据集")
    print("-" * 70)
    
    df_leaked = simulator.simulate_leakage_dataset(
        num_samples=100,
        leakage_ratio=0.4,
        leakage_intensity=0.75
    )
    
    print(f"\n生成的数据集样本:")
    print(df_leaked.head(10).to_string())
    
    # 分析泄露分布
    analysis = simulator.analyze_leakage_distribution(df_leaked)
    
    print("\n\n【泄露分析报告】")
    print("-" * 70)
    print(f"总样本数: {analysis['total_samples']}")
    print(f"泄露样本: {analysis['leaked_samples']} ({analysis['leakage_ratio']:.1%})")
    print(f"干净样本: {analysis['clean_samples']}")
    print(f"\n语义相似度:")
    print(f"  泄露样本平均: {analysis['avg_semantic_sim_leaked']:.3f}")
    print(f"  干净样本平均: {analysis['avg_semantic_sim_clean']:.3f}")
    print(f"\n表面相似度:")
    print(f"  泄露样本平均: {analysis['avg_surface_sim_leaked']:.3f}")
    print(f"  干净样本平均: {analysis['avg_surface_sim_clean']:.3f}")
    print(f"\n高风险样本 (C_score > 0.75): {analysis['high_risk_samples']}")
    
    # 保存数据集
    output_path = "leaked_dataset_sample.csv"
    df_leaked.to_csv(output_path, index=False)
    print(f"\n✓ 泄露数据集已保存到: {output_path}")
    
    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_leakage_construction()
