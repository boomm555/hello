#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
import json

def fetch_trending_repos(language, since='daily'):
    """
    爬取 GitHub 热门项目
    language: 'python', 'javascript', 或其他语言
    since: 'daily', 'weekly', 'monthly'
    """
    url = 'https://api.github.com/search/repositories'
    
    # 计算时间范围
    if since == 'daily':
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif since == 'weekly':
        date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    query = f'language:{language} stars:>100 created:>{date} sort:stars-desc'
    
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"爬取 {language} 项目失败: {e}")
        return []

def format_repo_info(repo):
    """格式化仓库信息为大白话描述"""
    return {
        'name': repo['name'],
        'url': repo['html_url'],
        'description': repo['description'] or '暂无描述',
        'stars': repo['stargazers_count'],
        'language': repo['language'] or '未知',
        'owner': repo['owner']['login']
    }

def generate_summary():
    """生成总结报告"""
    
    summary = []
    summary.append('# 📊 GitHub 每日热门项目总结\n')
    summary.append(f'📅 更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    summary.append('---\n\n')
    
    # AI/ML 项目
    summary.append('## 🤖 AI/机器学习项目\n\n')
    python_repos = fetch_trending_repos('python', 'daily')
    if python_repos:
        for i, repo in enumerate(python_repos, 1):
            info = format_repo_info(repo)
            summary.append(f'### {i}. {info["name"]} ⭐ {info["stars"]}\n')
            summary.append(f'📍 **开发者**: {info["owner"]}\n')
            summary.append(f'📝 **介绍**: {info["description"]}\n')
            summary.append(f'🔗 **项目链接**: [{info["name"]}]({info["url"]})\n\n')
    else:
        summary.append('暂无新项目\n\n')
    
    # 前端框架项目
    summary.append('## 🎨 前端框架项目\n\n')
    js_repos = fetch_trending_repos('javascript', 'daily')
    if js_repos:
        for i, repo in enumerate(js_repos, 1):
            info = format_repo_info(repo)
            summary.append(f'### {i}. {info["name"]} ⭐ {info["stars"]}\n')
            summary.append(f'📍 **开发者**: {info["owner"]}\n')
            summary.append(f'📝 **介绍**: {info["description"]}\n')
            summary.append(f'🔗 **项目链接**: [{info["name"]}]({info["url"]})\n\n')
    else:
        summary.append('暂无新项目\n\n')
    
    # 全语言热门爆款
    summary.append('## 🌟 全语言热门爆款\n\n')
    summary.append('*这些是最近比较火的全语言项目*\n\n')
    
    url = 'https://api.github.com/search/repositories'
    date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    params = {
        'q': f'stars:>1000 created:>{date}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 3
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        hot_repos = response.json().get('items', [])
        
        if hot_repos:
            for i, repo in enumerate(hot_repos, 1):
                info = format_repo_info(repo)
                summary.append(f'### {i}. {info["name"]} ⭐ {info["stars"]}\n')
                summary.append(f'📍 **开发者**: {info["owner"]}\n')
                summary.append(f'💬 **语言**: {info["language"]}\n')
                summary.append(f'📝 **介绍**: {info["description"]}\n')
                summary.append(f'🔗 **项目链接**: [{info["name"]}]({info["url"]})\n\n')
    except Exception as e:
        summary.append(f'获取热门项目失败: {e}\n\n')
    
    # 总结
    summary.append('---\n\n')
    summary.append('## 💡 小白快速理解\n\n')
    summary.append('- **⭐ 星标数**: 代表项目受欢迎程度，星越多说明越受欢迎\n')
    summary.append('- **AI/ML 项目**: 人工智能和机器学习相关，Python 项目为主\n')
    summary.append('- **前端项目**: 网页和应用界面相关，JavaScript 项目为主\n')
    summary.append('- **爆款项目**: 最近才发布但已经获得大量关注的新项目\n\n')
    summary.append('🔔 下次更新：明天 8:00 AM\n')
    
    return ''.join(summary)

if __name__ == '__main__':
    content = generate_summary()
    
    # 保存为 markdown 文件
    with open('trending_summary.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 总结已生成: trending_summary.md")
    print(content)
