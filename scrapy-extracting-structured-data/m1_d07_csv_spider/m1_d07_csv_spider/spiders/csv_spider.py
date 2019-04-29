from scrapy.spiders import CSVFeedSpider


# Examine the CSV file first to understand what it looks like
class CsvDataset(CSVFeedSpider):

    name = 'csv_spider'
    
    start_urls = ['https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv']

    # We explicitly specify the delimiter, quotechar and headers for the file
    delimiter = ';'
    quotechar = '"'
    headers = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'free sulfur dioxide',
               'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'quality']

    # This method gets called for each iteration/row in the CSV file
    def parse_row(self, response, row):

        # Here, we simply print out specific column values from each row
        print('pH = ', row['pH'], '\tAlcohol Content =', row['alcohol'], '\tWine Quality = ', row['quality'])
