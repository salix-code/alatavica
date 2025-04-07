from functools import reduce

from flask import Flask, render_template
import bokeh.plotting as plotting
import bokeh.embed as embed

from alatavica.datatype import FCandleData
from alatavica.db import FDatabase,FTable


from web.policy.policy_manager import PolicyManager
from web.render import FRender

app = Flask(__name__)

pm = PolicyManager()

@app.route("/<ticker>/<policy_name>")
def get_ticker(ticker,policy_name):
    # 创建 Bokeh 图表
    ticker = "1816.HK" if ticker is None else ticker
    db = FDatabase()
    table: FTable = db.get_table(ticker, "1d")
    rows: [FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time)
    rows = rows[max(0, len(rows) - 360):]
    render = FRender(ticker)
    render.draw(rows)

    policy_type = pm.find_policy(policy_name)
    policy = policy_type()
    policy.draw(render)


    # 将图表转换为 HTML 组件
    script,div = embed.components(render.finish())
    # 渲染模板并传递组件
    return render_template("index.html", bokeh_script = script,bokeh_div = div)
@app.route("/")
def index():
    return get_ticker("9690.HK")

if __name__ == "__main__":
    app.run(debug=True)