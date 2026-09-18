#include <stdio.h> #include <stdlib.h>
#include <string.h>

int main( int argc,char *argv[]){
  //Pre: el mensajeCifrado está en castellano y sin tildes
  if(argc != 2){
    printf("uso: brute_cesar \"mensaje cifrado\"");
    exit(0);
  }

  char *mensajeCifrado = argv[1];

  for (int i = 0; i < 27; i++){
    printf("\nIteracion %d: ", i);

    for (int j = 0; j < strlen(mensajeCifrado); j++){

      if((mensajeCifrado[j] >64 && mensajeCifrado[j] < 91) || (mensajeCifrado[j] > 96 && mensajeCifrado[j] < 123) || (mensajeCifrado == 164 || mensajeCifrado == 165)){ //si no es una letra se salta
        mensajeCifrado[j] = mensajeCifrado[j] + 1;

        if(mensajeCifrado[j] == 91){
          mensajeCifrado[j] = 65;
        }

        if(mensajeCifrado[j] == 123){
          mensajeCifrado[j] = 97;
        }
      }
    }

    printf("%s", mensajeCifrado);
  }

  exit(1);


}
