# Report source and rendering

The eight-page PDF was rendered from the delivered editable DOCX and visually inspected on every page. The same three diagrams are supplied as SVG and PNG. The DOCX and PDF contain the same report content.

`scripts/build_report.py` regenerates the DOCX and diagrams from the included study metadata and source text. Its authoring versions are recorded in `environment/report-toolchain.json`; these authoring packages are separate from the offline application/test wheel set. They are not required to reproduce the investigation. A local LibreOffice installation can export a regenerated DOCX to PDF with `soffice --headless --convert-to pdf --outdir report report/ISE-A3-Final-Report.docx`. Fonts and office versions may affect reflow; review a regenerated layout before submission.
