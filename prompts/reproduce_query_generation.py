#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetAll Query Generation Reproduction Script

Uses resilient_llm_client.py to reproduce query generation based on 
MeetBench-XL paper methodology (arXiv:2602.03285).

Usage:
    python reproduce_query_generation.py [--class C02] [--language en] [--num-queries 1]
"""

import argparse
import json
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resilient_llm_client import ResilientLLMClient
from query_prompts import (
    format_query_prompt,
    format_answer_prompt,
    format_evaluation_prompt,
    COMPLEXITY_CLASSES,
)

# Sample meeting transcript for demonstration (CHiME-6 style English meeting)
SAMPLE_ENGLISH_CONTEXT = """
[00:01:23] Moderator: Good morning everyone, let's start our weekly product review meeting.
[00:01:45] Sarah: Thanks. I'd like to begin with an update on the authentication module migration.
[00:02:10] Mike: Yes, I've been working on that. We've completed 80% of the OAuth2 endpoint migrations.
[00:02:35] Lisa: That's good progress. But we need to ensure compliance with GDPR Article 32 before going live.
[00:03:02] John: Right, I'll coordinate with the legal team on that. The deadline is next Friday.
[00:03:28] Sarah: Speaking of deadlines - what's the status of the Q3 sprint deliverables?
[00:03:55] Mike: We're on track for most items except the real-time notification feature, which depends on the WebSocket upgrade.
[00:04:22] Lisa: The WebSocket upgrade is blocked by infrastructure team's server maintenance window.
[00:04:48] John: I spoke with them yesterday. They can give us a slot this Thursday night.
[00:05:15] Sarah: Perfect. So if we push hard, we should hit the Q3 target.
[00:05:42] Mike: One concern though - load testing showed latency spikes when we exceed 10k concurrent connections.
[00:06:08] Lisa: That's a critical issue for our Black Friday launch preparation.
[00:06:35] John: Let's schedule a deep-dive session tomorrow to address this specifically.
"""

# Sample Chinese meeting context (AISHELL-4 style)
SAMPLE_CHINESE_CONTEXT = """
[00:01:15] 主持人：各位早上好，我们开始本周的项目评审会议。
[00:01:42] 李明：我先汇报一下用户认证模块的迁移进度。
[00:02:08] 王强：是的，我一直在跟进这个工作。OAuth2接口的迁移已经完成了80%。
[00:02:33] 张丽：进展不错。但上线前需要确保符合GDPR第32条的要求。
[00:03:01] 陈总：好的，我会协调法务部门处理这个事情。截止时间是下周五。
[00:03:27] 李明：说到截止时间，Q3冲刺的交付物状态怎么样？
[00:03:54] 王强：大部分都在按计划推进，除了实时通知功能，它依赖于WebSocket升级。
[00:04:21] 张丽：WebSocket升级被基础设施团队的服务器维护窗口阻塞了。
[00:04:47] 陈总：我昨天和他们沟通过了。他们可以在周四晚上给我们一个维护窗口。
[00:05:14] 李明：太好了。如果我们加把劲，应该能达到Q3的目标。
[00:05:41] 王强：不过有一个问题——负载测试显示超过1万并发连接时会出现延迟峰值。
[00:06:08] 张丽：这对我们的黑色星期五上线准备来说是个关键问题。
[00:06:35] 陈总：我们明天安排一个深入讨论会专门解决这个问题。
"""


def generate_query(client, complexity_class, language="en", num_queries=1):
    """
    Generate queries using LLM API based on complexity class.
    
    Args:
        client: ResilientLLMClient instance
        complexity_class: C01-C13 class identifier
        language: "en" or "zh"
        num_queries: Number of queries to generate
        
    Returns:
        Tuple of (generated_text, metrics)
    """
    # Select appropriate context
    context = SAMPLE_ENGLISH_CONTEXT if language == "en" else SAMPLE_CHINESE_CONTEXT
    
    # Format prompt
    prompt = format_query_prompt(
        context=context,
        complexity_class=complexity_class,
        num_queries=num_queries,
        language=language
    )
    
    print(f"\n{'='*60}")
    print(f"Generating Query | Class: {complexity_class} | Language: {language}")
    print(f"{'='*60}")
    
    # Call LLM API
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response, metrics = client.chat(messages=messages)
        
        # Extract generated text
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            return content.strip(), metrics
        else:
            return None, metrics
            
    except Exception as e:
        print(f"Error generating query: {e}")
        return None, None


def generate_answer(client, question, language="en"):
    """
    Generate answer for a query using LLM API.
    
    Args:
        client: ResilientLLMClient instance
        question: User question to answer
        language: "en" or "zh"
        
    Returns:
        Tuple of (answer_text, metrics)
    """
    # Select appropriate context
    context = SAMPLE_ENGLISH_CONTEXT if language == "en" else SAMPLE_CHINESE_CONTEXT
    
    # Format prompt
    prompt = format_answer_prompt(
        context=context,
        question=question,
        language=language
    )
    
    print(f"\n{'='*60}")
    print(f"Generating Answer | Language: {language}")
    print(f"Question: {question[:100]}...")
    print(f"{'='*60}")
    
    # Call LLM API
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response, metrics = client.chat(messages=messages)
        
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            return content.strip(), metrics
        else:
            return None, metrics
            
    except Exception as e:
        print(f"Error generating answer: {e}")
        return None, None


def evaluate_response(client, question, reference_answer, model_response):
    """
    Evaluate model response using MeetBench evaluation protocol.
    
    Args:
        client: ResilientLLMClient instance
        question: Original user question
        reference_answer: Gold/ground truth answer
        model_response: Model response to evaluate
        
    Returns:
        Evaluation result string
    """
    prompt = format_evaluation_prompt(
        question=question,
        reference_answer=reference_answer,
        model_response=model_response
    )
    
    print(f"\n{'='*60}")
    print("Evaluating Response with MeetBench Protocol")
    print(f"{'='*60}")
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response, metrics = client.chat(messages=messages)
        
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            return content.strip(), metrics
        else:
            return None, metrics
            
    except Exception as e:
        print(f"Error evaluating: {e}")
        return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Reproduce MeetAll query generation with LLM API"
    )
    parser.add_argument(
        "--class", 
        dest="complexity_class",
        default="C02",
        help="Complexity class (C01-C13), default: C02"
    )
    parser.add_argument(
        "--language",
        default="en",
        choices=["en", "zh"],
        help="Language: en (English) or zh (Chinese), default: en"
    )
    parser.add_argument(
        "--num-queries",
        type=int,
        default=1,
        help="Number of queries to generate, default: 1"
    )
    parser.add_argument(
        "--generate-answer",
        action="store_true",
        help="Also generate answer for the produced query"
    )
    parser.add_argument(
        "--list-classes",
        action="store_true",
        help="List all available complexity classes"
    )
    
    args = parser.parse_args()
    
    # List classes if requested
    if args.list_classes:
        print("\nAvailable Complexity Classes:")
        print("-" * 50)
        for class_id, class_def in COMPLEXITY_CLASSES.items():
            print(f"{class_id}: {class_def['name']}")
            print(f"   CL={class_def['cl_level']}, CD={class_def['cd_level']}, "
                  f"DK={class_def['dk_level']}, TE={class_def['te_level']}")
        return
    
    # Validate class
    if args.complexity_class not in COMPLEXITY_CLASSES:
        print(f"Error: Unknown class '{args.complexity_class}'")
        print("Use --list-classes to see all available classes.")
        return
    
    # Initialize LLM client
    print("Initializing LLM client (Hunyuan/Qwen failover)...")
    try:
        client = ResilientLLMClient(primary="hunyuan")
        print("Client initialized successfully!")
    except Exception as e:
        print(f"Error initializing client: {e}")
        return
    
    # Generate query
    query_result, gen_metrics = generate_query(
        client=client,
        complexity_class=args.complexity_class,
        language=args.language,
        num_queries=args.num_queries
    )
    
    if query_result:
        print(f"\n✅ Generated Query:\n{query_result}")
        print(f"\n📊 Metrics: Provider={gen_metrics.provider}, "
              f"Latency={gen_metrics.latency_s:.2f}s, "
              f"Attempt={gen_metrics.attempt}")
        
        # Optionally generate answer
        if args.generate_answer:
            answer_result, ans_metrics = generate_answer(
                client=client,
                question=query_result,
                language=args.language
            )
            
            if answer_result:
                print(f"\n✅ Generated Answer:\n{answer_result}")
                print(f"\n📊 Metrics: Provider={ans_metrics.provider}, "
                      f"Latency={ans_metrics.latency_s:.2f}s")
                
                # Optional: Evaluate the answer against itself (demo purposes)
                eval_result, _ = evaluate_response(
                    client=client,
                    question=query_result,
                    reference_answer="[Sample Reference]",
                    model_response=answer_result
                )
                
                if eval_result:
                    print(f"\n📋 MeetBench Evaluation Result:\n{eval_result}")
    else:
        print("\n❌ Failed to generate query")
    
    # Print final stats
    print(f"\n{'='*60}")
    print(f"Session Stats: {client.get_stats_summary()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
