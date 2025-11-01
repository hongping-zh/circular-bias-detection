# FAQ

## Installation
- pip install fails?
  - Upgrade pip, ensure Python>=3.8, check network availability/mirrors.

## CLI
- circular-bias not found?
  - pip install -e .[cli] or ensure Python/Scripts is on PATH (Windows).

## Web App
- Blank page?
  - npm install && npm run dev, open http://localhost:5173

## Data/CSV
- Missing required columns?
  - See README 'CSV Data Format' and data/sample_data.csv.

## Encoding/Line Endings
- Garbled README?
  - Use UTF-8; [.gitattributes](cci:7://file:///c:/Users/14593/CascadeProjects/circular-bias-detection/.gitattributes:0:0-0:0) enforces * text=auto eol=lf.
