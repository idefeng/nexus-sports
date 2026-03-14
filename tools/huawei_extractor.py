import subprocess
import json
import os
import time

class HuaweiExtractor:
    def __init__(self, bundle_name="com.nexus.health.bridge"):
        self.bundle_name = bundle_name
        self.device_id = None

    def run_hdc(self, args):
        cmd = ["hdc"] + args
        if self.device_id:
            cmd = ["hdc", "-t", self.device_id] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"HDC Error: {e.stderr}")
            return None

    def check_connection(self):
        output = self.run_hdc(["list", "targets"])
        if not output:
            print("No HarmonyOS devices found.")
            return False
        
        targets = output.split('\n')
        self.device_id = targets[0]
        print(f"Connected to device: {self.device_id}")
        return True

    def install_app(self, hap_path):
        print(f"Installing bridge app: {hap_path}")
        return self.run_hdc(["app", "install", hap_path])

    def trigger_dump(self):
        print("Please click 'Authorize & Dump Data' on your phone.")
        # In a real setup, we could use 'hdc shell aa start' to launch the app
        self.run_hdc(["shell", "aa", "start", "-b", self.bundle_name, "-a", "EntryAbility"])

    def pull_data(self, remote_path, local_path):
        print(f"Pulling data from {remote_path}...")
        return self.run_hdc(["file", "recv", remote_path, local_path])

    def run(self, hap_path=None):
        if not self.check_connection():
            return

        if hap_path and os.path.exists(hap_path):
            self.install_app(hap_path)

        self.trigger_dump()
        
        # Wait for user interaction and file creation
        remote_path = f"/data/app/el2/100/base/{self.bundle_name}/files/huawei_health_dump.json"
        local_path = "./huawei_dump.json"
        
        print("Waiting for data file...")
        for _ in range(30):
            time.sleep(2)
            if self.pull_data(remote_path, local_path) is not None:
                print(f"Success! Data saved to {local_path}")
                return True
        
        print("Timeout waiting for data. Make sure you clicked the button in the app.")
        return False

if __name__ == "__main__":
    extractor = HuaweiExtractor()
    extractor.run()
