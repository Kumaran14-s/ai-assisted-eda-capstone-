# Dataset source, licence and limitations

## Bundled offline sample
`data/sample_penguins_demo.csv` is a **synthetic, manually assembled teaching sample**. It contains 20 rows, including repeated rows and missing values, so the dashboard can demonstrate data-quality checks without an internet connection. It is inspired by familiar penguin measurements but is not a copy of the official dataset. Do not use its numbers as ecological findings or cite it as the Palmer Penguins dataset.

## Recommended public research dataset: Palmer Penguins
- Project page: https://allisonhorst.github.io/palmerpenguins/
- Data package repository: https://github.com/allisonhorst/palmerpenguins
- Original research context: Palmer Station Long-Term Ecological Research (LTER), Antarctica; penguin observations and measurements.
- Commonly distributed `palmerpenguins` package data are provided under a CC0 public-domain dedication according to the package documentation. Re-check the exact file and licence at download time and include the licence text/attribution required by the copy you use.
- Data include species, island, bill dimensions, flipper length, body mass, and sex, with missing observations.
- Limits: a limited number of species and locations; observations are not a random sample of every penguin population; missing values may affect comparisons; observational data do not establish causal relationships. Confirm the original collection metadata before making biological claims.

## Reproducible research procedure
1. Download the data only from the official project/repository.
2. Save the original file unchanged and record its URL, download date, file name and checksum.
3. Inspect the file's licence and metadata.
4. Run the notebook and dashboard on the real file.
5. Replace every illustrative report statement with results from that run. Do not transfer synthetic-sample statistics into a real-dataset report.
