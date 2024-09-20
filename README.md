# Repository for NORA Project, data extraction

## Setup GROBID
For transforming PDF files into XML format(more precisely TEI XML), the Grobid tool is used. There are multiple ways to setup this tool, the easiest one being using Docker. Assuming that docker is installed in the system, this command can be used to start the GROBID server on port 8081:

```
docker run --rm --init --ulimit core=0 -p 8081:8070 lfoppiano/grobid:0.8.0
```

The port can be changed to any other port if needed (by changing the first port number in the command). The GROBID server can then be accessed at http://localhost:8081. All the following commands will use this port as a default. More detailed information about Grobid in docker can be found in the [GROBID documentation](https://grobid.readthedocs.io/en/latest/Introduction/).

## Create TEI files
All files that are to be transformed should be placed in the same folder. There is a script in the lib folder that will take all the files from this folder and create Tei files from them. This script can be called from the command line from the top-level folder:
```
python3 code/grobid/pdf_to_tei.py --folder example_teis --output_folder example_teis
```
Optionally you can use -v to print verbose output or --port to change the port(default is 8081).

```
python3 code/grobid/pdf_to_tei.py --folder example_teis --output_folder example_teis --port 8081 -v
```
This may take some time. If -v is used, progress will be reported after every processed file. Grobid uses 10 threads by default and so does the script.

## Extracting Administrative Information
The script that extracts the administrative information can be run easily as:
```
python3 code/main.py
```
It takes all opinions from example_opinions folder, in the given structure (1 folder per question number), as it was the structure obtained by EFSA.
The result is in outputs/example_extracted_info.csv.

## Extracting Composition Information
The script that extracts the composition information is located in gpt_parsing/composition.py.
It excepts OpenAI API key to be saved in .env file in the environment. The file with the opinions can be set using enviroment variable OPINIONS_FOLDER.
It places the output in outputs/specifications folder, where some examples may be found.

## Final results
The main.py script was used on all opinions, and the resulting file is located in outputs/administrative_all.csv.

All the specifications outputs were merged into one long table, which is in outputs/composition_question.csv.
