
from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None

    if request.method == "POST":
        router_device = {
            'device_type': 'cisco_ios_telnet',
            'ip': '192.168.10.119',
            'port': 32770,
            'username': 'admin',
            'password': 'eve123',
            'secret': 'eve123',
            'fast_cli': False,
            'global_delay_factor': 2,
        }

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        net_connect = None

        try:
            net_connect = ConnectHandler(**router_device)

            net_connect.enable()

            net_connect.send_command_timing("terminal length 0")

            for cmd in commands_to_run:
                output = net_connect.send_command_timing(
                    cmd,
                    read_timeout=60
                )
                results[cmd] = output

        except Exception as e:
            error = f"Connection failed: {e}"

        finally:
            if net_connect:
                net_connect.disconnect()

    return render_template(
        "index.html",
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
