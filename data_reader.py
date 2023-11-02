import requests
import json
import database

base_link = "https://api.openalex.org/works"
search = "search=Automatic Analysis of Radiologist Report"
sort = "sort=cited_by_count:desc"
select_fields = "select=title,authorships,abstract_inverted_index"
page_base = "per-page=100&page="
page = 1

# Concept-id "C140608501" represents review articles
filters = {
    "dataset1": "filter=has_abstract:true",
    "dataset2": "filter=has_abstract:true,concept.id:C140608501",
    "dataset3": "filter=has_abstract:true,from_publication_date:2018-10-01"
}

# Instructions suggested collecting 500 entries for first 2 datasets and 1000 for the 3rd, not sure if necessary.
data_counts_in_hundreds = {
    "dataset1": 5,
    "dataset2": 5,
    "dataset3": 10
}

def read_data(argument_string, count_in_hundreds) -> list[dict]:
    # Request specific amount of works matching given search arguments
    results = []
    base_url = base_link + "?" + argument_string
    for page in range(1, count_in_hundreds + 1):
        raw_result = requests.get(base_url + str(page))
        results_array = json.loads(raw_result.text)["results"] # Array of dictionary-like objects

        parsed_objects = []
        for obj in results_array:
            # Parse abstract string from inverted index
            inverted_index = obj["abstract_inverted_index"]
            abstract = ""
            word_dict = {}
            for word in inverted_index:
                indexes = inverted_index[word]
                for index in indexes:
                    word_dict[index] = word
            for tuple in sorted(word_dict.items(), key=lambda x: x[0]):
                abstract += tuple[1] + " "
            abstract = abstract[:-1] # Cut the last whitespace (" ") from the string
            
            # Turn authorships object into string like: "name1;name2;name3;..."
            authors = []
            for authorship in obj["authorships"]:
                name = authorship["author"]["display_name"]
                authors.append(name)
            authors = ";".join(authors)
            
            # Create a new object for parsed data
            parsed_objects.append({
                "title": obj["title"], 
                "abstract": abstract, 
                "authors": authors
            })
        results.extend(parsed_objects)
    return results

for dataset in ["dataset1", "dataset2", "dataset3"]:
    # Get filtered works based on dataset
    filter = filters[dataset]
    arguments = "&".join([search, sort, filter, select_fields, page_base])
    results = read_data(arguments, data_counts_in_hundreds[dataset])
    # Save works into correct database table
    for work in results:
        title = work["title"]
        authors = work["authors"]
        abstract = work["abstract"]
        database.add_work(title=title, authors=authors, abstract=abstract, table=dataset)