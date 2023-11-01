These scripts use data from OpenAlex API, at "https://api.openalex.org/works".


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
- Download and start MariaDB service.
- Run data_reader.
- Run analysis.