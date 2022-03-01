import telnetlib

host = "127.0.0.1"
port = 8082
timeout = 100

# classic post upload
raw = """POST / HTTP/1.1
Host: 127.0.0.1:8082
Content-Type: text/plain
filename= "test.txt"
Content-Lenght: 22 \r\n\r
hello bebe chat mignon
"""

#classic delete upload
# raw = """DELETE /test.txt HTTP/1.1
# Host: 127.0.0.1:8082
# """

#delete directory
# raw = """DELETE /ugly_cat HTTP/1.1
# Host: 127.0.0.1:8082
# """

#fail method > 405
# raw = """BEBE / HTTP/1.1
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
# 404 NOT FOUND ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """GET / HTTP/1.0
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 505 HTTP VERSION NOT SUPPORTED - ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """GET / HTTP/1.0
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 505 HTTP VERSION NOT SUPPORTED - ERROR PAGE NOT FOUND IN CONF FILE
# OK

# raw = """GET /ugly_cat/graphic_design.jpg HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 200 OK
# OK

# raw = """GET index.html HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 200 OK
# NOT OK

# raw = """GET /ugly_cat/unknown.jpg HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 404 NOT FOUND - ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """GET /ugly_cat/unknown.jpg HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 404 NOT FOUND - ERROR PAGE NOT FOUND IN CONF FILE
# OK

# raw = """GET /ugly_cat/percy.jpg HTTP/1.1
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 400 BAD REQUEST - ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """GET /ugly_cat/percy.jpg HTTP/1.1
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 400 BAD REQUEST - ERROR PAGE PATH INCORRECT IN CONF FILE
# OK

# raw = """PUT /index.html HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 405 METHOD NOT ALLOWED - ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """RANDOMMETHOD /index.html HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 405 METHOD NOT ALLOWED - ERROR PAGE PATH INCORRECT IN CONF FILE
# NOT OK

# raw = """DELETE /ugly_cat/ HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 403 FORBIDDEN - ERROR PAGE FOUND IN CONF FILE
# OK

# raw = """DELETE /ugly_cat/ HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 403 FORBIDDEN - ERROR PAGE NOT FOUND IN CONF FILE
# OK

# raw = """DELETE /ugly_cat/mdr.jpg HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 500 INTERNAL SERVER ERROR - ERROR PAGE FOUND IN CONF FILE
# NOT OK

# raw = """DELETE /ugly_cat/mdr.jpg HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# Content-Length: 1000
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n
# """
# 500 INTERNAL SERVER ERROR - ERROR PAGE NOT FOUND IN CONF FILE
# =======
# 26\r\nVoici les donnees du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 0\r\r\n
# """

#error method
# raw = """PUT / HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# filename= "test.txt"
# Content-Lenght: 22 \r\n\r
# hello bebe chat mignon
# """

#error content lenght
# raw = """POST / HTTP/1.1
# Host: 127.0.0.1:8082
# Content-Type: text/plain
# <<<<<<< HEAD
# filename= "test.txt"\r\n\r
# hello bebe chat mignon
# =======
# filename= "hello.txt"
# Transfer-Encoding: chunked\r\n\r
# 26\r\nVoici les données du premier morceau\r\n\r
# 1C\ret voici un second morceau\r\n\r\n
# 20\ret voici deux derniers morceaux \r\n
# 12\r\sans saut de ligne\r\n
# 0\r\r\n


raw_byte = str.encode(raw)
with telnetlib.Telnet(host, port, timeout) as session:
    session.write(raw_byte)
    output = session.read_until(b"done", timeout)
    session.close()
    print(output)
    print("Done")