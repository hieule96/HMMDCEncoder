#ifndef _TMDCQPTable_
#define _TMDCQPTable_
#pragma once

#include <string>
#include <fstream>
#include "TLibCommon/TComDataCU.h"
#include "TLibCommon/TComSlice.h"

class TMDCQPTable{
    public:
        TMDCQPTable(Int nbElementReadLine,const char* QPFileName,const char* QtreeFileName);
        Int readALineQp();
        UInt* getQPArray(){return qpArray;}
        Int readALineQtree();
        UInt* getQtreeArray(){return qtreeArray;}
        void setIndexQpCU(Int index) { indexQpCU = index; }
        Int convertStringToIntArrayQP(UInt *bufferDest, char *str,int nbElement);
        Int convertStringtoIntArrayQtree(UInt *bufferDest, char *str,int nbElement);
        void appendQPArray(Int QP);
        ~TMDCQPTable();
        static TMDCQPTable* getInstance() {return m_instance;}
        static TMDCQPTable* initInstance(Int nbElementReadLine,const char* QPFileName, const char* QtreeFileName){
            if (m_instance==NULL){
                m_instance = new TMDCQPTable(nbElementReadLine,QPFileName,QtreeFileName); 
            }
            return m_instance;
        }
    private:
        UInt* qpArray;
        UInt* qtreeArray;
        Int indexQpCU;
        Int indexCU;
        Int m_QPArraySize;
        std::ifstream fpQPFile;
        std::ifstream fpQtreeFile;
        static TMDCQPTable* m_instance;
};


#endif
