# Fully Automated Self-Healing Infrastructure

**Author:** Arpit Kumar  
**Tech Stack:** Docker Compose, Nginx, Prometheus, Alertmanager, Python (Flask), Ansible  

## 🚀 Project Overview
In modern DevOps practices, ensuring high availability is critical. This project demonstrates a zero-touch, self-healing DevOps pipeline. Instead of relying on manual intervention, this architecture automatically detects when a core web service (Nginx) crashes and executes a remediation playbook to restart it within seconds, ensuring near 100% uptime.

## 🏗️ Architecture Workflow
1. **Monitoring:** `nginx-exporter` extracts live metrics from the Nginx `/stub_status` page.
2. **Evaluation:** Prometheus scrapes these metrics. If the service drops (`nginx_up == 0`), an alert is generated.
3. **Routing:** Prometheus forwards the alert to **Alertmanager**.
4. **Triggering:** Alertmanager sends an HTTP POST request to a custom **Python Webhook** (Port 5001).
5. **Execution:** The webhook executes an **Ansible** playbook (`heal_nginx.yml`), which automatically runs the Docker command to restart the failed Nginx container.

## 🛠️ Real-World Challenges & Fixes (My Experience)
During the practical implementation of this project, I resolved several real-world integration roadblocks:
* **Metrics 404 Error:** The default Nginx container didn't expose metrics. **Fix:** Created a custom `nginx.conf` enabling `stub_status` and mounted it via Docker volumes.
* **Alert Triggering Logic:** Alert remained inactive during a crash. **Fix:** Changed Prometheus rule from checking the exporter (`up == 0`) to explicitly checking the Nginx service state (`nginx_up == 0`).
* **Ansible YAML Errors:** Playbook failed to execute due to mapping errors. **Fix:** Corrected strict YAML indentation and spacing rules.
* **Stuck in FIRING State:** Alertmanager's 1-hour repeat interval caused subsequent webhook failures if the initial connection was refused. **Fix:** Kept the Python webhook running as a continuous background process before simulating crashes to ensure 100% HTTP delivery.

## ⚙️ How to Run This Project
**1. Start the Infrastructure:**
```bash
sudo docker-compose up -d

2. Start the Webhook Receiver (in a separate terminal):

Bash
sudo python3 webhook_receiver.py
3. Simulate a System Crash (Test Auto-Healing):

Bash
sudo docker stop my-nginx
Wait a few seconds. Prometheus will detect the downtime, Alertmanager will fire the webhook, and Ansible will automatically bring the Nginx container back to the "Up" state.

Step 2: Push the new changes to GitHub
Now, just run these 3 commands in your terminal to send your updated README to GitHub:

Bash
git add README.md
git commit -m "Updated README with complete project documentation and problem-solving steps"
git push
