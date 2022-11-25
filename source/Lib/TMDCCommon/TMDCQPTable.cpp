#include "TMDCQPTable.hpp"
#include <stdexcept>

#define BUFFER_READ_SIZE 1024
TMDCQPTable* TMDCQPTable::m_instance = NULL;

TMDCQPTable::TMDCQPTable(Int nbElementReadLine,const char * QPFileName1,const char *QPFileName2,const char * QtreeFileName){
        qpArray = new Int [nbElementReadLine];
        qtreeArray = new UInt[nbElementReadLine];
        this->m_cturs = 0;
        this->m_countQPArr = 0;
        this->m_countQtreeArr = 0;
        memset(qpArray, 0, nbElementReadLine * sizeof(Int));
        memset(qtreeArray, 0, nbElementReadLine * sizeof(UInt));
        fpQtreeFile.open(QtreeFileName);
        if (fpQtreeFile.fail()) {
            std::cerr << "Cannot open file : " << QtreeFileName << std::endl;
            exit(EXIT_FAILURE);
        }
        fpQPFile1.open(QPFileName1);
        if (fpQPFile1.fail()){
            std::cerr << "Cannot open file : " << QPFileName1 <<std::endl;
            exit(EXIT_FAILURE);
        }
        fpQPFile2.open(QPFileName1);
        if (fpQPFile2.fail()){
            std::cerr << "Cannot open file : " << QPFileName1 <<std::endl;
            exit(EXIT_FAILURE);
        }
}


Int TMDCQPTable::convertStringToIntArrayQP(Int *bufferDest, char *str,int nbElement){
    int j = 0;
    for (int i = 0; i < nbElement; i++) {
        bufferDest[i] = 0;
    }
    for (int i = 0; i < nbElement&&str[i]!='\n'&&str[i]!='\0';i++){

        if (str[i] == ','){
            j++;
        }
        else
        {
            bufferDest[j] = bufferDest[j]*10 + (str[i] - 48);
        }
    }
    return j;
}

// TODO: See if there's a better way to organize this file
Int TMDCQPTable::convertStringtoIntArrayQtree(UInt *bufferDest, char *str,int nbElement){
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
    return j;
}

// read a buffer of 1024 of a line
Int TMDCQPTable::readALineQtree(){
    this->m_cturs++;
    char* buffer = new char[BUFFER_READ_SIZE];
    if (fpQtreeFile.is_open()){
        fpQtreeFile.getline(buffer, BUFFER_READ_SIZE);
    }
    else
    {
        throw std::runtime_error("readALineQtree: Unexpected closed file");
    }
    // parse String Int
    this->m_countQtreeArr = convertStringtoIntArrayQtree(qtreeArray,buffer, BUFFER_READ_SIZE);
    delete[] buffer;
    return this->m_countQtreeArr;
}

Int TMDCQPTable::readALineQp(Int iQPFile){
    char* buffer = new char[BUFFER_READ_SIZE];
    // get the buffer from the file
    switch (iQPFile)
    {
        case 1:
            if(fpQPFile1.is_open()){
                fpQPFile1.getline(buffer, BUFFER_READ_SIZE);
            }
            else
            {
                throw std::runtime_error("readALineQp: Unexpected closed file");
            }
            break;
        case 2:
            if(fpQPFile2.is_open()){
                fpQPFile2.getline(buffer, BUFFER_READ_SIZE);
            }
            else
            {
                throw std::runtime_error("readALineQp: Unexpected closed file");
            }
            break;
    default:
        throw std::runtime_error("Bad iQP");
        break;
    }
    //parsing this buffer
    this->m_countQPArr = convertStringToIntArrayQP(qpArray,buffer,BUFFER_READ_SIZE);
    delete[] buffer;
    return this->m_countQPArr;
}
TMDCQPTable::~TMDCQPTable(){
    delete [] qpArray;
    delete [] qtreeArray;
    fpQtreeFile.close();
    fpQPFile1.close();
    fpQPFile2.close();
}