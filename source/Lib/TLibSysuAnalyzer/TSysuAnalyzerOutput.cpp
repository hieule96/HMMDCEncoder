#include "TSysuAnalyzerOutput.h"

TSysuAnalyzerOutput* TSysuAnalyzerOutput::m_instance = NULL;

TSysuAnalyzerOutput::TSysuAnalyzerOutput()
{

  //m_cSpsOut.open     ("decoder_sps.txt",  ios::out);
  //m_cPredOutput.open ("decoder_pred.txt", ios::out);
  m_cCUPUOutput.open ("decoder_cupu.txt", ios::out);
  m_CbfOutput.open("cbfFile.txt",ios::out);
  //m_cMVOutput.open   ("decoder_mv.txt",   ios::out);
  //m_cMergeOutput.open("decoder_merge.txt",ios::out);
  //m_cIntraOutput.open("decoder_intra.txt",ios::out);
  //m_cTUOutput.open   ("decoder_tu.txt",   ios::out);
  //m_cMEOutput.open   ("encoder_me.txt",   ios::out);
  //m_cBitOutputLCU.open  ("decoder_bit_lcu.txt",  ios::out);
  //m_cBitOutputSCU.open  ("decoder_bit_scu.txt",  ios::out);
#if ( HM_VERSION > 40)
  m_cTileOutPut.open("decoder_tile.txt", ios::out);
#endif


}

void TSysuAnalyzerOutput::writeNewLineQP() {
    m_QPFile << std::endl;
}


void TSysuAnalyzerOutput::writeQP(Int QP, const char *delimiter) {
    m_QPFile << QP << delimiter;
}


void TSysuAnalyzerOutput::writeDqp(Int dQP, const char *delimiter){
    m_CbfOutput<<dQP<<delimiter;
}

void TSysuAnalyzerOutput::writeNewLineDqp() {
    m_CbfOutput << std::endl;
}

TSysuAnalyzerOutput::TSysuAnalyzerOutput(const char* cupu_name)
{

    //m_cSpsOut.open("decoder_sps.txt", ios::out);
    //m_cPredOutput.open("decoder_pred.txt", ios::out);
    m_cCUPUOutput.open(cupu_name, ios::out);
    m_CbfOutput.open("cbfFileEncoder.txt",ios::out);
    //m_cMVOutput.open("decoder_mv.txt", ios::out);
    //m_cMergeOutput.open("decoder_merge.txt", ios::out);
    //m_cIntraOutput.open("decoder_intra.txt", ios::out);
    //m_cTUOutput.open("decoder_tu.txt", ios::out);
    //m_cMEOutput.open("encoder_me.txt", ios::out);
    //m_cBitOutputLCU.open("decoder_bit_lcu.txt", ios::out);
    //m_cBitOutputSCU.open("decoder_bit_scu.txt", ios::out);
    //m_cCUOutputResi.open("residual.yuv", ios::out);
#if ( HM_VERSION > 40)
    m_cTileOutPut.open("decoder_tile.txt", ios::out);
#endif


}

TSysuAnalyzerOutput::TSysuAnalyzerOutput(const char* cupu_name, const char* qpDecFile)
{
    char buffer[20];
    memset(buffer,0,20*sizeof(char));
    m_cCUPUOutput.open(cupu_name, ios::out);
    sprintf(buffer,"%s_Cbf.txt",qpDecFile);
    m_CbfOutput.open(buffer,ios::out);
    memset(buffer,0,20*sizeof(char));
    sprintf(buffer,"%s_2.txt",qpDecFile);
    m_QPFile2.open(qpDecFile,ios::out);
    m_QPFile.open(buffer, ios::out);
}

