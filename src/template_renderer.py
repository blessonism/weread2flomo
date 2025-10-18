"""
模板渲染器
"""
from datetime import datetime
from typing import Dict, Optional, List
from .config_manager import config


class TemplateRenderer:
    """模板渲染器"""

    @staticmethod
    def render(
        template: str,
        book_title: str,
        author: str,
        highlight_text: str,
        chapter_name: str = "",
        book_url: str = "",
        note_text: str = "",
        create_time: str = "",
        tags: List[str] = None,
        ai_summary: str = ""
    ) -> str:
        """
        渲染模板

        Args:
            template: 模板字符串
            book_title: 书名
            author: 作者
            highlight_text: 划线内容
            chapter_name: 章节名
            book_url: 书籍链接
            note_text: 笔记内容
            create_time: 创建时间
            tags: 标签列表
            ai_summary: AI 生成的摘要

        Returns:
            渲染后的内容
        """
        # 处理章节信息
        chapter_info = ""
        if chapter_name:
            chapter_info = f"📍 {chapter_name}"

        # 处理 AI 摘要（明确标识为 AI 生成）
        ai_summary_section = ""
        if ai_summary:
            ai_summary_section = f"✨ AI 摘要：{ai_summary}\n"

        # 处理笔记部分
        note_section = ""
        if note_text:
            note_section = f"💭 我的思考：{note_text}\n"

        # 处理时间
        if not create_time:
            create_time = datetime.now().strftime("%Y-%m-%d")

        # 处理标签
        tags_str = " ".join(tags) if tags else ""

        # 替换模板变量
        content = template.format(
            book_title=book_title,
            author=author,
            highlight_text=highlight_text,
            chapter_info=chapter_info,
            book_url=book_url,
            ai_summary_section=ai_summary_section,
            note_section=note_section,
            create_time=create_time,
            tags=tags_str
        )

        # 清理多余的空行
        lines = content.split('\n')
        cleaned_lines = []
        prev_empty = False

        for line in lines:
            is_empty = not line.strip()

            if is_empty:
                if not prev_empty:
                    cleaned_lines.append(line)
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False

        return '\n'.join(cleaned_lines).strip()


class TagGenerator:
    """标签生成器"""

    @staticmethod
    def _clean_book_title(book_title: str) -> str:
        """
        清理书名，用于生成标签
        
        规则：
        1. 移除书名号《》
        2. 只保留括号前的主标题（移除副标题、版本信息等）
        3. 移除空格、逗号、顿号等标点符号
        4. 保留中英文、数字
        
        Args:
            book_title: 原始书名
            
        Returns:
            清理后的书名
            
        Examples:
            "美丽新世界（译文经典）" -> "美丽新世界"
            "原则（Principles）" -> "原则"
            "思考，快与慢" -> "思考快与慢"
            "代码大全 第2版" -> "代码大全第2版"
        """
        # 移除书名号
        clean = book_title.replace('《', '').replace('》', '')
        
        # 只保留括号前的内容（无论中英文括号）
        # 处理中文括号
        if '（' in clean:
            clean = clean.split('（')[0]
        if '(' in clean:
            clean = clean.split('(')[0]
        
        # 移除【】方括号及其内容
        if '【' in clean:
            clean = clean.split('【')[0]
        if '[' in clean:
            clean = clean.split('[')[0]
        
        # 移除常见标点符号
        clean = clean.replace(' ', '').replace('　', '')  # 空格和全角空格
        clean = clean.replace('，', '').replace(',', '')   # 逗号
        clean = clean.replace('、', '')                    # 顿号
        clean = clean.replace('：', '').replace(':', '')   # 冒号
        clean = clean.replace('！', '').replace('!', '')   # 感叹号
        clean = clean.replace('？', '').replace('?', '')   # 问号
        clean = clean.replace('·', '').replace('•', '')   # 间隔号
        
        # 移除首尾空白
        clean = clean.strip()
        
        return clean

    @staticmethod
    def generate_tags(
        book_title: str,
        author: str,
        highlight_text: str,
        category: Optional[str] = None,
        ai_tags: List[str] = None
    ) -> List[str]:
        """
        生成标签列表

        Args:
            book_title: 书名
            author: 作者
            highlight_text: 划线内容
            category: 书籍分类
            ai_tags: AI生成的标签

        Returns:
            标签列表
        """
        tags = []

        # 检查是否启用层级标签
        use_hierarchical = config.get('tags.use_hierarchical_tags', True)

        # 处理书名标签（层级或独立）
        if config.should_add_book_title_tag():
            # 清理书名
            clean_title = TagGenerator._clean_book_title(book_title)
            
            if use_hierarchical:
                # 使用层级标签: #微信读书/书名
                book_tag = f"#微信读书/{clean_title}"
                tags.append(book_tag)
            else:
                # 使用独立标签: #微信读书 #书名
                default_tags = config.get('tags.default', ['#微信读书'])
                tags.extend(default_tags)
                book_tag = f"#{clean_title}"
                tags.append(book_tag)
        else:
            # 不添加书名标签时，只添加默认标签
            default_tags = config.get('tags.default', ['#微信读书'])
            tags.extend(default_tags)

        # 添加分类标签
        if category:
            category_tags = config.get_category_tags(category)
            tags.extend(category_tags)

        # 添加AI标签
        if ai_tags:
            tags.extend(ai_tags)

        # 添加作者标签
        if config.should_add_author_tag():
            author_clean = author.replace(' ', '_')
            author_tag = f"#{author_clean}"
            tags.append(author_tag)

        # 去重并保持顺序
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags


if __name__ == "__main__":
    # 测试模板渲染
    print("=== 模板渲染测试 ===\n")

    renderer = TemplateRenderer()
    tag_generator = TagGenerator()

    # 测试数据
    book_title = "思考，快与慢"
    author = "丹尼尔·卡尼曼"
    highlight = "人们总是高估自己的理性，低估直觉的作用"
    chapter = "第三章：启发法与偏见"

    # 生成标签
    category = config.get_book_category(book_title, author)
    tags = tag_generator.generate_tags(
        book_title=book_title,
        author=author,
        highlight_text=highlight,
        category=category,
        ai_tags=["#认知偏差", "#心理学"]
    )

    print(f"分类: {category}")
    print(f"标签: {tags}\n")

    # 测试简洁模板
    print("=== 简洁模板 ===")
    simple_template = config.get_template('simple')
    content = renderer.render(
        template=simple_template,
        book_title=book_title,
        author=author,
        highlight_text=highlight,
        chapter_name=chapter,
        tags=tags
    )
    print(content)

    print("\n" + "="*50 + "\n")

    # 测试详细模板
    print("=== 详细模板 ===")
    detailed_template = config.get_template('detailed')
    content = renderer.render(
        template=detailed_template,
        book_title=book_title,
        author=author,
        highlight_text=highlight,
        chapter_name=chapter,
        note_text="可以试试用来提高决策质量",
        tags=tags
    )
    print(content)
