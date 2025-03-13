from flask import Flask, render_template
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

@app.route("/")
def index():
    # 创建 Bokeh 图表
    p = figure(title="Bokeh 图表示例", x_axis_label="X 轴", y_axis_label="Y 轴", tools="pan,wheel_zoom,box_zoom,reset,hover")
    p.line([1, 2, 3], [4, 5, 6], legend_label="线图", line_width=2)
    p.circle([1, 2, 3], [4, 5, 6], legend_label="散点图", size=10)

    # 将图表转换为 HTML 组件
    script, div = components(p)
    print("Script:", script)  # 打印 script 内容
    print("Div:", div)  # 打印 div 内容

    # 渲染模板并传递组件
    return render_template("index.html", script=script, div=div)

if __name__ == "__main__":
    app.run(debug=True)