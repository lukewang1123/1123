import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# 球队名称映射字典，将常用简称映射为全称
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

# 反向映射，用于从全称获取简称
full_name_to_short = {v: k for k, v in team_name_map.items()}

# 常见的NBA球队名称列表
NBA_TEAMS = list(team_name_map.keys())

# 球队全称列表
NBA_FULL_TEAMS = list(team_name_map.values())

def fetch_all_injuries():
    """从墨子说球网站抓取所有球队的详细伤病信息"""
    url = 'http://www.mozishuoqiu.com/index.php/Injury/lst#14'
    print(f"正在访问: {url}")
    response = requests.get(url)
    print(f"HTTP状态码: {response.status_code}")
    
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_injuries = {}
    
    # 查找所有表格
    tables = soup.find_all('table')
    print(f"\n找到 {len(tables)} 个表格")
    
    # 遍历所有表格
    print("\n正在解析表格数据...")
    
    for i, table in enumerate(tables):
        print(f"\n处理表格 {i+1}:")
        
        # 查找表格的tbody
        tbody = table.find('tbody')
        if not tbody:
            print("  未找到tbody，跳过")
            continue
        
        # 获取所有数据行
        rows = tbody.find_all('tr')
        if not rows:
            print("  表格中没有数据行，跳过")
            continue
        
        # 第一行的第一个单元格是球队名称
        first_row = rows[0]
        cols = first_row.find_all('td')
        if len(cols) < 1:
            print("  第一行没有足够的单元格，跳过")
            continue
        
        # 提取球队名称，去除"返回顶部"文本
        team_name = cols[0].text.strip()
        # 去除"返回顶部"文本
        team_name = team_name.replace('返回顶部', '').strip()
        print(f"  找到球队: {team_name}")
        
        # 解析所有数据行
        injuries = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                print(f"  行数据不完整，跳过: {row}")
                continue
            
            # 提取字段
            player = cols[1].text.strip()
            status = cols[2].text.strip()
            reason = cols[3].text.strip()
            timeline = cols[4].text.strip()
            
            # 构建伤病记录
            injury_record = {
                "player": player,
                "status": status,
                "reason": reason,
                "timeline": timeline
            }
            injuries.append(injury_record)
        
        # 添加到结果字典
        all_injuries[team_name] = injuries
        print(f"  球队: {team_name}，伤病球员数量: {len(injuries)}")
    
    print(f"\n总共抓取到 {len(all_injuries)} 支球队的伤病信息")
    return all_injuries

def read_games(file_path):
    """读取比赛信息"""
    games = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # 解析比赛信息，新格式：YYYY-MM-DD 客队 vs 主队 时间
            match = re.match(r'(\d{4}-\d{2}-\d{2}) (.*) vs (.*) (.*)', line)
            if match:
                date = match.group(1).strip()
                away_team = match.group(2).strip()
                home_team = match.group(3).strip()
                time = match.group(4).strip()
                games.append({'date': date, 'away': away_team, 'home': home_team, 'time': time})
    
    return games

def get_tomorrow_date():
    """获取明天的日期，格式为YYYY-MM-DD"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%d')

def get_tomorrow_display_date():
    """获取明天的日期，用于显示，格式为月日"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    return tomorrow.strftime('%m月%d日')

