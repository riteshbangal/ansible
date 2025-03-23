
http://localhost:8080/ -->
 kubectl get secret awx-demo-admin-password -o jsonpath="{.data.password}" | base64 --decode
eT58G0SYIiEr6p0lHkoQsLipVQykZZiB%

export AWX_ADMIN_PASSWORD=$(kubectl get secret awx-demo-admin-password -n awx -o jsonpath="{.data.password}" | base64 --decode)
curl -v -u admin:eT58G0SYIiEr6p0lHkoQsLipVQykZZiB% http://localhost:8080/api/v2/
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