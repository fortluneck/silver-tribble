# 数字化转型指数分析平台

这是一个基于Streamlit的数字化转型指数分析平台，用于可视化和分析企业数字化转型指数数据。

## 功能特性

- **多维度数据筛选**：支持按年份、股票代码、行业、省份和企业名称进行筛选
- **数据可视化**：包括指数分布直方图、年度趋势图、行业对比分析、省份对比分析和地理分布图
- **企业排名**：展示数字化转型指数前20名的企业
- **响应式设计**：适配不同屏幕尺寸

## 技术栈

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy

## 项目结构

```
.
├── app/                  # 应用程序目录
├── data/                 # 数据文件目录
├── assets/               # 资源文件目录
├── utils/                # 辅助工具函数目录
├── dt_index_deploy.py    # 主应用程序文件
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
streamlit run dt_index_deploy.py
```

## 部署到 Streamlit Cloud

1. 将项目上传到 GitHub
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 点击 "New app"
4. 选择你的 GitHub 仓库和分支
5. 指定主文件路径：`dt_index_deploy.py`
6. 点击 "Deploy!"

## 数据文件

应用程序需要以下数据文件：
- `合并后的数字化转型指数数据.xlsx`：包含所有年份的数字化转型指数数据

确保数据文件与主应用程序文件在同一目录下，或在 `possible_paths` 列表中指定正确的路径。

## 自定义配置

- **CSS样式**：可以在 `css_style` 变量中修改应用程序的样式
- **省份提取规则**：可以在 `extract_province` 函数中修改省份提取的规则
- **数据文件路径**：可以在 `load_data` 函数的 `possible_paths` 列表中添加或修改数据文件路径

## 许可证

MIT
