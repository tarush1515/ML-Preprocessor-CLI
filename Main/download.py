import pandas as pd


class Download:
    def __init__(self, data, style):
        self.data = data
        self.style = style

    # download the modified DataFrame as .csv file
    def download(self):
        toBeDownload = {}
        for column in self.data.columns.values:
            toBeDownload[column] = self.data[column]

        newFileName = input(
            "\nEnter the " + "FILENAME" + " you want? (without .csv) : "
        )
        # if newFileName == "-1":
        #     return
        newFileName = newFileName + ".csv"
        # index=False as this will not add an extra column of index.
        pd.DataFrame(self.data).to_csv(newFileName, index=False)

        print("Hurray!! It is done....\U0001F601")

        if input("Do you want to exit now? (y/n) ").lower() == "y":
            print("Exiting...\U0001F44B")
            exit()
        else:
            return
