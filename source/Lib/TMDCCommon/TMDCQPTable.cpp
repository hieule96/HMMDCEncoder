#include "TMDCQPTable.hpp"
#define BUFFER_READ_SIZE 1024
TMDCQPTable* TMDCQPTable::m_instance = NULL;

TMDCQPTable::TMDCQPTable(Int nbElementReadLine,const char * QPFileName,const char * QtreeFileName){
        qpArray = new UInt [nbElementReadLine];
        qtreeArray = new UInt[nbElementReadLine];
        memset(qpArray, 0, nbElementReadLine * sizeof(UInt));
        memset(qtreeArray, 0, nbElementReadLine * sizeof(UInt));
        indexQpCU = 0;
        indexCU = 0;
        m_QPArraySize = nbElementReadLine;
        fpQtreeFile.open(QtreeFileName);
        if (fpQtreeFile.fail()) {
            std::cerr << "Cannot open file : " << QtreeFileName << std::endl;
            exit(EXIT_FAILURE);
        }
        fpQPFile.open(QPFileName);
        if (fpQPFile.fail()){
            std::cerr << "Cannot open file : " << QPFileName <<std::endl;
            exit(EXIT_FAILURE);
        }
}


void TMDCQPTable::appendQPArray(Int QP) {
    if (indexQpCU < m_QPArraySize) {
        qpArray[indexQpCU++] = QP;
    }
}


void TMDCQPTable::convertStringToIntArrayQP(UInt *bufferDest, char *str,int nbElement){
    int j = 0;
    for (int i = 0; i < nbElement; i++) {
        bufferDest[i] = 0;
    }
    for (int i = 0; i < nbElement&&str[i]!='\n'&&str[i]!='\0';i++){

        if (str[i] == ' '){
            j++;
        }
        else
        {
            bufferDest[j] = bufferDest[j]*10 + (str[i] - 48);
        }
    }
}

// TODO: See if there's a better way to organize this file
void TMDCQPTable::convertStringtoIntArrayQtree(UInt *bufferDest, char *str,int nbElement){
    int j = -1;
    bool skip = false;
    for (int i = 0; i < nbElement; i++) {
        bufferDest[i] = 0;
    }
    for (int i = 0; i < nbElement&&str[i]!='\n'&&str[i]!='\0';i++){
        //special character skip
        if (str[i]=='<'){
            skip = true;
        }
        if (str[i]=='>')
         {   //skip first space
            i++;
            skip = false;
            }
        if (skip)
        {
            continue;
        }
        if (str[i] == ' '){
            j++;
        }
        else
        {
            bufferDest[j] = bufferDest[j]*10 + (str[i] - 48);
        }
    }
}

// read a buffer of 1024 of a line
UInt* TMDCQPTable::readALineQtree(){
    char* buffer = new char[BUFFER_READ_SIZE];
    if (fpQtreeFile.is_open()){
        fpQtreeFile.getline(buffer, BUFFER_READ_SIZE);
    }
    else
    {
        std::cerr << "Unexpected closed file" << std::endl;
        exit(EXIT_FAILURE);
    }
    // parse String Int
    convertStringtoIntArrayQtree(qtreeArray,buffer, BUFFER_READ_SIZE);
    delete[] buffer;
    return qtreeArray;
}

UInt* TMDCQPTable::readALineQp(){
    char* buffer = new char[BUFFER_READ_SIZE];
    // get the buffer from the file
    if(fpQPFile.is_open()){
        fpQPFile.getline(buffer, BUFFER_READ_SIZE);
    }
    else
    {
        std::cerr << "Unexpected closed file" << std::endl;
        exit(EXIT_FAILURE);
    }
    //parsing this buffer
    convertStringToIntArrayQP(qpArray,buffer,BUFFER_READ_SIZE);
    delete[] buffer;
    return qpArray;
}
TMDCQPTable::~TMDCQPTable(){
    delete [] qpArray;
    delete [] qtreeArray;
    fpQtreeFile.close();
    fpQPFile.close();
}