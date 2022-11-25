#ifndef _TMDCQPTable_
#define _TMDCQPTable_
#pragma once

#include <string>
#include <fstream>
#include "TLibCommon/TComDataCU.h"
#include "TLibCommon/TComSlice.h"

class TMDCQPTable{
    public:
        TMDCQPTable(Int nbElementReadLine,const char* QPFileName1,const char* QPFileName2,const char* QtreeFileName);
        TMDCQPTable(Int nbElementReadLine,const char * QPFileName);
        Int readALineQp(Int iQPFile);
        Int* getQPArray(){return qpArray;}
        Int readALineQtree();
        Int readStdIn();
        UInt* getQtreeArray(){return qtreeArray;}
        Int convertStringToIntArrayQP(Int *bufferDest, char *str,int nbElement);
        Int convertStringtoIntArrayQtree(UInt *bufferDest, char *str,int nbElement);
        Int getCturs() {return this->m_cturs;};
        Void resetCturs() {this->m_cturs=0;};
        Int getCountQP() {return this->m_countQPArr;};
        Int getCountQtree(){return this->m_countQtreeArr;};
        void appendQPArray(Int QP);
        ~TMDCQPTable();
        static TMDCQPTable* getInstance() {return m_instance;}
        static TMDCQPTable* initInstance(Int nbElementReadLine,const char* QPFileName1,const char* QPFileName2, const char* QtreeFileName){
            if (m_instance==NULL){
                m_instance = new TMDCQPTable(nbElementReadLine,QPFileName1,QPFileName2,QtreeFileName); 
            }
            return m_instance;
        }
    private:
        Int* qpArray;
        UInt* qtreeArray;
        Int m_cturs;
        Int m_countQPArr;
        Int m_countQtreeArr;
        std::ifstream fpQPFile1;
        std::ifstream fpQPFile2;
        std::ifstream fpQtreeFile;
        static TMDCQPTable* m_instance;
};


#endif
