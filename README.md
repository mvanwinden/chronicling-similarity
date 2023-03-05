# Chronicling similarity
This Python script computes the Jaccard similarity of year descriptions within XML-parsed chronicles. For demonstration purposes, this repository contains a corpus of five seventeenth-century Rotterdam chronicles. 

## Usage
```bash
git clone https://github.com/mvanwinden/chronicling-similarity
cd chronicling-similarity
pip install -r requirements.txt
chronicling_similarity.py
```

Plots of the event distribution and the jaccard similarities will be saved to the directory as a vector image.

## Acknowledgements
The corpus of Rotterdam chronicles was created using an XML-parser developed by the Aarhus University Centre for Humanities Computing, which is available at https://github.com/centre-for-humanities-computing/dutch-chronicles. 
