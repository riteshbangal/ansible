
http://localhost:8080/ -->
 kubectl get secret awx-demo-admin-password -o jsonpath="{.data.password}" | base64 --decode

export AWX_ADMIN_PASSWORD=$(kubectl get secret awx-demo-admin-password -n awx -o jsonpath="{.data.password}" | base64 --decode)
curl -v -u admin:<pass> http://localhost:8080/api/v2/
----------------------------------

Basic Authentication (Username & Password)
curl -v -u admin:$AWX_ADMIN_PASSWORD http://localhost:8080/api/v2/

Token-Based Auth
curl -v -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$AWX_ADMIN_PASSWORD\"}" \
    -u admin:$AWX_ADMIN_PASSWORD \
    http://localhost:8080/api/v2/tokens/


Get the Token and Store It in a Variable
export AWX_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$AWX_ADMIN_PASSWORD\"}" \
    -u admin:$AWX_ADMIN_PASSWORD \
    http://localhost:8080/api/v2/tokens/ | jq -r '.token')


Verify the Token
echo $AWX_TOKEN


Use the Token in API Requests
curl -v -H "Authorization: Bearer $AWX_TOKEN" http://localhost:8080/api/v2/jobs/

Get the inventories
curl -H "Authorization: Bearer $AWX_TOKEN" http://localhost:8080/api/v2/inventories/ | jq .

Create an Inventory 
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AWX_TOKEN" \
    -d '{
          "name": "my-vms",
          "description": "Inventory for managing my virtual machines",
          "organization": 1
        }' \
    http://localhost:8080/api/v2/inventories/ | jq .


Add the Host to the Inventory
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AWX_TOKEN" \
  -d '{
        "name": "192.168.64.9", 
        "inventory": 2, 
        "enabled": true, 
        "variables": "{\"ansible_host\": \"192.168.64.9\"}"
      }' \
  http://localhost:8080/api/v2/hosts/ | jq .

List Hosts from Inventory ID 2
curl -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/inventories/2/hosts/ | jq .


Set Up the Ansible Project in AWX
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AWX_TOKEN" \
    -d '{
          "name": "apache-automation",
          "description": "Ansible project for managing Apache server",
          "organization": 1,  # Replace with your organization ID
          "scm_type": "git",
          "scm_url": "https://github.com/riteshbangal/ansible.git",
          "scm_branch": "develop",  # Replace with the branch you are using
          "credential": 1  # Replace with the ID of your credentials
        }' \
    http://localhost:8080/api/v2/projects/ | jq .



Create the Credential
curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer $AWX_TOKEN" \
-d '{
        "name": "my-vms-ssh",
        "description": "SSH key for my-vms",
        "organization": 1, 
        "credential_type": 1,
        "inputs": {
        "username": "your-ssh-username",
        "password": "your-ssh-password",
        "ssh_key_data": "-----BEGIN OPENSSH PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END OPENSSH PRIVATE KEY-----\n"
        }
    }' \
http://localhost:8080/api/v2/credentials/ | jq .


