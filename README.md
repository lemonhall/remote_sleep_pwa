# remote_sleep_pwa

https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable

![a4d9fc0638a83a00c2d3b6a2c297bd9](https://github.com/lemonhall/remote_sleep_pwa/assets/637919/74dcab97-f235-49bb-8e70-2fa30df6586b)


1、第一件事，是搞一个https的站点出来

打开dns，这就是分分钟的事情了

我增加了一个叫sleep的

2、第二步，搞一下nginx

到/etc/nginx/sites-enabled,目录下

lemonhall@lemonhallme:/etc/nginx/sites-enabled$ ls
code-server  default  lemon-blog
lemonhall@lemonhallme:/etc/nginx/sites-enabled$ 

    sudo cp pwa-demo sleep-pwa

    server {
        listen 80;
        server_name sleep.lemonhall.me;
        # enforce https
        return 301 https://$server_name:443$request_uri;
    }
    server {
        listen 443 ssl http2;
        server_name sleep.lemonhall.me;
        ssl_certificate /etc/letsencrypt/live/172-233-73-134.ip.linodeusercontent.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/172-233-73-134.ip.linodeusercontent.com/privkey.pem;
        location / {
            root /home/lemonhall/sleep_pwa;
            index index.html;
            try_files $uri $uri/ =404;
        }
    }


然后：
  sudo systemctl reload nginx

3、验证一下哈
  https://sleep.lemonhall.me/

没问题哈

5、修改index.html

      <body>
        <h2>远程睡眠控制器</h2>
        <button onclick="sleep()">睡眠</button>
      
        <script>
          function sleep() {
            // 在此处添加调用远程 HTTP 接口的代码
            // 例如，使用 AJAX 发送 POST 请求到指定的 URL
            fetch('http://192.168.50.250/sleep', {
              method: 'GET'
            })
              .then(response => response.json())
              .then(data => console.log(data));
          }
        </script>
      </body>

6、接着来
安全上下文
要使 Web 应用程序可安装，它必须在安全上下文中提供。通常意味着它必须通过 HTTPS 提供。本地资源，如 localhost、127.0.0.1 和 file:// 也被视为安全。

我这么搞，首先满足了安全上下文吧？
对吧

7、然后
https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation

接下来让这个应用可以离线起来
https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps/Tutorials/CycleTracker/HTML_and_CSS

接着就是一个教程了

首先我优化了viewport
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Cycle Tracker</title>
    <link rel="stylesheet" href="style.css" />

声明我自己是个中文：
  <html lang="zh">

9、开始想办法能让它离线
https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps/Tutorials/CycleTracker/Service_workers

10、按照豆包的建议

    .container {
      width: 100%;
      padding: 20px;
      background-color: #f5f5f5;
      border-radius: 5px;
      margin: 0 auto;
      text-align: center;
    }

    .sleep-btn {
      padding: 10px 20px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }

11、解决SSL问题
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

  # 主程序逻辑
  if __name__ == "__main__":
      app.run(host='0.0.0.0', port=16086,ssl_context='adhoc')

flask报错：
    * Serving Flask app 'sleep'
    * Debug mode: off
    Traceback (most recent call last):
      File "C:\Users\lemon\Desktop\sleep.py", line 23, in <module>
        app.run(host='0.0.0.0', port=16086,ssl_context='adhoc')
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 615, in run
        run_simple(t.cast(str, host), port, self, **options)
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\werkzeug\serving.py", line 1077, in run_simple
        srv = make_server(
              ^^^^^^^^^^^^
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\werkzeug\serving.py", line 917, in make_server
        return ThreadedWSGIServer(
              ^^^^^^^^^^^^^^^^^^^
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\werkzeug\serving.py", line 790, in __init__
        ssl_context = generate_adhoc_ssl_context()
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\werkzeug\serving.py", line 589, in generate_adhoc_ssl_context
        cert, pkey = generate_adhoc_ssl_pair()
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\lemon\AppData\Local\Programs\Python\Python312\Lib\site-packages\werkzeug\serving.py", line 504, in generate_adhoc_ssl_pair
        raise TypeError(
    TypeError: Using ad-hoc certificates requires the cryptography library.
    PS C:\Users\lemon\Desktop>

安装库：
  pip install cryptography

OK，不再报错
  PS C:\Users\lemon\Desktop> python .\sleep.py
  * Serving Flask app 'sleep'
  * Debug mode: off
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  * Running on all addresses (0.0.0.0)
  * Running on https://127.0.0.1:16086
  * Running on https://192.168.50.250:16086
  Press CTRL+C to quit

而且地址也是正确显示了的

12、尝试解决SSL证书报错问题

在dns那边做了手脚
    sleep_win11.lemonhall.me  192.168.50.250
做了一个指向本地的地址的dns


      PS C:\Users\lemon> ping sleep_win11.lemonhall.me

      正在 Ping sleep_win11.lemonhall.me [192.168.50.250] 具有 32 字节的数据:
      来自 192.168.50.250 的回复: 字节=32 时间<1ms TTL=128
      来自 192.168.50.250 的回复: 字节=32 时间<1ms TTL=128

      192.168.50.250 的 Ping 统计信息:
          数据包: 已发送 = 2，已接收 = 2，丢失 = 0 (0% 丢失)，
      往返行程的估计时间(以毫秒为单位):
          最短 = 0ms，最长 = 0ms，平均 = 0ms
      Control-C
      PS C:\Users\lemon>

测试没有问题了

修改前端call的地址到：https://sleep_win11.lemonhall.me:16086/test

然后修改python端也需要把host那边指向这个地址

最后代理服务器这边需要bypass掉这个地址，需要把整个链路都bypass掉

  sleep.lemonhall.me/:1 Access to fetch at 'https://sleep_win11.lemonhall.me:16086/test' from origin 'https://sleep.lemonhall.me' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.

然后开始报CORS错误，哎呦喂

解决的方式是：flask_cors模块

      import subprocess
      from flask import Flask, request
      from flask_cors import CORS

      # 定义进入睡眠状态的命令
      sleep_command = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"

      def put_windows_to_sleep():
          # 执行睡眠命令
          subprocess.Popen(sleep_command)

      # 创建 Flask 应用
      app = Flask(__name__)
      CORS(app)

然后又开始报错了：
       GET https://sleep_win11.lemonhall.me:16086/test net::ERR_CERT_AUTHORITY_INVALID

哎，好烦啊，这些游览器就没有一个简单模式么：
  https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

https://experienceleague.adobe.com/en/docs/target/using/experiences/vec/troubleshoot-composer/mixed-content

直接给它允许了，在ios上再看怎么回事，烦死了


13、换了一种方式，走wss

        <script src="https://unpkg.com/mqtt@latest/dist/mqtt.min.js"></script>

        <script>
          var client = mqtt.connect("wss://test.mosquitto.org:8081") // you add a ws:// url here
          client.on('connect', ()=>{
            console.log('connected.');
            client.subscribe("mee")
            client.on("message", function (topic, payload) {
              console.log(payload);
              console.log([topic, payload].join(": "));
              // client.end()
            });
        
            client.publish("mee", "hello");    
          });
        </script>

安装依赖：
  pip install paho-mqtt

https://stackoverflow.com/questions/74344689/python-paho-mqtt-client-websocket-handshake-error-connection-not-upgraded

      import subprocess
      from flask import Flask, request
      from flask_cors import CORS
      import paho.mqtt.client as mqtt

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

这是改好了的服务端的代码，很好用

    import tkinter as tk
    import subprocess

    # 定义待启动程序的类
    class Program:
        def __init__(self, name, enabled):
            self.name = name
            self.enabled = enabled

    # 创建主窗口
    root = tk.Tk()

    # 设置窗口标题
    root.title("Startup Programs Manager")

    # 创建列表框
    program_list = tk.Listbox(root, width=20, height=10)
    program_list.pack()

    # 创建添加按钮
    add_button = tk.Button(root, text="Add", command=lambda: add_program())
    add_button.pack()

    # 创建删除按钮
    del_button = tk.Button(root, text="Delete", command=lambda: delete_program())
    del_button.pack()

    # 创建启动按钮
    start_button = tk.Button(root, text="Start", command=lambda: start_programs())
    start_button.pack()

    # 初始化程序列表
    programs = [Program("sleep.py", True),
                Program("Program 2", False),
                Program("Program 3", True)]

    # 将初始程序添加到列表框
    for program in programs:
        program_list.insert(tk.END, program.name)

    # 定义添加程序的函数
    def add_program():
        name = input("请输入程序名称：")
        enabled = True if input("启用该程序吗？(y/n) ") == "y" else False
        programs.append(Program(name, enabled))
        program_list.insert(tk.END, name)

    # 定义删除程序的函数
    def delete_program():
        selection = program_list.curselection()
        if selection:
            program_name = program_list.get(selection[0])
            programs.remove(program_name)
            program_list.delete(selection[0])

    # 定义启动程序的函数
    def start_programs():
        for program in programs:
            if program.enabled:
                subprocess.Popen(["python", program.name])

    # 运行主事件循环
    root.mainloop()

这是GUI部分的代码
