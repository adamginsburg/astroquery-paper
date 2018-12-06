# latex Makefile
ifndef texpath
texpath=/usr/texbin/
endif
PDFLATEX=pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
PDFLATEX=${texpath}/pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
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

diff:
	git show 63e21c1e134a9790f781cbf89539472643457d42:main.tex > main_submitted.tex
	latexdiff main.tex main_submitted.tex > diff.tex
	${PDFLATEX} diff.tex
	${PDFLATEX} diff.tex
	${PDFLATEX} diff.tex