curl 'http://localhost:8080/api/v2/credentials/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9,es;q=0.8,nl;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'userLoggedIn=true; csrftoken=rAX36YNdtjJj49tEzg8hSlZrJJnNACRC; awx_sessionid=cafrin3900b8nnvgdjmbi882l4uroy6c' \
  -H 'Origin: http://localhost:8080' \
  -H 'Referer: http://localhost:8080/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36' \
  -H 'X-CSRFToken: rAX36YNdtjJj49tEzg8hSlZrJJnNACRC' \
  -H 'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"inputs":{"username":"ubuntu","password":"","ssh_key_data":"-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAQEAz2nyMZfKuBe1rPUOFB6qki5IX2cCFq7R/fOZIuCy0ltAl+Stowg1\nzGJ0Opf+hBM3/6NfmLbGHBfqwy/nDvvWfHbpAZK2p2NhEpZs9yd2W/CiqGzNOATYWdSqgV\nXEvuVzq8pGBnVabM4cdn3ACgu+tvRYuM3Xv5wOgDtNrktSOq+iqHLcizwKt3Abt7TxLZqQ\n84QOiF4Q6XhVaBPnXhgdECGuE6+Xw16oFEzQIt79m7ta3GT5QJeSFtjQRm8n6fxg0SI09H\nY8++g1FQdmXT7AdOGSrpd/EEEQ................coAEKCofsRUS8sLtn0LenC8y6GmTPQGwkdkKRhP+CBE\nq0CZVgqyherSprj5xa6nFENkE+My2WixakVEAzIdy7BEabowAAAIEA0f10n2u7chwuWVHf\neGgrr0n4BVt7v0mDq/6eOq1es2lpVBOyZxTbx3YdW45Vghq35K7DxHACrQC3w17LCEc6lF\noS9/dGK3m1z5Q/413407V+gt1k8tX6Zx8GBIkxe43K28lUeBdfxHgibOwd1KRylC+nTrcn\niEVrVlzq90+yT9UAAAAfcml0ZXNoY2hhbmRyYWJhbmdhbEBSaXRlc2hzLU1CUAECAwQ=\n-----END OPENSSH PRIVATE KEY-----","ssh_public_key_data":"","ssh_key_unlock":"","become_method":"","become_username":"","become_password":""},"name":"my-vms-ssh","description":"SSH key-based access to my-vms","isOrgLookupDisabled":false,"credential_type":1,"organization":1}'



  Verify credentials
  curl -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/credentials/3/ | jq .


Create the Project via API:
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AWX_TOKEN" \
    -d '{
          "name": "apache-automation",
          "description": "Project to manage Apache server using Ansible",
          "organization": 1,
          "scm_type": "git",
          "scm_url": "https://github.com/riteshbangal/ansible.git",
          "scm_branch": "master",
          "scm_update_on_launch": true
        }' \
    http://localhost:8080/api/v2/projects/ | jq .


Get the project:
curl -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/projects/8/ | jq .

Create the Job Template via API:
curl -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AWX_TOKEN" \
    -d '{
          "name": "apache-setup",
          "description": "Setup and manage Apache server",
          "job_type": "run",
          "inventory": 2,
          "project": 8,
          "playbook": "ansible-project/apache-automation/playbooks/site.yml",
          "credential": 3
        }' \
    http://localhost:8080/api/v2/job_templates/ | jq .

curl 'http://localhost:8080/api/v2/job_templates/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9,es;q=0.8,nl;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'userLoggedIn=true; csrftoken=rAX36YNdtjJj49tEzg8hSlZrJJnNACRC; awx_sessionid=cafrin3900b8nnvgdjmbi882l4uroy6c' \
  -H 'Origin: http://localhost:8080' \
  -H 'Referer: http://localhost:8080/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36' \
  -H 'X-CSRFToken: rAX36YNdtjJj49tEzg8hSlZrJJnNACRC' \
  -H 'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"allow_callbacks":false,"allow_simultaneous":false,"ask_credential_on_launch":false,"ask_diff_mode_on_launch":false,"ask_execution_environment_on_launch":false,"ask_forks_on_launch":false,"ask_instance_groups_on_launch":false,"ask_inventory_on_launch":false,"ask_job_slice_count_on_launch":false,"ask_job_type_on_launch":false,"ask_labels_on_launch":false,"ask_limit_on_launch":false,"ask_scm_branch_on_launch":false,"ask_skip_tags_on_launch":false,"ask_tags_on_launch":false,"ask_timeout_on_launch":false,"ask_variables_on_launch":false,"ask_verbosity_on_launch":false,"become_enabled":false,"description":"Setup and manage Apache server","diff_mode":false,"extra_vars":"---\n","forks":0,"host_config_key":"","job_slice_count":1,"job_tags":"","job_type":"run","limit":"","name":"apache-setup","playbook":"ansible-project/apache-automation/playbooks/manage_apache.yml","prevent_instance_group_fallback":false,"scm_branch":"","skip_tags":"","timeout":0,"use_fact_cache":false,"verbosity":"0","webhook_service":"","execution_environment":1,"project":8,"inventory":2}'

find the Job Template ID
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/job_templates/9/ | jq .


Launch the Job Template
curl -v -X POST -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/job_templates/9/launch/ | jq .


Monitor the Job
curl -X GET -H "Authorization: Bearer $AWX_TOKEN" \
    http://localhost:8080/api/v2/jobs/9/ | jq .
