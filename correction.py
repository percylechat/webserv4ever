import telnetlib

host = "127.0.0.1"
port = 8082
timeout = 100

# classic post upload
# raw = """POST / HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# filename= "test.txt"
# Content-Lenght: 22 \r\n\r
# hello bebe chat mignon
# """

#classic delete upload
# raw = """DELETE /test.txt HTTP/1.1
# Host: 127.0.0.1:8082
# """

#delete directory
# raw = """DELETE /ugly_cat HTTP/1.1
# Host: 127.0.0.1:8082
# """

#fail method > 405
raw = """BEBE / HTTP/1.1
Host: 127.0.0.1:8082
Content-Type: text/plain
filename= "test.txt"
Content-Lenght: 22 \r\n\r
hello bebe chat mignon
"""

#fail http > 505
# raw = """POST / HTTP/1.0
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# filename= "test.txt"
# Content-Lenght: 22 \r\n\r
# hello bebe chat mignon
# """


#chunked encoding upload
# raw = """GET /ugly_cat/merde.jpg HTTP/1.1
# raw = """POST / HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# <<<<<<< HEAD
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """

raw_byte = str.encode(raw)
with telnetlib.Telnet(host, port, timeout) as session:
    session.write(raw_byte)
    output = session.read_until(b"done", timeout)
    session.close()
    print(output)
    print("Done")