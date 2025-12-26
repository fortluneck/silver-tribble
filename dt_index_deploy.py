import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 省份提取函数
def extract_province(company_name):
    """从企业名称中提取省份信息"""
    if not company_name or pd.isna(company_name):
        return "未知"
    
    # 定义省份和直辖市的关键词字典
    provinces = {
        '北京': ['北京', '京'],
        '上海': ['上海', '沪', '浦发'],
        '广东': ['广东', '粤', '深圳', '广州', '东莞', '佛山', '珠海'],
        '江苏': ['江苏', '苏', '南京', '苏州', '无锡', '常州'],
        '浙江': ['浙江', '浙', '杭州', '宁波', '温州', '绍兴'],
        '山东': ['山东', '鲁', '青岛', '济南', '烟台', '淄博'],
        '河北': ['河北', '冀', '石家庄', '唐山', '邯郸'],
        '河南': ['河南', '豫', '郑州', '洛阳'],
        '湖北': ['湖北', '鄂', '武汉', '黄石', '十堰'],
        '湖南': ['湖南', '湘', '长沙', '株洲', '湘潭'],
        '四川': ['四川', '川', '蜀', '成都', '绵阳'],
        '陕西': ['陕西', '陕', '秦', '西安', '宝鸡'],
        '安徽': ['安徽', '皖', '合肥', '芜湖'],
        '福建': ['福建', '闽', '福州', '厦门'],
        '江西': ['江西', '赣', '南昌', '九江'],
        '广西': ['广西', '桂', '南宁', '柳州'],
        '云南': ['云南', '滇', '昆明'],
        '贵州': ['贵州', '黔', '贵阳'],
        '辽宁': ['辽宁', '辽', '沈阳', '大连'],
        '吉林': ['吉林', '吉', '长春'],
        '黑龙江': ['黑龙江', '黑', '哈尔滨'],
        '天津': ['天津', '津'],
        '重庆': ['重庆', '渝'],
        '山西': ['山西', '晋', '太原'],
        '内蒙古': ['内蒙古', '蒙', '呼和浩特'],
        '西藏': ['西藏', '藏', '拉萨'],
        '新疆': ['新疆', '疆', '乌鲁木齐'],
        '青海': ['青海', '青', '西宁'],
        '甘肃': ['甘肃', '甘', '陇', '兰州'],
        '宁夏': ['宁夏', '宁', '银川'],
        '海南': ['海南', '琼', '海口', '三亚']
    }
    
    # 特殊处理
    special_cases = {
        '东北': '辽宁',  # 东北高速 -> 辽宁
        '西南': '四川',
        '华北': '北京',
        '华东': '上海',
        '华南': '广东',
        '华中': '湖北'
    }
    
    # 检查特殊情况
    for key, province in special_cases.items():
        if key in company_name:
            return province
    
    # 检查省份关键词
    for province, keywords in provinces.items():
        for keyword in keywords:
            if keyword in company_name:
                return province
    
    return "未知"

