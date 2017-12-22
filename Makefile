# latex Makefile
ifndef texpath
texpath=/usr/texbin/
endif
PDFLATEX=pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
#PDFLATEX=/usr/bin/pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
BIBTEX=bibtex
DVIPS=dvips
PS2PDF=ps2pdf
SHELL=/bin/bash

all: main.tex

.PHONY: main.tex
main.tex: 
	echo "texpath: ${texpath}"
	${PDFLATEX} main.tex
	${BIBTEX} main
	${PDFLATEX} main.tex
	${BIBTEX} main
	${PDFLATEX} main.tex
	#python local_build.py --no-bibtex
	#cp authorea_build/authorea_paper.pdf main.pdf
	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=main_compressed.pdf main.pdf

