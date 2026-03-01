PDF=build/main.pdf

all: $(PDF)

$(PDF): main.tex
	latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex

clean:
	latexmk -C -output-directory=build main.tex || true
	rm -rf build
