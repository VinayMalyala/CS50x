#include <stdio.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[]){
    FILE *src = fopen(argv[1], "rb");
    FILE *dst = fopen(argv[2], "wb");

    BYTE b;

    while(fread(&b, sizeof(b), 1, src) != 0){
        fwrite(&b, sizeof(b), 1, dst); //./cp cat.jpg backup.jpg
    }
    //copies images from one file to another pixel by pixel
    fclose(dst);
    fclose(src);
}
