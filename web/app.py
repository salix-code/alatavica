from datetime import datetime, timedelta
from functools import reduce

from flask import Flask, render_template,redirect, url_for

import bokeh.plotting as plotting
import bokeh.embed as embed

from alatavica.datatype import FCandleData, FDownloadSetting
from alatavica.db import FDatabase,FTable


from web.policy.policy_manager import PolicyManager
from web.render import FRender

import os

from alatavica.download.eod_downloader import download as eod_download
from alatavica.download.yfinance_downloader import download as yfinance_download
import time

app = Flask(__name__)

pm = PolicyManager()

@app.route("/<ticker>")
def get_ticker(ticker):
    # 创建 Bokeh 图表
    ticker = "1816.HK" if ticker is None else ticker
    db = FDatabase()
    table: FTable = db.get_table(ticker, "1d")
    rows: [FCandleData] = table.fetch_rows()
    rows.sort(key=lambda x: x.time)
    rows = rows[max(0, len(rows) - 360):]
    render = FRender(ticker)
    render.draw(rows)

    #policy_type = pm.find_policy(policy_name)
    #policy = policy_type()
    #policy.draw(render)


    # 将图表转换为 HTML 组件
    script,div = embed.components(render.finish())
    # 渲染模板并传递组件
    return render_template("ticker.html", bokeh_script = script,bokeh_div = div)
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    symbol_names = []
    for db_name in os.listdir("../db/"):
        if db_name.endswith(".db"):
            symbol_names.append(db_name[:-3])

    db = FDatabase()
    end_day = datetime.today()
    for symbol_name in symbol_names:
        table = db.get_table(symbol_name, "1d")
        row: [FCandleData] = table.fetch_rows()
        start_day = end_day - timedelta(days=360)
        if len(row) > 0:
            if start_day < row[0].time:
                start_day = row[0].time + timedelta(days=1)
        if start_day > end_day:
            continue
        download_setting = FDownloadSetting(symbol_name, start_day, end_day)
        download_rows: [FCandleData] = yfinance_download(download_setting)

        with_fail_data = (len(download_rows) == 0)
        if len(download_rows) > 0:
            for row in download_rows:
                if row.begin_price == 0:
                    with_fail_data = True
                    break
        if with_fail_data:
            download_rows = eod_download(download_setting)

        table.append_rows(download_rows)

        db.save_table(table)

        time.sleep(5)

        return redirect(url_for('update_result'))

@app.route('/update_result', methods=['POST'])
def update_result():
    return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)