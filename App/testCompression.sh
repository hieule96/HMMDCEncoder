export FORCE_NO_INTRA=1
# export FORCE_LUMA_MODE=1
# export FORCE_CHROMA_MODE=4

./TAppEncoder -c ../MdcCfgns/encoder_intra_main.cfg -c ../sequence/foreman_cif.cfg -qf QP1.csv -o QP1.yuv -b QP1.hevc -qt qtreeAI.txt -em 1
./TAppEncoder -c ../MdcCfgns/encoder_intra_main.cfg -c ../sequence/foreman_cif.cfg -qf QP2.csv -o QP2.yuv -b QP2.hevc -qt qtreeAI.txt -em 1
# ./TAppEncoder -c ../MdcCfgns/encoder_lowdelay_P_main.cfg -c ../sequence/foreman_cif.cfg -qf QP1.csv -o QP1.yuv -b QP1.hevc -qt qtreeV.txt -em 1
# ./TAppEncoder -c ../MdcCfgns/encoder_lowdelay_P_main.cfg -c ../sequence/foreman_cif.cfg -qf QP2.csv -o QP2.yuv -b QP2.hevc -qt qtreeV.txt -em 1
# ./TAppDecoder -b QP1.hevc -o QP1.yuv
# ./TAppDecoder -b QP2.hevc -o QP2.yuv
