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
// #include "../includes/cgi.hpp"

#include "../includes/response.hpp"

#include <dirent.h>
#include <sys/types.h>
#include <algorithm>

#define MAX_EVENTS 5

std::vector<Bundle_for_response> bfr;

int compare_path(std::string root, std::string page){
    int res = 0;
    if (root.size() > 1)
        root = root.substr(1, root.size() - 1);
    else
        return 1;
    page = page.substr(1, page.size() - 1);
    std::size_t test1 = root.find_first_of("/");
    std::size_t test2 = page.find_first_of("/");
    while (test1 != root.npos && test2 != page.npos){
        std::string check1 = root.substr(0, test1);
        std::string check2 = page.substr(0, test2);
        if (check1 != check2)
            return res;
        res++;
        root = root.substr(test1 + 1, root.size() - test1 + 1);
        page = page.substr(test2 + 1, page.size() - test2 + 1);
        test1 = root.find_first_of("/");
        test2 = page.find_first_of("/");
    }
    return res;
}

Bundle_for_response confirm_used_server(Bundle_for_response bfr, serverConf conf){
    if (conf.http.data()[bfr.specs].size() > 1){
        std::map<std::string,std::map<std::string,std::vector<std::string> > >::iterator it = conf.http.data()[bfr.specs].begin();
        int best = 0;
        int i = 0;
        while (it != conf.http.data()[bfr.specs].end()){
            if (it->first != "server"){
                std::string loc = it->first.substr(9, it->first.size() - 9);
                int test = compare_path(loc, bfr.re.page);
                if (test > best)
                    bfr.loc = it->first;
            }
            i++;
            it++;
        }
    }
    else
        bfr.loc = 1;
    std::size_t j = bfr.specs + 1;
    int best = compare_path(bfr.loc.substr(9, bfr.loc.size() - 9), bfr.re.page);
    while (j < conf.http.size()){
        std::map<std::string,std::map<std::string,std::vector<std::string> > >::iterator it = conf.http.data()[j].begin();
        int i = 0;
        while (it != conf.http.data()[j].end()){
            if (it->first != "server"){
                std::string loc = it->first.substr(9, it->first.size() - 9);
                int test = compare_path(loc, bfr.re.page);
                if (test > best){
                    bfr.loc = it->first;
                    bfr.specs = j;
                }
            }
            i++;
            it++;
        }
        j++;
    }
    bfr.absolut_path = conf.http.data()[bfr.specs][bfr.loc]["root"][0];
    int i = 0;
    int g = 0;
    std::string temp = bfr.loc.substr(9, bfr.loc.size() - 9);
    while (bfr.re.page[i] == temp[g]){
        i++;
        g++;
    }
    if (i >= 1)
        i--;
    bfr.absolut_path.append(bfr.re.page.substr(i, bfr.re.page.size() - i));
    std::size_t d = bfr.re.page.find_last_of(".");
    if (d != bfr.re.page.npos){
        std::string ext = bfr.re.page.substr(d, bfr.re.page.size() - d);
        if (conf.http.data()[bfr.specs][bfr.loc]["cgi"].size() > 0){
            if (ext == conf.http.data()[bfr.specs][bfr.loc]["cgi"][0])
                bfr.re.is_cgi = true;
            else
                bfr.re.is_cgi = false;
        }
        else
            bfr.re.is_cgi = false;
    }
    if (conf.http.data()[bfr.specs]["server"]["client_max_body_size"].size() > 0 && atoi(conf.http.data()[bfr.specs]["server"]["client_max_body_size"][0].c_str()) > 0) {
        int g = atoi(conf.http.data()[bfr.specs]["server"]["client_max_body_size"][0].c_str());
        {
            if (static_cast< int >(bfr.re.body.size()) > g)
                bfr.re.error_type = 413;
        }
    }
    if (conf.http.data()[bfr.specs][bfr.loc]["methods"].size() > 0){
        std::size_t h = 0;
        int cont = 0;
        while (conf.http.data()[bfr.specs][bfr.loc]["methods"].size() > h){
            if (conf.http.data()[bfr.specs][bfr.loc]["methods"][h] == bfr.re.type)
                cont++;
            h++;
        }
        if (cont == 0)
            bfr.re.error_type = 405;
    }
    return bfr;
}

int check_conn(int fd_1, Socket *serv, int nbr){
    int i = 0;
    while (i < nbr){
        if (fd_1 == serv[i].get_fd())
            return i;
        i++;
    }
    return -1;
}

int fd_in_queue(int fd, int queue){
    struct epoll_event event;
    event.events = EPOLLIN | EPOLLRDHUP;
    event.data.fd = fd;
    if (epoll_ctl(queue, EPOLL_CTL_ADD, fd, &event)){
        close(fd);
        return -1;
    }
    return 0;
}