def generate_html(games, all_injuries):
    """生成HTML页面"""
    tomorrow_display = get_tomorrow_display_date()
    
    html = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NBA伤病查询</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            
            header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px 0;
                background-color: #1a73e8;
                color: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            h1 span {
                margin-right: 10px;
            }
            
            .date {
                font-size: 16px;
                opacity: 0.9;
            }
            
            .game-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .game-time {
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }
            
            .game-info {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
            }
            
            .team-section {
                margin-bottom: 15px;
            }
            
            .team-name {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #1a73e8;
            }
            
            .injury-list {
                list-style: none;
            }
            
            .injury-item {
                padding: 8px 0;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .injury-item:last-child {
                border-bottom: none;
            }
            
            .injury-detail {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
                padding-left: 15px;
            }
            
            .no-injury {
                color: #4caf50;
                font-weight: bold;
                text-align: center;
                padding: 10px 0;
            }
            
            .no-games {
                text-align: center;
                background-color: white;
                border-radius: 10px;
                padding: 40px 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                color: #666;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1><span>🏀</span> 世界之巅球员伤病参考</h1>
                <div class="date">'''
    html += tomorrow_display
    html += '''</div>
            </header>
    '''
    
    if not games:
        html += '''
            <div class="no-games">
                明日无比赛
            </div>
        '''
    else:
        for game in games:
            away_team = game['away']
            home_team = game['home']
            game_time = game['time']
            
            # 直接使用页面上的球队名称获取伤病数据
            away_injuries = all_injuries.get(away_team, [])
            home_injuries = all_injuries.get(home_team, [])
            
            html += '''
            <div class="game-card">
                <div class="game-time">'''
            html += game_time
            html += '''</div>
                <div class="game-info">'''
            html += away_team + ' vs ' + home_team
            html += '''</div>
                
                <div class="team-section">
                    <div class="team-name">'''
            html += away_team + '伤病情况'
            html += '''</div>
                    '''
            if away_injuries:
                html += '<ul class="injury-list">'
                for injury in away_injuries:
                    html += '<li class="injury-item">'
                    html += injury['player'] + ': ' + injury['status']
                    html += '<div class="injury-detail">'
                    html += '原因: ' + injury['reason'] + '<br>'
                    html += '时间表: ' + injury['timeline']
                    html += '</div>'
                    html += '</li>'
                html += '</ul>'
            else:
                html += '<div class="no-injury">✅ 暂无重要伤病</div>'
            html += '''
                </div>
                
                <div class="team-section">
                    <div class="team-name">'''
            html += home_team + '伤病情况'
            html += '''</div>
                    '''
            if home_injuries:
                html += '<ul class="injury-list">'
                for injury in home_injuries:
                    html += '<li class="injury-item">'
                    html += injury['player'] + ': ' + injury['status']
                    html += '<div class="injury-detail">'
                    html += '原因: ' + injury['reason'] + '<br>'
                    html += '时间表: ' + injury['timeline']
                    html += '</div>'
                    html += '</li>'
                html += '</ul>'
            else:
                html += '<div class="no-injury">✅ 暂无重要伤病</div>'
            html += '''
                </div>
            </div>
        '''
    
    html += '''
        </div>
    </body>
    </html>
    '''
    
    return html

def main():
    # 获取明天的日期
    tomorrow_date = get_tomorrow_date()
    print(f"明日日期: {tomorrow_date}")
    
    # 读取比赛信息
    all_games = read_games('games.txt')
    print(f"读取到 {len(all_games)} 场比赛")
    
    # 过滤出明天的比赛
    tomorrow_games = [game for game in all_games if game['date'] == tomorrow_date]
    print(f"明日比赛: {len(tomorrow_games)} 场")
    for game in tomorrow_games:
        print(f"  - {game['away']} vs {game['home']} {game['time']}")
    
    # 抓取详细的伤病数据
    all_injuries = fetch_all_injuries()
    
    # 调试输出：打印所有抓取到的球队名称
    print("\n=== 调试输出 ===")
    print("所有抓取到的球队名称:")
    all_teams = list(all_injuries.keys())
    for team in all_teams:
        print(f"  - {team}")
    print(f"总计 {len(all_teams)} 支球队")
    
    # 调试输出：打印鹈鹕队的伤病列表详情
    print("\n鹈鹕队的伤病列表详情:")
    pelicans_injuries = all_injuries.get('鹈鹕', [])
    print(f"  伤病球员数量: {len(pelicans_injuries)}")
    for injury in pelicans_injuries:
        print(f"    * {injury['player']}: {injury['status']}")
        print(f"      原因: {injury['reason']}")
        print(f"      时间表: {injury['timeline']}")
    
    # 调试输出：打印明天比赛中涉及的球队映射和伤病数据
    print("\n明天比赛中涉及的球队映射和伤病数据:")
    for game in tomorrow_games:
        away_team = game['away']
        home_team = game['home']
        
        # 从all_injuries中取到的伤病数据（直接使用页面上的球队名称）
        away_injuries_data = all_injuries.get(away_team, [])
        home_injuries_data = all_injuries.get(home_team, [])
        
        print(f"\n比赛: {away_team} vs {home_team}")
        print(f"  {away_team} 伤病数据数量: {len(away_injuries_data)}")
        print(f"  {home_team} 伤病数据数量: {len(home_injuries_data)}")
    
    # 打印明天比赛球队的伤病情况
    print("\n明天比赛球队的伤病情况:")
    for game in tomorrow_games:
        away_team = game['away']
        home_team = game['home']
        
        # 检查球队是否在伤病数据中
        away_injuries = all_injuries.get(away_team, [])
        home_injuries = all_injuries.get(home_team, [])
        
        print(f"\n{away_team}:")
        print(f"  - 伤病球员数量: {len(away_injuries)}")
        for injury in away_injuries:
            print(f"    * {injury['player']}: {injury['status']}")
            print(f"      原因: {injury['reason']}")
            print(f"      时间表: {injury['timeline']}")
        
        print(f"\n{home_team}:")
        print(f"  - 伤病球员数量: {len(home_injuries)}")
        for injury in home_injuries:
            print(f"    * {injury['player']}: {injury['status']}")
            print(f"      原因: {injury['reason']}")
            print(f"      时间表: {injury['timeline']}")
    
    # 生成HTML
    html_content = generate_html(tomorrow_games, all_injuries)
    
    # 写入HTML文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n更新完成！HTML页面已生成。明日日期：{tomorrow_date}，比赛场次：{len(tomorrow_games)}")

if __name__ == "__main__":
    main()
