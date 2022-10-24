CIRCUITS = $(wildcard *.svg)
CIRCUITSPDF=$(CIRCUITS:.svg=.pdf)

%.pdf: %.svg
	@echo -e "\033[1m** Generating PDF from $<\033[0m"
	@inkscape -T -D -o $@ $<
	@pdfcrop $@ $@

.PHONY: all

all: $(CIRCUITSPDF) 

.PHONY: clean

clean:
	@rm -f *~ *.eps *.pdf
