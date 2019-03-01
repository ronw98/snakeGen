#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define NB_FRUITS 100
int main()
{
	srand(time(NULL));
	int ** tab = (int **) malloc(NB_FRUITS * sizeof(int*));
	int i=0;
	for(i = 0; i<NB_FRUITS; i++)
	{
		tab[i] = (int *) malloc(2*sizeof(int));
		tab[i][0] = rand() % 28 + 1;
		tab[i][1] = rand() % 28 + 1;
	}

	FILE * fic = NULL;
	fic = fopen("tab.txt","w");
	if(fic == (FILE *) NULL)
		return EXIT_FAILURE;
	for(i = 0; i<NB_FRUITS-1; i++)
	{
		fprintf(fic,"(%d,%d),",tab[i][0],tab[i][1]);
	}
	fprintf(fic,"(%d,%d)",tab[NB_FRUITS-1][0],tab[NB_FRUITS-1][1]);
	fclose(fic);
	return 0;

}
