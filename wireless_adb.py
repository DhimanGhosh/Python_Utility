import subprocess

def execute_subprocess_cmd(cmd):
    return subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        ).communicate()[0]

def get_device_list():
    res = execute_subprocess_cmd('adb devices')
    serials = [x.split('\t')[0] for x in res.split('\n') if '\tdevice' in x]
    return serials

def get_device_ip(device_serial):
    device_ip_cmd = f'adb -s {device_serial} shell ip -f inet addr show wlan0'
    res = execute_subprocess_cmd(device_ip_cmd)
    device_ip_address = res.split('\n')[1].strip().split(' ')[1].split('/')[0]
    return device_ip_address

def create_wireless_adb(device, ip_address):
    tcp_port = 5555
    wireless_adb_cmds = [f'adb tcpip {tcp_port}',f'adb connect {ip_address}:{tcp_port}']
    for cmd in wireless_adb_cmds:
        wireless_adb_endpoint = execute_subprocess_cmd(cmd).strip().lstrip('connected to ')
    if 'already connected to' not in wireless_adb_endpoint:
        print(f"Device '{device}' configured with wireless adb at '{wireless_adb_endpoint}'")

def disconnect_all_wireless_adb():
    subprocess.run('adb disconnect')
    subprocess.run('adb devices')

def main():
    devices_attached = get_device_list()
    if devices_attached:
        disconnect_all_wireless_adb()
        for device in devices_attached:
            create_wireless_adb(device, get_device_ip(device))
    else:
        print('Sorry! No Devices attached to this PC...')

if __name__ == '__main__':
    main()
