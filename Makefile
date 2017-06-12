# latex Makefile
ifndef texpath
texpath=/usr/texbin/
endif
PDFLATEX=${texpath}pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
SKIPERR=${texpath}pdflatex --interaction=nonstopmode
LATEX=${PDFLATEX}
BIBTEX=bibtex
DVIPS=dvips
PS2PDF=ps2pdf

all: main.tex

.PHONY: main.tex
main.tex: 
	echo "texpath: ${texpath}"
	#${PDFLATEX} main.tex
	python local_build.py --no-bibtex
	cp authorea_build/authorea_paper.pdf main.pdf
	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=main_compressed.pdf main.pdf