#if ( HM_VERSION > 40)
//write out tile info
void TSysuAnalyzerOutput::writeOutTileInfo(TComPic * pcPic)
{
    int iPoc = pcPic ->getPOC();
    int iTileNumRows =  pcPic ->getPicSym() ->getNumRowsMinus1()+1;
    int iTileNumCols = pcPic ->getPicSym() ->getNumColumnsMinus1()+1;


    for( int uiRowIdx=0; uiRowIdx < iTileNumRows; uiRowIdx++ )
           for( int uiColumnIdx=0; uiColumnIdx <iTileNumCols ; uiColumnIdx++ )
           {
             int uiTileIdx = uiRowIdx * (iTileNumCols) + uiColumnIdx;

             //information for each tile
             int uiTileWidth = 0;
             int uiTileHeight = 0;
             int uiFirstCUAddr = 0;

             uiTileWidth = pcPic ->getPicSym()->getTComTile(uiTileIdx)->getTileWidth();

             uiTileHeight = pcPic ->getPicSym()->getTComTile(uiTileIdx)->getTileHeight();

             uiFirstCUAddr = pcPic ->getPicSym()->getTComTile(uiTileIdx) ->getFirstCUAddr();

             m_cTileOutPut << "<" << iPoc << "," << (iTileNumCols )* (iTileNumRows )<< ">"
                  << " " << uiFirstCUAddr << " " << uiTileWidth << " " << uiTileHeight << endl;


           }
}

#endif




void TSysuAnalyzerOutput::writeOutCUInfo   ( TComDataCU* pcCU )
{
  Int iPoc = pcCU->getSlice()->getPOC();
  Int iAddr = pcCU->getCtuRsAddr();
  Int iTotalNumPart = pcCU->getTotalNumPart();


  //m_cPredOutput << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out prediction info
  m_cCUPUOutput << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out CU & PU splitting info
  //m_cMVOutput   << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out me info
  //m_cMergeOutput<< "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out merge mode info
  //m_cIntraOutput<< "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out intra mode info
  //m_cTUOutput   << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out TU mode info
  //m_cBitOutputLCU << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out bit info
  //m_cBitOutputSCU << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out bit info
  //m_cMEOutput   << "<" << iPoc << "," << iAddr << ">" << " ";  ///< Write out ME info  
  m_CbfOutput << "<" << iPoc << "," << iAddr << ">" << " "; // write out cbf flag
  xWriteOutCUInfo  ( pcCU, iTotalNumPart, 0, 0 );   ///< Recursive write Prediction, CU, PU, Merge, Intra, ME
  //m_cBitOutputLCU << pcCU->getTotalBits(); ///< Bit info
  //for(int i = 0; i < aiCUBits.size(); i++)
  //  m_cBitOutputSCU << aiCUBits.at(i) << " "; ///< Bit info

  //m_cPredOutput << endl;
  m_cCUPUOutput << endl;
  m_CbfOutput << endl;
  m_QPFile2 << endl;
  //m_cMVOutput   << endl;
  //m_cMergeOutput<< endl;
  //m_cIntraOutput<< endl;
  //m_cTUOutput   << endl;
  //m_cBitOutputLCU  << endl;
  //m_cBitOutputSCU  << endl;
  //m_cMEOutput   << endl;
}


