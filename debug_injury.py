import requests
from bs4 import BeautifulSoup

# 球队名称映射字典
team_name_map = {
    '湖人': '洛杉矶湖人',
    '快船': '洛杉矶快船',
    '勇士': '金州勇士',
    '火箭': '休斯顿火箭',
    '独行侠': '达拉斯独行侠',
    '掘金': '丹佛掘金',
    '活塞': '底特律活塞',
    '步行者': '印第安纳步行者',
    '鹈鹕': '新奥尔良鹈鹕',
    '奇才': '华盛顿奇才',
    '爵士': '犹他爵士',
    '开拓者': '波特兰开拓者',
    '凯尔特人': '波士顿凯尔特人',
    '篮网': '布鲁克林篮网',
    '尼克斯': '纽约尼克斯',
    '76人': '费城76人',
    '猛龙': '多伦多猛龙',
    '公牛': '芝加哥公牛',
    '骑士': '克利夫兰骑士',
    '雄鹿': '密尔沃基雄鹿',
    '热火': '迈阿密热火',
    '魔术': '奥兰多魔术',
    '老鹰': '亚特兰大老鹰',
    '黄蜂': '夏洛特黄蜂',
    '国王': '萨克拉门托国王',
    '太阳': '菲尼克斯太阳',
    '森林狼': '明尼苏达森林狼',
    '雷霆': '俄克拉荷马城雷霆',
    '灰熊': '孟菲斯灰熊',
    '马刺': '圣安东尼奥马刺'
}

def debug_injury_page():
    """调试墨子说球伤病页面的HTML结构"""
    url = 'http://www.mozishuoqiu.com/index.php/Injury/lst#14'
    print(f"正在访问: {url}")
    
    # 获取页面内容
    response = requests.get(url)
    print(f"HTTP状态码: {response.status_code}")
    
    response.encoding = 'utf-8'
    html_content = response.text
    
    # 输出页面前5000字符
    print("\n" + "="*80)
    print("页面前5000字符:")
    print("="*80)
    print(html_content[:5000])
    print("\n" + "="*80)
    
    # 使用BeautifulSoup解析
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有可能的球队名称元素
    print("\n" + "="*80)
    print("查找球队名称元素:")
    print("="*80)
    
    # 查找所有文本节点，寻找球队名称
    text_nodes = soup.find_all(string=True)
    found_teams = set()
    
    for text in text_nodes:
        text_stripped = text.strip()
        if text_stripped in team_name_map:
            team_name = text_stripped
            if team_name not in found_teams:
                found_teams.add(team_name)
                
                # 获取该文本节点的父元素
                parent = text.parent
                
                print(f"\n找到球队: {team_name}")
                print(f"父元素标签: {parent.name}")
                print(f"父元素class: {parent.get('class', '无')}")
                
                # 输出周围的HTML代码片段
                print("\n周围HTML代码片段:")
                # 获取父元素的前一个和后一个兄弟元素
                prev_sibling = parent.previous_sibling
                next_sibling = parent.next_sibling
                
                if prev_sibling:
                    print(f"前一个兄弟元素: {prev_sibling}")
                
                print(f"当前元素: {parent}")
                
                if next_sibling:
                    print(f"后一个兄弟元素: {next_sibling}")
                
                # 查找附近的表格
                print("\n附近的表格:")
                # 查找当前元素后面的表格
                current = parent
                table_found = False
                
                for _ in range(30):
                    if current:
                        # 检查当前元素是否包含表格
                        tables = current.find_all('table')
                        if tables:
                            for table in tables:
                                print(f"找到表格: {table}")
                                # 输出表格的前5行
                                print("\n表格前5行:")
                                rows = table.find_all('tr')
                                for i, row in enumerate(rows[:5]):
                                    print(f"行 {i+1}: {row}")
                                table_found = True
                                break
                        # 检查下一个兄弟元素
                        current = current.next_sibling
                        # 如果是NavigableString，跳过
                        while current and isinstance(current, str):
                            current = current.next_sibling
                    else:
                        break
                
                if not table_found:
                    print("未找到表格")
    
    # 查找所有表格
    print("\n" + "="*80)
    print(f"找到 {len(soup.find_all('table'))} 个表格")
    print("="*80)

if __name__ == "__main__":
    debug_injury_page()