# 设置页面配置
st.set_page_config(
    page_title="数字化转型指数分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加CSS自定义样式和Mermaid支持
css_style = """
<style>
/* 全局样式 */
body {
    color: #333333;
    background-color: #f0f2f6;
}

/* 侧边栏样式 */
.sidebar {
    background-color: #1e1e1e;
    color: #ffffff;
}

/* 侧边栏标题 */
.sidebar-header {
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

/* 选择框样式 */
.stSelectbox > label {
    color: #ffffff;
}

.stSelectbox > div > div {
    color: #ffffff;
    background-color: #2a2a2a;
    border: 1px solid #444444;
}

/* 文本输入框样式 */
.stTextInput > label {
    color: #ffffff;
}



.stTextInput > div > div > input {
    color: #ffffff;
    background-color: #2a2a2a;
    border: 1px solid #444444;
}

/* 按钮样式 */
.stButton > button {
    background-color: #1a73e8;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background-color: #1557b0;
}

/* 主内容区域 */
.main-content {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Mermaid图表样式 */
.mermaid {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 添加Mermaid支持
mermaid_script = """
<script src='https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.min.js'></script>
<script>
    mermaid.initialize({startOnLoad: true, theme: 'default'});
    
    // 修改特定输入框标签颜色为黑色
    setTimeout(function() {
        const labels = document.querySelectorAll('.stTextInput > label');
        labels.forEach(label => {
            if (label.textContent.includes('股票代码') || label.textContent.includes('企业名称')) {
                label.style.color = '#000000';
            }
        });
    }, 1000);
</script>
"""
st.markdown(mermaid_script, unsafe_allow_html=True)

# 数据加载与处理
@st.cache_data
def load_data():
    """加载并处理数字化转型指数数据"""
    try:
        # 支持多种文件路径
        import os
        possible_paths = [
            "合并后的数字化转型指数数据.xlsx",
            "./合并后的数字化转型指数数据.xlsx",
            "/app/合并后的数字化转型指数数据.xlsx"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_excel(path)
                break
        else:
            st.error("未找到数据文件")
            return None
        
        # 数据处理
        df['股票代码'] = df['股票代码'].astype(str)
        df['年份'] = df['年份'].astype(int)
        
        # 从企业名称提取省份信息
        df['省份'] = df['企业名称'].apply(extract_province)
        
        # 确保行业名称不为空
        df['行业名称'] = df['行业名称'].fillna('未知行业')
        df['行业代码'] = df['行业代码'].fillna('未知')
        
        return df
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return None

# 加载数据
df = load_data()

if df is not None:
    # 应用标题
    st.title("数字化转型指数分析平台")
    st.markdown("---")
    
    # 侧边栏筛选器
    st.sidebar.header("数据筛选")
    
    # 股票代码搜索（支持多个，用逗号分隔）
    stock_codes = st.sidebar.text_input("股票代码（多个用逗号分隔）")
    
    # 年份筛选（支持多选）
    years = sorted(df['年份'].unique())
    default_years = [2021]  # 默认选择有完整数据的年份
    selected_years = st.sidebar.multiselect("选择年份", years, default=default_years)
    
    # 年份提示
    if any(year > 2021 for year in selected_years):
        st.sidebar.warning("⚠️ 提示：2022年后行业数据不完整，建议查看2021年及之前的数据")
    
    # 行业筛选（支持多选）
    industries = sorted(df['行业名称'].unique())
    selected_industries = st.sidebar.multiselect("选择行业（可多选）", industries)
    
    # 省份筛选（支持多选）
    provinces = sorted(df['省份'].unique())
    selected_provinces = st.sidebar.multiselect("选择省份（可多选）", provinces)
    
    # 企业名称搜索（支持多个，用逗号分隔）
    company_names = st.sidebar.text_input("企业名称（多个用逗号分隔）")
    
    # 筛选数据
    filtered_df = df.copy()
    
    # 年份筛选
    if selected_years:
        filtered_df = filtered_df[filtered_df['年份'].isin(selected_years)]
    
    # 行业筛选
    if selected_industries:
        filtered_df = filtered_df[filtered_df['行业名称'].isin(selected_industries)]
    
    # 省份筛选
    if selected_provinces:
        filtered_df = filtered_df[filtered_df['省份'].isin(selected_provinces)]
    
    # 企业名称筛选
    if company_names:
        names = [name.strip() for name in company_names.split(',') if name.strip()]
        if names:
            filtered_df = filtered_df[filtered_df['企业名称'].str.contains('|'.join(names), case=False, na=False)]
    
    # 股票代码筛选
    if stock_codes:
        codes = [code.strip() for code in stock_codes.split(',') if code.strip()]
        if codes:
            filtered_df = filtered_df[filtered_df['股票代码'].str.contains('|'.join(codes), case=False, na=False)]
    
    # 主内容区域
    with st.container():
        # 数据概览
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("企业数量", len(filtered_df))
        
        if filtered_df.empty:
            st.warning("当前筛选条件下没有数据")
        else:
            avg_index = filtered_df['数字化转型指数(0-100分)'].mean()
            max_index = filtered_df['数字化转型指数(0-100分)'].max()
            min_index = filtered_df['数字化转型指数(0-100分)'].min()
            
            with col2:
                st.metric("平均指数", f"{avg_index:.1f}")
            with col3:
                st.metric("最高指数", int(max_index))
            with col4:
                st.metric("最低指数", int(min_index))
        
        # 数字化转型指数分布与趋势图表
        st.subheader("数字化转型指数分析")
        
        # 创建两列布局
        col_left, col_right = st.columns(2)
        
        with col_left:
            # 左侧：指数分布直方图
            if not filtered_df.empty:
                fig_dist = px.histogram(
                    filtered_df,
                    x='数字化转型指数(0-100分)',
                    title='数字化转型指数分布',
                    color_discrete_sequence=['#1f77b4'],
                    labels={'数字化转型指数(0-100分)': '数字化转型指数(0-100分)', 'count': '企业数量'}
                )
                fig_dist.update_layout(
                    bargap=0.1,
                    xaxis=dict(range=[0, 100], title='数字化转型指数(0-100分)'),
                    yaxis=dict(title='企业数量'),
                    plot_bgcolor='#f9f2f4',
                    paper_bgcolor='#f9f2f4',
                    font=dict(family='Arial', size=12),
                    title_x=0.5
                )
                st.plotly_chart(fig_dist, width='stretch')
            else:
                st.info("当前筛选条件下没有足够的数据生成分布图")
        
        with col_right:
            # 右侧：指数季度趋势图
            trend_df = df.copy()
            
            # 应用与主筛选相同的条件（除年份外）
            if selected_industries:
                trend_df = trend_df[trend_df['行业名称'].isin(selected_industries)]
            if selected_provinces:
                trend_df = trend_df[trend_df['省份'].isin(selected_provinces)]
            if company_names:
                names = [name.strip() for name in company_names.split(',') if name.strip()]
                if names:
                    trend_df = trend_df[trend_df['企业名称'].str.contains('|'.join(names), case=False, na=False)]
            if stock_codes:
                codes = [code.strip() for code in stock_codes.split(',') if code.strip()]
                if codes:
                    trend_df = trend_df[trend_df['股票代码'].str.contains('|'.join(codes), case=False, na=False)]
            
            if not trend_df.empty:
                # 计算每年平均指数
                annual_avg = trend_df.groupby('年份')['数字化转型指数(0-100分)'].mean().reset_index()
                annual_avg = annual_avg.sort_values('年份')
                
                # 绘制趋势图
                fig_trend = px.line(
                    annual_avg,
                    x='年份',
                    y='数字化转型指数(0-100分)',
                    title='指数年度趋势',
                    markers=True,
                    color_discrete_sequence=['#1f77b4'],
                    labels={'数字化转型指数(0-100分)': '指数值', '年份': '年份'}
                )
                fig_trend.update_layout(
                    xaxis=dict(tickmode='linear', title='年份'),
                    yaxis=dict(title='指数值'),
                    plot_bgcolor='#f9f2f4',
                    paper_bgcolor='#f9f2f4',
                    font=dict(family='Arial', size=12),
                    title_x=0.5
                )
                st.plotly_chart(fig_trend, width='stretch')
            else:
                st.info("当前筛选条件下没有足够的数据生成趋势图")
    
    # 企业排名表格
    st.subheader("企业排名")
    if not filtered_df.empty:
            ranked_df = filtered_df.sort_values(by='数字化转型指数(0-100分)', ascending=False)
            display_df = ranked_df[['股票代码', '企业名称', '省份', '行业名称', '数字化转型指数(0-100分)', '总词频数']].head(20)
            display_df.insert(0, '排名', range(1, len(display_df) + 1))
            st.dataframe(display_df, width='stretch')
    
    # 行业对比分析
    st.subheader("行业对比分析")
    year_data = df.copy()
    
    # 应用年份筛选
    if selected_years:
        year_data = year_data[year_data['年份'].isin(selected_years)]
    
    # 应用省份筛选
    if selected_provinces:
        year_data = year_data[year_data['省份'].isin(selected_provinces)]
    
    industry_avg = year_data.groupby('行业名称')['数字化转型指数(0-100分)'].mean().sort_values(ascending=False).reset_index()
    
    if len(industry_avg) > 1:
        # 只显示非未知行业的数据
        industry_avg_non_unknown = industry_avg[industry_avg['行业名称'] != '未知行业']
        
        if len(industry_avg_non_unknown) > 0:
            # 设置图表标题
            if selected_years:
                if len(selected_years) == 1:
                    title = f"{selected_years[0]}年各行业平均指数Top10"
                else:
                    title = f"{min(selected_years)}-{max(selected_years)}年各行业平均指数Top10"
            else:
                title = "各行业平均指数Top10"
            
            fig = px.bar(
                industry_avg_non_unknown.head(10),
                x='行业名称',
                y='数字化转型指数(0-100分)',
                title=title,
                color='数字化转型指数(0-100分)',
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("当前条件下没有非未知行业数据")
    
    # 省份对比分析
    st.subheader("省份对比分析")
    year_data_province = df.copy()
    
    # 应用年份筛选
    if selected_years:
        year_data_province = year_data_province[year_data_province['年份'].isin(selected_years)]
    
    # 应用行业筛选
    if selected_industries:
        year_data_province = year_data_province[year_data_province['行业名称'].isin(selected_industries)]
    
    province_avg = year_data_province.groupby('省份')['数字化转型指数(0-100分)'].mean().sort_values(ascending=False).reset_index()
    
    if len(province_avg) > 1:
        # 只显示非未知省份的数据
        province_avg_non_unknown = province_avg[province_avg['省份'] != '未知']
        
        if len(province_avg_non_unknown) > 0:
            # 设置图表标题
            if selected_years:
                if len(selected_years) == 1:
                    title = f"{selected_years[0]}年各省份平均指数Top10"
                else:
                    title = f"{min(selected_years)}-{max(selected_years)}年各省份平均指数Top10"
            else:
                title = "各省份平均指数Top10"
            
            fig = px.bar(
                province_avg_non_unknown.head(10),
                x='省份',
                y='数字化转型指数(0-100分)',
                title=title,
                color='数字化转型指数(0-100分)',
                color_continuous_scale='Greens'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("当前条件下没有非未知省份数据")
    

    
    # 数字化转型指数地图分布
    st.subheader("数字化转型指数地理分布")
    # 应用年份筛选（如果选择了多个年份，默认使用最新年份）
    if selected_years:
        map_data = df[df['年份'] == max(selected_years)]
    else:
        map_data = df[df['年份'] == df['年份'].max()]
    
    # 应用筛选条件
    if selected_industries:
        map_data = map_data[map_data['行业名称'].isin(selected_industries)]
    if company_names:
        names = [name.strip() for name in company_names.split(',') if name.strip()]
        if names:
            map_data = map_data[map_data['企业名称'].str.contains('|'.join(names), case=False, na=False)]
    if stock_codes:
        codes = [code.strip() for code in stock_codes.split(',') if code.strip()]
        if codes:
            map_data = map_data[map_data['股票代码'].str.contains('|'.join(codes), case=False, na=False)]
    
    # 计算各省份平均指数
    province_map_data = map_data.groupby('省份')['数字化转型指数(0-100分)'].mean().reset_index()
    province_map_data = province_map_data[province_map_data['省份'] != '未知']
    
    if not province_map_data.empty:
        # 使用Plotly的中国地图可视化
        # 获取当前地图数据使用的年份
        map_year = max(selected_years) if selected_years else df['年份'].max()
        
        # 为中国省份创建一个映射字典，确保Plotly能正确识别
        province_mapping = {
            '北京': 'Beijing',
            '上海': 'Shanghai',
            '广东': 'Guangdong',
            '江苏': 'Jiangsu',
            '浙江': 'Zhejiang',
            '山东': 'Shandong',
            '河北': 'Hebei',
            '河南': 'Henan',
            '湖北': 'Hubei',
            '湖南': 'Hunan',
            '四川': 'Sichuan',
            '陕西': 'Shaanxi',
            '安徽': 'Anhui',
            '福建': 'Fujian',
            '江西': 'Jiangxi',
            '广西': 'Guangxi',
            '云南': 'Yunnan',
            '贵州': 'Guizhou',
            '辽宁': 'Liaoning',
            '吉林': 'Jilin',
            '黑龙江': 'Heilongjiang',
            '天津': 'Tianjin',
            '重庆': 'Chongqing',
            '山西': 'Shanxi',
            '内蒙古': 'Nei Mongol',
            '西藏': 'Xizang',
            '新疆': 'Xinjiang',
            '青海': 'Qinghai',
            '甘肃': 'Gansu',
            '宁夏': 'Ningxia',
            '海南': 'Hainan'
        }
        
        # 创建带英文省份名称的地图数据
        map_data_with_en = province_map_data.copy()
        map_data_with_en['Province_EN'] = map_data_with_en['省份'].map(province_mapping)
        
        # 过滤掉无法映射的省份
        map_data_with_en = map_data_with_en.dropna(subset=['Province_EN'])
        
        if not map_data_with_en.empty:
            # 创建中国地图
            fig = px.choropleth(
                map_data_with_en,
                locations='Province_EN',
                locationmode='country names',
                scope='asia',
                color='数字化转型指数(0-100分)',
                hover_name='省份',
                hover_data={'Province_EN': False, '数字化转型指数(0-100分)': ':.1f'},
                title=f'{map_year}年各省份数字化转型指数分布',
                color_continuous_scale='Blues',
                range_color=[0, 100]
            )
            
            # 增强地图视觉效果
            fig.update_geos(
                center={'lat': 35, 'lon': 105},
                projection_scale=5,
                visible=False,
                showcountries=True,
                countrycolor='#444444',
                showcoastlines=True,
                coastlinecolor='#999999',
                showland=True,
                landcolor='#f8f9fa',
                showlakes=True,
                lakecolor='#e3f2fd',
                resolution=50  # 提高地图分辨率
            )
            
            # 美化布局
            fig.update_layout(
                title={
                    'text': f'{map_year}年各省份数字化转型指数分布',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 20, 'color': '#333333'}
                },
                geo=dict(
                    fitbounds='locations',
                    lataxis=dict(range=[18, 53]),
                    lonaxis=dict(range=[73, 135])
                ),
                coloraxis_colorbar={
                    'title': '指数值',
                    'tickformat': '.0f',
                    'len': 0.8,
                    'thickness': 20,
                    'bgcolor': '#f5f5f5',
                    'borderwidth': 1,
                    'bordercolor': '#cccccc'
                },
                hoverlabel={
                    'bgcolor': 'white',
                    'font_color': '#333333',
                    'bordercolor': '#dddddd',
                    'font_size': 14
                },
                margin={'r': 20, 'l': 20, 't': 60, 'b': 20}
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("当前筛选条件下没有可显示在地图上的省份数据")
    else:
        st.info("当前筛选条件下没有足够的数据生成地图")
        

