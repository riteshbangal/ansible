# README: Setting up QEMU with Alpine Linux and Ansible on MacBook

## Prerequisites
Ensure you have Homebrew installed on your MacBook. If not, install it using:
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Install QEMU
```sh
brew install qemu
```

## Download Alpine Linux ISO
```sh
curl -O https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-standard-3.18.0-x86_64.iso
```

## Create a Virtual Disk
```sh
qemu-img create -f qcow2 alpine.qcow2 2G
```

## Start QEMU with Alpine Linux
```sh
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -netdev user,id=net0 -device e1000,netdev=net0 \
  -cdrom alpine-standard-3.18.0-x86_64.iso \
  -hda alpine.qcow2 \
  -boot d \
  -nographic
```

## Install Alpine Linux
1. Once the VM boots, login as `root`.
2. Run `setup-alpine` to configure the system.
3. Follow the prompts to:
   - Set hostname
   - Configure network
   - Set root password
   - Choose a package mirror
   - Enable SSH (optional)
   - Install the system to disk (`sys` mode)
4. Reboot the VM after installation.

## Boot Alpine from Disk
```sh
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -netdev user,id=net0 -device e1000,netdev=net0 \
  -hda alpine.qcow2 \
  -boot c \
  -nographic
```

## Install Ansible on MacBook
```sh
brew install ansible
```

## Enable SSH on Alpine VM
1. Login to the VM and install OpenSSH:
   ```sh
   apk add openssh
   ```
2. Start and enable the SSH service:
   ```sh
   rc-service sshd start
   rc-update add sshd
   ```
3. Find the VM IP address:
   ```sh
   ip a
   ```

## Connect from MacBook to Alpine VM
```sh
ssh root@<VM_IP>
```

## Configure Ansible to Manage Alpine VM
1. Add the VM to Ansible's inventory:
   ```sh
   echo "alpine ansible_host=<VM_IP> ansible_user=root" >> inventory
   ```
2. Test the connection:
   ```sh
   ansible alpine -i inventory -m ping
   ```

## Next Steps
- Use Ansible to automate package installation and configuration.
- Deploy additional software or services on your Alpine VM.
- Configure persistent networking for better SSH access.

### Notes
- If you need to forward SSH ports for easier access, modify your QEMU command with `-netdev user,id=net0,hostfwd=tcp::2222-:22`.
- To stop the VM, use `poweroff` inside the VM or `Ctrl+A X` in the terminal.

Let me know if you need any modifications!


----------------------------------
local-alpine.vm.dev
root/ Admin@12345

----------------------------------
