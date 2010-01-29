.PHONY: pdf clean proper

PAPER := report
TEXFILE := $(PAPER).tex
BIBFILE := $(PAPER)
PDFFILE := $(PAPER).pdf

OPEN := open

LATEX := pdflatex
BIBTEX := bibtex

SUFFIXES := .aux .log .maf .mtc .mtc1 .out .bbl .blg .toc
FILES := $(addprefix $(PAPER), $(SUFFIXES))

## TODO: play around with double colon rules!

PDF_DEFS := $(TEXFILE)

ifeq ($(EMACS), t)
	PDF_DEFS += clean
endif

pdf: $(PDF_DEFS)
	$(LATEX) $(TEXFILE)
	$(BIBTEX) $(BIBFILE)
	$(LATEX) $(TEXFILE)
	$(LATEX) $(TEXFILE)

ifeq ($(EMACS), t)
	 $(OPEN) $(PDFFILE)
endif

clean:
	@$(RM) $(FILES) *~

proper: clean
	@$(RM) $(PDFFILE)
