from pyecharts.charts import Map
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts.globals import ThemeType #引入主题
import os
from pathlib import Path



#把excel表格中的数据，以字典形式存储
excel_path = 'D:\软工\软工个人作业\个人作业1\修订版本\excel'
dir_list = os.listdir(excel_path)
dir_list = sorted(dir_list,key=lambda x: os.path.getctime(os.path.join(excel_path, x))) #按创建时间依次访问

for i in dir_list:  # 对于每一个文件
    filePath = r'D:\软工\软工个人作业\个人作业1\修订版本\excel' + '\\' + i  # 所存txt绝对路径
    print(filePath)
    name = Path(filePath).stem #存下文件名

    data = pd.read_excel(filePath, sheet_name='Sheet2')
    print(filePath)
    print(data)
    province = list(data["省份"])
    add_confirmed = list(data["新增确诊"])
    li = [list(z) for z in zip(province,add_confirmed)]

    c = (
        Map(init_opts=opts.InitOpts(width="1500px", height="1000px"))  # 可切换主题
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2022年"+ name +"新型冠状病毒新增确诊病例"),
            visualmap_opts=opts.VisualMapOpts(
                min_=1,
                max_=4000,
                range_text=['新型冠状病毒新增确诊病例区间:', ''],  # 分区间
                is_piecewise=True,  # 定义图例为分段型，默认为连续的图例
                pieces=[
                    {"min": 1, "max": 9, "lable": "1-9人", "color": "#CCFFFF"},
                    {"min": 10, "max": 99, "lable": "10-99人", "color": "#FFFF99"},
                    {"min": 100, "max": 299, "lable": "100-299人", "color": "#FF9966"},
                    {"min": 300, "max": 499, "lable": "300-499人", "color": "#FF6666"},
                    {"min": 500, "max": 999, "lable": "500-999人", "color": "#CC3333"},
                    {"min": 1000, "lable": "1000+人", "color": "#990033"}
                ]
            )
        )
            .add("add_confirmed", li, maptype="china")


            .render("2022年"+ name + ".html")
    )



