#include "ExportC.h"
TEncTop* newInstance() {
    printf("Create New TEncTop\n");
    return new TEncTop();
}