void TSysuAnalyzerOutput::xWriteOutCUInfo  ( TComDataCU* pcCU, Int iLength, Int iOffset, UInt iDepth )
{
  
  UChar* puhDepth    = pcCU->getDepth();
  SChar * puhPartSize = pcCU->getPartitionSize();
  UChar * puhCbf = pcCU->getCbf(COMPONENT_Y);
  SChar* puhQP = pcCU->getQP();
  TComMv rcMV;

  if( puhDepth[iOffset] <= iDepth )
  {
    ///< CU PU info
    m_cCUPUOutput << (Int)(puhPartSize[iOffset]) << " "; 

    ///< TU info
    //xWriteOutTUInfo  ( pcCU, iLength, iOffset, 0 );   ///< Recursive write TU
    

    /// PU number in this leaf CU
    int iNumPart = 0;           

    switch ( puhPartSize[iOffset] )
    {
    case SIZE_2Nx2N:    iNumPart = 1; break;
    case SIZE_2NxN:     iNumPart = 2; break;
    case SIZE_Nx2N:     iNumPart = 2; break;
    case SIZE_NxN:      iNumPart = 4; break;
    case SIZE_2NxnU:    iNumPart = 2; break;
    case SIZE_2NxnD:    iNumPart = 2; break;
    case SIZE_nLx2N:    iNumPart = 2; break;
    case SIZE_nRx2N:    iNumPart = 2; break;
    default:    iNumPart = 0;  /*assert(0);*/  break;  ///< out of boundery
    }

    /// Traverse every PU
    int iPartAddOffset = 0;   ///< PU offset
    for( int i = 0; i < iNumPart; i++ )
    {

      switch ( puhPartSize[iOffset] )
      {
      case SIZE_2NxN:
        iPartAddOffset = ( i == 0 )? 0 : iLength >> 1;
        break;
      case SIZE_Nx2N:
        iPartAddOffset = ( i == 0 )? 0 : iLength >> 2;
        break;
      case SIZE_NxN:
        iPartAddOffset = ( iLength >> 2 ) * i;
        break;
      case SIZE_2NxnU:    
        iPartAddOffset = ( i == 0 ) ? 0 : iLength >> 3;
        break;
      case SIZE_2NxnD:    
        iPartAddOffset = ( i == 0 ) ? 0 : (iLength >> 1) + (iLength >> 3);
        break;
      case SIZE_nLx2N:    
        iPartAddOffset = ( i == 0 ) ? 0 : iLength >> 4;
        break;
      case SIZE_nRx2N:   
        iPartAddOffset = ( i == 0 ) ? 0 : (iLength >> 2) + (iLength >> 4);
        break;
      default:
        assert ( puhPartSize[iOffset] == SIZE_2Nx2N );
        iPartAddOffset = 0;
        break;
      }

      ///// Write prediction info (for historical reason, MODE_SKIP = 0, MODE_INTER = 1 ....) (SKIP mode removed after HM-8.0)
      m_CbfOutput << (Int) puhCbf[iOffset] << " ";
      m_QPFile2 << (Int) puhQP[iOffset] <<",";
      /// Write merge info
      //Bool bMergeFlag = pcCU->getMergeFlag(iOffset+iPartAddOffset);      
      //Int iMergeIndex = pcCU->getMergeIndex(iOffset+iPartAddOffset);
      //if(bMergeFlag)
      //  m_cMergeOutput << iMergeIndex << " ";
      //else
      //  m_cMergeOutput << -1 << " ";

      /// Write MV info
      //Int iInterDir = pcCU->getInterDir(iOffset+iPartAddOffset);   ///< Inter direction: 0--Invalid, 1--List 0 only, 2--List 1 only, 3--List 0&1(bi-direction)
      //int iRefIdx = -1;
      //m_cMVOutput << iInterDir << " ";
      //if( iInterDir == 0 )
      //{
      //  // do nothing
      //}
      //else if ( iInterDir == 1 )
      //{
      //  rcMV= pcCU->getCUMvField(REF_PIC_LIST_0)->getMv(iOffset+iPartAddOffset);	
      //  iRefIdx = pcCU->getCUMvField(REF_PIC_LIST_0)->getRefIdx(iOffset+iPartAddOffset);
      //  m_cMVOutput << pcCU->getSlice()->getRefPOC(REF_PIC_LIST_0, iRefIdx) << " " << rcMV.getHor() << " " << rcMV.getVer() << " ";
      //}
      //else if ( iInterDir == 2 )
      //{
      //  rcMV= pcCU->getCUMvField(REF_PIC_LIST_1)->getMv(iOffset+iPartAddOffset);
      //  iRefIdx = pcCU->getCUMvField(REF_PIC_LIST_1)->getRefIdx(iOffset+iPartAddOffset);
      //  m_cMVOutput << pcCU->getSlice()->getRefPOC(REF_PIC_LIST_1, iRefIdx) << " " << rcMV.getHor() << " " << rcMV.getVer() << " ";
      //}
      //else if ( iInterDir == 3 )
      //{
      //  rcMV= pcCU->getCUMvField(REF_PIC_LIST_0)->getMv(iOffset+iPartAddOffset);	
      //  iRefIdx = pcCU->getCUMvField(REF_PIC_LIST_0)->getRefIdx(iOffset+iPartAddOffset);
      //  m_cMVOutput << pcCU->getSlice()->getRefPOC(REF_PIC_LIST_0, iRefIdx) << " " << rcMV.getHor() << " " << rcMV.getVer() << " ";
      //  rcMV= pcCU->getCUMvField(REF_PIC_LIST_1)->getMv(iOffset+iPartAddOffset);
      //  iRefIdx = pcCU->getCUMvField(REF_PIC_LIST_1)->getRefIdx(iOffset+iPartAddOffset);
      //  m_cMVOutput << pcCU->getSlice()->getRefPOC(REF_PIC_LIST_1, iRefIdx) << " " << rcMV.getHor() << " " << rcMV.getVer() << " ";
      //}    

      ///// Write Intra info
      //Int iLumaIntraDir   = pcCU->getIntraDir(CHANNEL_TYPE_LUMA,iOffset+iPartAddOffset);
      //Int iChromaIntraDir = pcCU->getIntraDir(CHANNEL_TYPE_CHROMA,iOffset+iPartAddOffset);
      //m_cIntraOutput << iLumaIntraDir << " " << iChromaIntraDir << " ";




    } /// PU end
  }
  else
  {
    m_cCUPUOutput << "99" << " ";     ///< CU info
    for( UInt i = 0; i < 4; i++ )
    {
      xWriteOutCUInfo  ( pcCU, iLength/4, iOffset+iLength/4*i, iDepth+1);
    }
  }
}


