#NOM    : makefile
#CLASSE : RAPPORT - SysG5
#OBJET  : Rapport Project SysG5 : Time Setup
#HOWTO	: make; make clean
#AUTEUR	: 42933 Achetouan Mohammed - 45682 Kardillo Younes 

all: pdf clean

pdf: 
	#Ne fait pas la Table des matières
	#pdflatex latex/rapportTimeSetup.tex
	
	pdflatex latex/rapportTimeSetup.tex
	pdflatex latex/rapportTimeSetup.tex
	rm -f *.toc *.aux *.log *.out *.fls *.gz *.fdb_latexmk
	evince rapportTimeSetup.pdf &

%.pdf: %.tex
	rubber -m pdftex latex/$<  

clean:             
	rm -f *.toc *.aux *.log *.out

cleanall:             
	rm -f *.toc *.pdf *.aux *.log *.out  

.PHONY: all pdf clean cleanall

.SILENT: pdf
