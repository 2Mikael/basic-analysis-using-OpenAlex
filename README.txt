These scripts read, store, and perform simple analysis on data from OpenAlex API, at "https://api.openalex.org/works".

Files:
  data_reader:
  - GETs text from the API with several content filters as arguments.
  - Parses the text into a more suitable form for this project.
  - Saves the parsed text into a MariaDB database, which must be set up separately.
  
  database:
  - Contains logic for accessing the MariaDB database.
  - Populated by data_reader.
  - Read from by analysis.
  
  analysis:
  - Contains required analyses of the data.
  - Visualizes the results using matplotlib.pyplot library.

Usage:
- Download and start MariaDB.
- Setup database and tables, see instructions in the "database.py" file.
- Run data_reader.
- Run analysis.
