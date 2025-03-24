# AWX API Automation Flow

## **🚀 Regular Operational Flow in AWX**

1. **Validate the inventory**  
2. **Validate the hosts**  
3. **Validate the credentials**  
4. **Sync the project repository**  
5. **Launch a job template**  
6. **Monitor the job execution**  
7. **Fetch job logs for debugging**  
8. **(Optional) Retrieve job results and execution history**  

## **📌 Additional Enhancements**
- **🔄 Auto-retry failed jobs**
- **📢 Notification System (Slack/Email alerts)**
- **📊 Generate reports on execution stats**
- **📅 Schedule automation jobs**
- **📎 Implement Role-Based Access Control (RBAC)**

---

## **🔄 Detailed API Flow for Automation**

# AWX API Automation Flow

## Validate If AWX Is Running (Pre-check)
Before making API calls, check if AWX is running.

```sh
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/v2/ping/
```

Response 200: AWX is running. Other responses: AWX might be down or have issues.

## Authentication

### Basic Authentication (Username & Password)
```sh
curl -v -u admin:$AWX_ADMIN_PASSWORD http://localhost:8080/api/v2/
```

### Token-Based Auth
```sh
curl -v -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$AWX_ADMIN_PASSWORD\"}" \
    -u admin:$AWX_ADMIN_PASSWORD \
    http://localhost:8080/api/v2/tokens/
```

### Get the Token and Store It in a Variable
```sh
export AWX_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$AWX_ADMIN_PASSWORD\"}" \
    -u admin:$AWX_ADMIN_PASSWORD \
    http://localhost:8080/api/v2/tokens/ | jq -r '.token')
```

### Verify the Token
```sh
[ -n "$AWX_TOKEN" ] && echo "Token retrieved successfully" || echo "Failed to retrieve token"
```

### Use the Token in API Requests
```sh
curl -v -H "Authorization: Bearer $AWX_TOKEN" http://localhost:8080/api/v2/jobs/
```


### **1️⃣ Validate the Inventory**
Ensure the inventory exists before launching a job.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/inventories/2/
```
- Check if the inventory is `enabled: true`.

---

### **2️⃣ Validate the Hosts**
Ensure all hosts in the inventory are reachable.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/inventories/2/hosts/
```
- Validate that the list contains expected hosts.
- Check their `enabled` status.

---

### **3️⃣ Validate the Credentials**
Ensure SSH keys or passwords are correctly configured.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/credentials/3/
```
- If `inputs` contain `"ssh_key_data": null`, credentials are missing.

---

### **4️⃣ Sync the Project Repository**
Ensure your playbook repository is up to date.

#### **API Endpoint**
```bash
curl -X POST -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/projects/8/update/
```
- If the job fails, check logs for Git issues.

---

### **5️⃣ Launch a Job Template**
Start a job that executes a playbook.

#### **API Endpoint**
```bash
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AWX_TOKEN" \
    -d '{}' \
    http://localhost:8080/api/v2/job_templates/9/launch/
```
- Save `job_id` from the response.

---

### **6️⃣ Monitor the Job Execution**
Check if the job is running or has failed.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/jobs/9/
```
- Look for `"status": "running"` or `"successful"`.

---

### **7️⃣ Fetch Job Logs for Debugging**
Get detailed logs for troubleshooting.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/jobs/9/stdout/?format=txt
```

---

### **8️⃣ Retrieve Job Results and Execution History**
For tracking and reporting.

#### **API Endpoint**
```bash
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/jobs/
```
- Filters can be applied (e.g., `?status=failed`).

---

## **📌 Summary of the Flow**

| Step  | Action |
|-------|--------|
| ✅ **1** | Validate the inventory |
| ✅ **2** | Validate the hosts |
| ✅ **3** | Validate credentials |
| 🔄 **4** | Sync the project repository |
| 🚀 **5** | Launch the job template |
| 👀 **6** | Monitor job execution |
| 📝 **7** | Fetch job logs |
| 📊 **8** | Retrieve job history |

---

### **💡 Additional Enhancements**
✅ **Implement Auto-Retry for Failed Jobs**  
✅ **Automate Reporting with a Summary Dashboard**  
✅ **Schedule Critical Jobs (e.g., Apache health check every 6 hours)**  
✅ **Integrate with Slack/Email for Job Status Alerts**


## Project Structure

ansible-automation-api/
│── main.py
│── auth.py
│── awx_status.py
│── inventory.py
│── config.py
│── requirements.txt
│── logs/
└── utils/
    ├── logger.py
