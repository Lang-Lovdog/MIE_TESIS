#!/bin/bash
cat << TeXHeader > documento.tex
\documentclass[twocolumn,a4paper]{article}
\usepackage[margin=1.5cm]{geometry}
\usepackage{graphicx}
\setlength{\parindent}{0pt}
\begin{document}
TeXHeader

#for img in LearningCurve*.png; do
for img in ConfusionMatrix*.png; do
    echo "\noindent\includegraphics[width=0.88\linewidth]{$img}\par\vspace{0.5cm}" >> documento.tex
done

echo '\end{document}' >> documento.tex

pdflatex documento.tex