void poll_handling(int epoll_fd, const int fd, struct epoll_event *event, Socket *serv, serverConf conf)
{
    int j = check_conn(fd, serv, conf.http.size());
    Socket sock[1];
    sock[0].fd_sock = fd;
    if (j != -1)
    {
        unsigned int i = 0;
        while (i != bfr.size() && bfr[i].fd_listen != fd)
            i++;
        int clientsocket = sock[0].server_accept();
        Socket test[1];
        test[0].fd_sock = clientsocket;
        if (fcntl(test[0].fd_sock, F_SETFL, O_NONBLOCK) < 0)
            return ;
        if (fd_in_queue(test[0].fd_sock, epoll_fd))
            return ;
        bfr[i].fd_accept = test[0].fd_sock;
    }
    else if (event->events & EPOLLRDHUP){
        unsigned int i = 0;
        while (i != bfr.size() && bfr[i].fd_read != fd)
            i++;
//TO DO clear request or delete
        // bfr[i].init_re();
        close(sock[0].fd_sock);
    }
    else if (event->events & EPOLLOUT){
        unsigned int i = 0;
        while (i != bfr.size() && bfr[i].fd_read != fd)
            i++;
        int ret;
        if (bfr[i].re.status_is_handled == false){
            std::string content = get_response(bfr[i], conf);
            // std::cout << "response= " << content << std::endl;
            ret = send(sock[0].fd_sock, content.c_str(), content.size(), 0);
            if (ret == 0){
                close(sock[0].fd_sock);
                exit(0);
                // close(bfr[i].fd_read);
            }
            if (ret == 0 || ret == -1)
                return ;
            close(sock[0].fd_sock);
        }
    }
    else if (event->events & EPOLLIN){
        unsigned int i = 0;
        while (i < bfr.size() && (bfr[i].fd_accept != fd)){
            i++;
        }
        int ret = 0;
        char buffer[3000];
// TO DO find way either to adapt buffer size or to limit if not big enough or else buffer overflow
        bzero(buffer, sizeof(buffer));
        ret = recv(sock[0].fd_sock, buffer, sizeof(buffer), MSG_DONTWAIT);
        // std::cout << buffer << std::endl;
        if (ret == -1)
// TO DO handle failed recv
            return ;
        first_dispatch(buffer, &(bfr[i].re));
        bfr[i] = confirm_used_server(bfr[i], conf);
        if (bfr[i].re.status_is_finished == true)
        {
            event->events = EPOLLOUT;
            epoll_ctl(epoll_fd, EPOLL_CTL_MOD, sock[0].fd_sock, event);
            bfr[i].fd_read = sock[0].fd_sock;
        }
    }
    else
        ;
    return ;
}

int launch(serverConf conf){
    struct epoll_event event;
    struct epoll_event events[MAX_EVENTS]; // number of fd attended at same time, here 5
    unsigned int event_count;
    const char *check = NULL;

    std::string home = "127.0.0.1";
    int queue = epoll_create1(EPOLL_CLOEXEC);
    if (queue == -1){
        std::cout << "Error: queue handler epoll couldn't be created" << std::endl;
        return 1;
    }
    std::size_t i = 0;
    Socket serv[conf.http.size()];
    while (i < conf.http.size()){
        std::size_t j = 0;
        while (j < conf.http.data()[i]["server"]["listen"].size()){
            int port = atoi(conf.http.data()[i]["server"]["listen"][j].c_str());
            check = serv[i].create_socket(port, INADDR_ANY);
            if (check == NULL){
                check = serv[i].server_binding();
                if (check != NULL){
                    std::cout << check << std::endl;
                    return 1;
                }
                if (fcntl(serv[i].get_fd(), F_SETFL, O_NONBLOCK) < 0){
                    std::cout << "Error setting nonblocking socket" << std::endl;
                    return 1;
                }
                check = serv[i].server_listening(5); // only 5 waiting conneions authorized so the server is not overcharged
                if (check != NULL){
                    std::cout << check << std::endl;
                    return 1;
                }
                event.events = EPOLLIN;
                event.data.fd = serv[i].get_fd();
                if (epoll_ctl(queue, EPOLL_CTL_ADD, serv[i].get_fd(), &event)){
                    close(serv[i].get_fd());
                    std::cout << "Failed to add file descriptor to epoll\n" << std::endl;
                    return -1;
                }
                Bundle_for_response one;
                one.init_re();
                one.fd_listen = serv[i].get_fd();
                one.specs = i;
                bfr.push_back(one);
            }
            j++;
        }
        i++;
    }
    while (1){
        event_count = epoll_wait(queue, events, MAX_EVENTS, -1);
        i = 0;
        while (i < event_count){
            poll_handling(queue, events[i].data.fd, &events[i], serv, conf);
            i++;
        }
    }
    close(queue);
    return 0;
}

void signalHandler( int signum ) {
   std::cout << "Closing Webserv\nGoodbye!" << std::endl;
   exit(signum);  
}

int main(int argc, char *argv[]){
    if (argc != 2){
        std::cout << "ERROR, conf file missing" << std::endl;
    }
    signal(SIGINT, signalHandler);
    serverConf conf = start_conf(argv[1]);
    if (!conf._valid){
        std::cout << "This configuration file is invalid" << std::endl;
        return 1;
    }
    return launch(conf);
}