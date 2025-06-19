# Rules of figure_worker

---

[toc]

## Domain

The rules apply to modules like `figure_worker.car.fig1_xxx` or `figure_worker.mouse.fig1_yyy`.

## Rules

### Rule: Main

The `main.py` is required, it contains `Processor` class with attributes:

- readme_legend, str, the content of `## 图像 legend （给用户看的）` in `readme.md` .
- worker, object, [Rule: Object](#rule-object) plot the matplotlib figure and compute results.

also with methods:

- process, process the data and generate figure and results as iterator.
- extract_and_draw, inner method for figure and results generation, also provide class safety functional.
- read_example_data, read the example data from the `input` folder.

### Rule: Object

It has working class playing as entrance, the `extract_and_draw` method returns dict:

- fig, matplotlib's fig, the figure being plotted.
- report, dict, the results in detail.
- name, str, the name of the analysis.
- _NeedSave, (Optional) dict, the results to be saved by the db.
- _NoPDF, (Optional) boolean, wether to render the figure and report into the pdf.
