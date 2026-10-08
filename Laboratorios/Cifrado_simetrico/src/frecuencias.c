#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  // Pre: el mensajeCifrado está en castellano y sin tildes ni ñ
  if (argc != 2) {
      printf("uso: frec \"mensaje cifrado\"");
      return 1;
  }

  const char charMasFrec = 'e';

  char *mensajeCifrado = argv[1];
  int desplazamiento = 0;
  int apariciones[26] = {0};
  int longitud = strlen(mensajeCifrado);

  for (int i = 0; i < longitud; i++) {

      if (mensajeCifrado[i] >= 'A' && mensajeCifrado[i] <= 'Z') {
          apariciones[mensajeCifrado[i] - 'A']++;
      }
      else if (mensajeCifrado[i] >= 'a' && mensajeCifrado[i] <= 'z') {
          apariciones[(mensajeCifrado[i] - 'a')]++;
      }
  }

  int frec = 0;
  int indiceMasFrec = 0;

  for (int i = 0; i < 26; i++) {
    if (apariciones[i] > frec) {
        frec = apariciones[i];
        indiceMasFrec = i;
    }
  }

  desplazamiento = (charMasFrec - 'a') - indiceMasFrec;

  for (int j = 0; j < longitud; j++) {

      if (mensajeCifrado[j] >= 'A' && mensajeCifrado[j] <= 'Z') {
          mensajeCifrado[j] = 'A' + (mensajeCifrado[j] - 'A' + desplazamiento + 26) % 26;
      }
      else if (mensajeCifrado[j] >= 'a' && mensajeCifrado[j] <= 'z') {
          mensajeCifrado[j] = 'a' + (mensajeCifrado[j] - 'a' + desplazamiento + 26) % 26;
      }
  }

  printf("%s\n", mensajeCifrado);

  return 0;
}
