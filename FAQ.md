# FAQ

## Installation
- Q: pip install fails?
  - A: Upgrade pip, ensure Python>=3.8, check network mirrors.

## CLI
- Q: circular-bias not found?
  - A: Reinstall with pip install -e .[cli] or ensure Scripts/ on PATH (Windows).

## Web App
- Q: Blank page?
  - A: Run 
pm install then 
pm run dev, open http://localhost:5173

## Data/CSV
- Q: Missing required columns?
  - A: See README 'CSV Data Format' and examples in data/.

## Encoding/Line Endings
- Q: README shows garbled text?
  - A: Use UTF-8 encoding; [.gitattributes](cci:7://file:///c:/Users/14593/CascadeProjects/circular-bias-detection/.gitattributes:0:0-0:0) enforces * text=auto eol=lf.
