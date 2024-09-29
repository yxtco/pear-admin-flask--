import applications.common.curd
from applications.common.helper import ModelFilter
from applications import create_app
from applications.models import WorkModels, WorkLogModel
from applications.common import curd
from threading import Thread
from datetime import datetime, timedelta
import time

app = create_app()


# 假设这是你的数据库操作函数
def check_and_update_expired_works():
    # 这里应该是你的数据库连接和查询逻辑
    # 示例：从user_work表中获取所有记录，并检查expire_at字段
    with app.app_context():  # 确保在Flask上下文中运行
        # 模拟数据库查询
        # 实际应用中应替换为真实的数据库查询
        mf = ModelFilter()
        mf.exact('work_status', "未处理")
        works = WorkModels.query.filter(mf.get_filter(WorkModels)).all()
        for work in works:
            if work.expire_at < datetime.now():
                # 更新数据库中的状态
                print(f"Work {work.id} has expired. Updating status...")
                # 更新work_status
                work.update_work(work.exnumber, {"work_status": "已关闭", "is_expire": True})
                # 实际应用中应替换为真实的数据库更新操作
                worklog = WorkLogModel(
                    work_id=work.id,
                    work_status="已关闭",
                    comment="已超时关闭",
                    create_at=datetime.now(),
                    user_id=0,
                )
                worklog.worklog_save()
                pass


def run_periodic_check():
    while True:
        check_and_update_expired_works()
        # 每60秒检查一次
        time.sleep(60)


if __name__ == "__main__":
    ip_address = "0.0.0.0"
    port = 5000
    adebug_mode = False

    # 启动后台线程
    thread = Thread(target=run_periodic_check)
    thread.daemon = True  # 设置为守护线程，这样主线程退出时子线程也会退出
    thread.start()

    app.run(host=ip_address, port=port, debug=adebug_mode)
