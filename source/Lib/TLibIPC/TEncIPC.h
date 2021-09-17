#ifndef __TENCIPC__
#define __TENCIPC__

#include <zmq.h>
#include "TLibCommon/TComDataCU.h"

class TEncIPC {
    private:
        void *context;
        void *requester;
    public:
        TEncIPC(){
            
        };
        ~TEncIPC(){
            close_conection();
        };
        void connect(const char * addr);
        Int send(UInt *buff, Int size);
        Int receive(UInt *buff, Int size);
        void close_conection(); 
};

#endif