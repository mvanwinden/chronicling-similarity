# Chronicling similarity
This Python script computes the Jaccard similarity of year descriptions within XML-parsed chronicles of Rotterdam. This serves as a demonstration of the potential applications of this method in quantifying the extent of text reuse in the chronicles of Rotterdam.

## Usage
1. Clone or download the repository to your local machine.
2. Navigate to the directory where the repository is located.
3. Ensure that you have the required Python libraries installed. The required libraries are pandas, numpy, seaborn, and matplotlib.
4. Place the reference file parsed_rotterdam_chronicles.ndjson in the same directory as chronicling_similarity.py.
5. Run the script with the following command: python chronicling_similarity.py
6. The output will be a heatmap of the Jaccard similarity values between pairs of chronicles, displayed in a new window.
