import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route('/alerts', methods=['POST'])
def receive_alert():
  print('Alert Triggered! Running Ansible Playbook to heal NGINX...')
  result = subprocess.run(
      ['ansible-playbook', 'heal_nginx.yml'], capture_output=True, text=True
  )
  print(result.stdout)
  return 'Self-healing executed', 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)
