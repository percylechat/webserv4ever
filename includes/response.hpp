#include "../includes/socket.hpp"
#include <stdio.h>
#include <unistd.h>
#include <sys/epoll.h> // queue handling
// #include "request.hpp"
#include <vector>
#include <cstdlib>
#include <cstring>
#include <sstream>

#include <fcntl.h>
// #include "../parsing_conf.hpp"
// #include "request.hpp"
#include "../includes/cgi.hpp"

#include <dirent.h>
#include <sys/types.h>
#include <algorithm>

std::string get_response(Bundle_for_response bfr, serverConf conf);