//Void TSysuAnalyzerOutput::xWriteOutTUInfo  ( TComDataCU* pcCU, Int iLength, Int iOffset, UInt iDepth)
//{
//  UChar* puhTranIdx  = pcCU->getTransformIdx();
//  if( puhTranIdx[iOffset] <= iDepth )
//  {
//    /// Write TU info
//    m_cTUOutput << (Int)(puhTranIdx[iOffset]) << " ";
//  }
//  else
//  {
//    m_cTUOutput << "99" << " ";     
//    for( UInt i = 0; i < 4; i++ )
//    {
//      xWriteOutTUInfo  ( pcCU, iLength/4, iOffset+iLength/4*i, iDepth+1);
//    }
//  }
//}

//Void TSysuAnalyzerOutput::writeOutSps   ( TComSPS* pcSPS )
//{
//#define HM_VERSION 160
//#if (HM_VERSION >= 100)
//  m_cSpsOut << "Resolution:"   << pcSPS->getPicWidthInLumaSamples() << "x" << pcSPS->getPicHeightInLumaSamples() << endl;
//#else
//  m_cSpsOut << "Resolution:"   << pcSPS->getWidth() << "x" << pcSPS->getHeight() << endl;
//#endif
//
//  m_cSpsOut << "Max CU Size:"  << pcSPS->getMaxCUHeight() << endl;
//  m_cSpsOut << "Max CU Depth:" << pcSPS->getMaxTotalCUDepth() << endl;
//  m_cSpsOut << "Max Inter TU Depth:" << pcSPS->getQuadtreeTUMaxDepthInter() << endl;
//  m_cSpsOut << "Max Intra TU Depth:" << pcSPS->getQuadtreeTUMaxDepthIntra() << endl;
//
//#if (HM_VERSION >= 100)
//  int iInputBitDepth = pcSPS->getBitDepth(CHANNEL_TYPE_LUMA);
//#else
//  int iInputBitDepth = pcSPS->getBitDepth();
//#endif
//
//  m_cSpsOut << "Input Bit Depth:"  << iInputBitDepth  << endl;
//
//}


TSysuAnalyzerOutput::~TSysuAnalyzerOutput()
{
  m_cCUPUOutput.close();
  m_CbfOutput.close();
  //m_cMVOutput.close();
  //m_cPredOutput.close();
  //m_cSpsOut.close();
  //m_cIntraOutput.close();
  //m_cTUOutput.close();
  //m_cBitOutputLCU.close();
  //m_cBitOutputSCU.close();
  //m_cMEOutput.close();
  //m_cCUOutputResi.close();
//#if (HM_VERSION >40)
//   m_cTileOutPut.close();
//#endif
}
