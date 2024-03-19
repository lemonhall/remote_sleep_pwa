import subprocess
import paho.mqtt.client as mqtt

from datetime import datetime

# 定义进入睡眠状态的命令
sleep_command = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"

def put_windows_to_sleep():
    # 执行睡眠命令
    subprocess.Popen(sleep_command)

# 定义消息处理函数
def message_callback(client, userdata, message):
    print("确实收到新消息了")
    # 在这里编写收到消息后的处理逻辑
    print("Received message:", message.payload.decode("utf-8"))
    msg = message.payload.decode("utf-8")
    if msg == "go_to_sleep":
        print("俺要去睡咯")
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        print("当前时间和日期：", formatted_now)
        put_windows_to_sleep()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    if reason_code!=0 :
        client.reconnect()
    if reason_code == 0:
        # 订阅主题
        client.subscribe("lemon_sleep/#")

def on_log(client, userdata, level, buff):
    print(buff)

# 创建 MQTT 客户端对象
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,transport='websockets')
client.on_log = on_log
client.tls_set()
client.connect("test.mosquitto.org", 8081)
# 注册消息回调函数
client.on_message = message_callback
# 注册成功连接回调
client.on_connect = on_connect

# 主程序逻辑
if __name__ == "__main__":
    # 启动客户端循环
    client.loop_forever()
