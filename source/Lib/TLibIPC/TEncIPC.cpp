#include "TEncIPC.h"

void TEncIPC::connect(const char * addr){
    context = zmq_ctx_new ();
    requester = zmq_socket (context, ZMQ_REQ);
    zmq_connect (requester, "tcp://localhost:5555");
}

Int TEncIPC::send(UInt *buff, Int size){
    return zmq_send (requester,buff, size, 0);
}

Int TEncIPC::receive(UInt *buff,Int size){
    return zmq_recv (requester, buff, size, 0);
}

void TEncIPC::close_conection(){
    zmq_close (requester);
    zmq_ctx_destroy (context);
}