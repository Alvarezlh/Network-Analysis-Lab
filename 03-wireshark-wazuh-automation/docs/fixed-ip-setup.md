# Fixed IP on Kali Linux (NetworkManager)

## Why

With DHCP, the IP addresses of the lab machines change between sessions. That breaks the Wazuh Agent connection (it keeps pointing to an old Manager address) and leaves configuration files out of date. A fixed IP removes the problem.

Kali Linux uses NetworkManager, not Netplan, so `/etc/netplan` does not exist. The configuration is done with `nmcli`.

## Steps

1. **Collect the current values:**
```bash
   ip -4 a
   ip route show default | awk '{print $3}'
   sudo nmcli connection show
```
   Write down the IP, the gateway, and the **NAME** column of the active connection (for example `Wired connection 1`).

   `nmcli` uses the connection **name**, not the device name. Using `eth0` fails if the connection is called `Wired connection 1`.

2. **Set the static address** (replace the placeholders with your values):
```bash
   sudo nmcli con mod "Wired connection 1" \
     ipv4.method manual \
     ipv4.addresses <KALI_IP>/24 \
     ipv4.gateway <GATEWAY_IP> \
     ipv4.dns "1.1.1.1,8.8.8.8"
```

3. **Apply the change:**
```bash
   sudo nmcli con up "Wired connection 1"
```

4. **Verify:**
```bash
   ip -4 a show eth0
   ping -c 3 1.1.1.1
```
   The interface must show the address without the `dynamic` flag, and the ping must answer.

## Notes

- Choose an address outside the router's DHCP range, or reserve it in the router, so that no other device receives the same address.
- The Wazuh Manager VM also needs a fixed IP. The method depends on the operating system of the VM.
- After fixing the addresses, make sure the `<address>` field in the agent's `/var/ossec/etc/ossec.conf` points to the Manager's fixed IP.